from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Event, Gallery, GroupMember, User
from backend.schemas import (
    CreateGalleryItemRequest,
    GalleryResponse
)
from backend.security import get_current_user
from backend.routers._helpers import (
    create_notification,
    require_member
)


router = APIRouter(
    prefix="/groups",
    tags=["Gallery"]
)


def build_gallery_response(
    item: Gallery,
    user: User
):
    return {
        "id": item.id,
        "group_id": item.group_id,
        "event_id": item.event_id,
        "uploaded_by": item.uploaded_by,
        "first_name": user.first_name if user else None,
        "last_name": user.last_name if user else None,
        "image_url": item.image_url,
        "caption": item.caption,
        "created_at": item.created_at
    }


@router.get(
    "/{group_id}/gallery",
    response_model=list[GalleryResponse]
)
def get_gallery(
    group_id: int,
    event_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(
        group_id,
        db,
        current_user
    )

    query = (
        db.query(Gallery, User)
        .join(
            User,
            User.id == Gallery.uploaded_by
        )
        .filter(
            Gallery.group_id == group_id
        )
    )

    if event_id is not None:
        query = query.filter(
            Gallery.event_id == event_id
        )

    rows = (
        query
        .order_by(
            Gallery.created_at.desc()
        )
        .all()
    )

    return [
        build_gallery_response(
            item,
            user
        )
        for item, user in rows
    ]


@router.post(
    "/{group_id}/gallery",
    response_model=GalleryResponse,
    status_code=status.HTTP_201_CREATED
)
def add_gallery_item(
    group_id: int,
    data: CreateGalleryItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(
        group_id,
        db,
        current_user
    )

    if data.event_id is not None:
        event = (
            db.query(Event)
            .filter(
                Event.id == data.event_id,
                Event.group_id == group_id
            )
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=400,
                detail="Event does not belong to this group"
            )

    image_url = data.image_url.strip()

    if not (
        image_url.startswith("http://")
        or image_url.startswith("https://")
    ):
        raise HTTPException(
            status_code=400,
            detail="Image URL must start with http:// or https://"
        )

    item = Gallery(
        group_id=group_id,
        event_id=data.event_id,
        uploaded_by=current_user.id,
        image_url=image_url,
        caption=(
            data.caption.strip()
            if data.caption
            else None
        )
    )

    db.add(item)

    members = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id
        )
        .all()
    )

    for member in members:
        if member.user_id != current_user.id:
            create_notification(
                db=db,
                user_id=member.user_id,
                group_id=group_id,
                notification_type="gallery",
                message=(
                    f"{current_user.first_name} "
                    f"added a new gallery item"
                )
            )

    db.commit()
    db.refresh(item)

    return build_gallery_response(
        item,
        current_user
    )


@router.delete(
    "/{group_id}/gallery/{item_id}"
)
def delete_gallery_item(
    group_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = require_member(
        group_id,
        db,
        current_user
    )

    item = (
        db.query(Gallery)
        .filter(
            Gallery.id == item_id,
            Gallery.group_id == group_id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Gallery item not found"
        )

    if (
        item.uploaded_by != current_user.id
        and membership.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Only the uploader or group admin "
                "can delete this item"
            )
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Gallery item deleted successfully"
    }