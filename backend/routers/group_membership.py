from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Group, GroupMember, User
from backend.security import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["Group Membership"]
)


@router.delete(
    "/{group_id}/leave"
)
def leave_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = (
        db.query(Group)
        .filter(Group.id == group_id)
        .first()
    )

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

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
            status_code=404,
            detail="You are not a member of this group"
        )

    if membership.role == "admin":
        admin_count = (
            db.query(GroupMember)
            .filter(
                GroupMember.group_id == group_id,
                GroupMember.role == "admin"
            )
            .count()
        )

        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "You are the only admin. "
                    "Assign another admin before leaving the group."
                )
            )

    db.delete(membership)
    db.commit()

    return {
        "message": "You left the group successfully",
        "group_id": group_id
    }