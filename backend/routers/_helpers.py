from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import GroupMember, Notification, User


def require_member(
    group_id: int,
    db: Session,
    current_user: User
):
    membership = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )

    return membership


def require_admin(
    group_id: int,
    db: Session,
    current_user: User
):
    membership = require_member(
        group_id,
        db,
        current_user
    )

    if membership.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Group admin permission required"
        )

    return membership


def create_notification(
    db: Session,
    user_id: int,
    group_id: int | None,
    notification_type: str,
    message: str,
    title: str | None = None
):
    title_map = {
        "task_assigned": "New Task Assigned",
        "task_completed": "Task Completed",
        "food_order": "New Food Order",
        "food_status": "Food Order Updated",
        "gallery": "New Gallery Item",
        "expense": "New Expense",
        "chat": "New Chat Message",
        "poll": "New Poll Activity",
        "general": "GatherUp Notification"
    }

    if title is None:
        title = title_map.get(
            notification_type,
            "GatherUp Notification"
        )

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type,
        is_read=False
    )

    db.add(notification)

    return notification