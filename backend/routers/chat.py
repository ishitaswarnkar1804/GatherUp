import json

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import GroupMember, GroupMessage, User
from backend.routers._helpers import create_notification
from backend.security import JWT_SECRET, JWT_ALGORITHM


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


active_connections: dict[int, list[WebSocket]] = {}


def authenticate_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = int(payload.get("sub"))

        return user_id

    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid or expired token"
        )


def is_group_member(
    db: Session,
    group_id: int,
    user_id: int
) -> bool:

    membership = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        )
        .first()
    )

    return membership is not None


async def broadcast(
    group_id: int,
    message: dict
):

    connections = active_connections.get(
        group_id,
        []
    )

    disconnected = []

    for websocket in connections:

        try:
            await websocket.send_text(
                json.dumps(message)
            )

        except Exception:
            disconnected.append(websocket)

    for websocket in disconnected:

        if websocket in connections:
            connections.remove(websocket)

    if not connections:
        active_connections.pop(
            group_id,
            None
        )


@router.websocket("/ws/{group_id}")
async def group_chat_websocket(
    websocket: WebSocket,
    group_id: int,
    token: str
):

    user_id = authenticate_token(token)

    db: Session = SessionLocal()

    try:

        if not is_group_member(
            db,
            group_id,
            user_id
        ):

            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="You are not a member of this group"
            )

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:

            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="User not found"
            )

        await websocket.accept()

        active_connections.setdefault(
            group_id,
            []
        ).append(websocket)

        await websocket.send_text(
            json.dumps(
                {
                    "type": "connected",
                    "message": "Connected to group chat"
                }
            )
        )

        while True:

            data = await websocket.receive_text()

            try:
                payload = json.loads(data)

            except json.JSONDecodeError:
                continue

            message_text = str(
                payload.get("message", "")
            ).strip()

            if not message_text:
                continue

            if len(message_text) > 2000:
                continue

            message = GroupMessage(
                group_id=group_id,
                user_id=user_id,
                message=message_text
            )

            db.add(message)

            members = (
                db.query(GroupMember)
                .filter(GroupMember.group_id == group_id)
                .all()
            )

            for member in members:
                if member.user_id == user_id:
                    continue

                create_notification(
                    db=db,
                    user_id=member.user_id,
                    group_id=group_id,
                    notification_type="chat",
                    message=(
                        f"{user.first_name} {user.last_name} sent a message "
                        f"in your group: {message_text}"
                    )
                )

            try:
                db.commit()
                db.refresh(message)
            except Exception:
                db.rollback()
                raise

            chat_message = {
                "type": "message",
                "id": message.id,
                "group_id": group_id,
                "user_id": user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "message": message.message,
                "created_at": message.created_at.isoformat()
            }

            await broadcast(
                group_id,
                chat_message
            )

    except WebSocketDisconnect:

        pass

    finally:

        connections = active_connections.get(
            group_id,
            []
        )

        if websocket in connections:
            connections.remove(websocket)

        if not connections:

            active_connections.pop(
                group_id,
                None
            )

        db.close()