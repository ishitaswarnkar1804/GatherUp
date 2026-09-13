import secrets
import string

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Group, GroupMember, GroupMessage, User
from backend.schemas import (
    CreateGroupRequest,
    GroupResponse,
    JoinGroupRequest,
    GroupMemberResponse
)
from backend.security import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


def generate_invite_code(db: Session) -> str:
    characters = string.ascii_uppercase + string.digits

    while True:
        code = "".join(
            secrets.choice(characters)
            for _ in range(8)
        )

        existing_group = db.query(Group).filter(
            Group.invite_code == code
        ).first()

        if not existing_group:
            return code


@router.post(
    "",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED
)
def create_group(
    group_data: CreateGroupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invite_code = generate_invite_code(db)

    new_group = Group(
        name=group_data.name,
        description=group_data.description,
        invite_code=invite_code,
        created_by=current_user.id
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    group_member = GroupMember(
        group_id=new_group.id,
        user_id=current_user.id,
        role="admin"
    )

    db.add(group_member)
    db.commit()

    return new_group


@router.get(
    "",
    response_model=list[GroupResponse]
)
def get_my_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    groups = (
        db.query(Group)
        .join(
            GroupMember,
            GroupMember.group_id == Group.id
        )
        .filter(
            GroupMember.user_id == current_user.id
        )
        .all()
    )

    return groups


@router.post(
    "/join",
    response_model=GroupResponse
)
def join_group(
    group_data: JoinGroupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = db.query(Group).filter(
        Group.invite_code == group_data.invite_code.upper()
    ).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invite code"
        )

    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group.id,
        GroupMember.user_id == current_user.id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already a member of this group"
        )

    group_member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        role="member"
    )

    db.add(group_member)
    db.commit()

    return group


@router.get(
    "/{group_id}/members",
    response_model=list[GroupMemberResponse]
)
def get_group_members(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()

    if not current_membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )

    members = (
        db.query(GroupMember, User)
        .join(
            User,
            User.id == GroupMember.user_id
        )
        .filter(
            GroupMember.group_id == group_id
        )
        .all()
    )

    return [
        {
            "user_id": membership.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": membership.role
        }
        for membership, user in members
    ]
@router.get(
    "/{group_id}/messages"
)
def get_group_messages(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )

    messages = (
        db.query(GroupMessage, User)
        .join(
            User,
            User.id == GroupMessage.user_id
        )
        .filter(
            GroupMessage.group_id == group_id
        )
        .order_by(
            GroupMessage.created_at.asc()
        )
        .all()
    )

    return [
        {
            "id": message.id,
            "user_id": message.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "message": message.message,
            "created_at": message.created_at
        }
        for message, user in messages
    ]