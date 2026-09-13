from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Notification, User
from backend.schemas import (
    MarkNotificationRequest,
    NotificationResponse
)
from backend.security import get_current_user


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get(
    "",
    response_model=list[NotificationResponse]
)
def get_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id
        )
    )

    if unread_only:
        query = query.filter(
            Notification.is_read == False
        )

    return (
        query
        .order_by(Notification.created_at.desc())
        .limit(100)
        .all()
    )


@router.get(
    "/unread-count"
)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .count()
    )

    return {
        "count": count
    }


@router.patch(
    "/{notification_id}",
    response_model=NotificationResponse
)
def update_notification(
    notification_id: int,
    data: MarkNotificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = data.is_read

    db.commit()
    db.refresh(notification)

    return notification


@router.post(
    "/read-all"
)
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .update(
            {"is_read": True},
            synchronize_session=False
        )
    )

    db.commit()

    return {
        "message": "All notifications marked as read"
    }


@router.delete(
    "/{notification_id}"
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()

    return {
        "message": "Notification deleted successfully"
    }