from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Event, FoodOrder, GroupMember, User
from backend.schemas import (
    CreateFoodOrderRequest,
    FoodOrderResponse,
    UpdateFoodOrderStatusRequest
)
from backend.security import get_current_user
from backend.routers._helpers import (
    create_notification,
    require_member
)


router = APIRouter(
    prefix="/groups",
    tags=["Food Orders"]
)

ALLOWED_STATUSES = {
    "pending",
    "confirmed",
    "cancelled"
}


def build_food_response(
    order: FoodOrder,
    user: User
):
    return {
        "id": order.id,
        "group_id": order.group_id,
        "event_id": order.event_id,
        "user_id": order.user_id,
        "ordered_by": order.user_id,
        "first_name": user.first_name if user else None,
        "last_name": user.last_name if user else None,
        "item_name": order.item_name,
        "quantity": order.quantity,
        "price": order.price,
        "status": order.status,
        "created_at": order.created_at
    }


@router.get(
    "/{group_id}/food-orders",
    response_model=list[FoodOrderResponse]
)
def get_food_orders(
    group_id: int,
    event_id: int | None = None,
    order_status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(group_id, db, current_user)

    query = (
        db.query(FoodOrder, User)
        .join(User, User.id == FoodOrder.user_id)
        .filter(FoodOrder.group_id == group_id)
    )

    if event_id is not None:
        query = query.filter(FoodOrder.event_id == event_id)

    if order_status is not None:
        if order_status not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail="Invalid food order status"
            )

        query = query.filter(
            FoodOrder.status == order_status
        )

    rows = (
        query
        .order_by(FoodOrder.created_at.desc())
        .all()
    )

    return [
        build_food_response(order, user)
        for order, user in rows
    ]


@router.post(
    "/{group_id}/food-orders",
    response_model=FoodOrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_food_order(
    group_id: int,
    data: CreateFoodOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(group_id, db, current_user)

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

    order = FoodOrder(
        group_id=group_id,
        event_id=data.event_id,
        user_id=current_user.id,
        item_name=data.item_name.strip(),
        quantity=data.quantity,
        price=data.price,
        status="pending"
    )

    db.add(order)

    members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    for member in members:
        if member.user_id != current_user.id:
            create_notification(
                db,
                member.user_id,
                group_id,
                "food_order",
                f"{current_user.first_name} added a food order: {order.item_name}"
            )

    db.commit()
    db.refresh(order)

    return build_food_response(order, current_user)


@router.patch(
    "/{group_id}/food-orders/{order_id}/status",
    response_model=FoodOrderResponse
)
def update_food_order_status(
    group_id: int,
    order_id: int,
    data: UpdateFoodOrderStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = require_member(
        group_id,
        db,
        current_user
    )

    new_status = data.status.lower().strip()

    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Status must be pending, confirmed, or cancelled"
        )

    order = (
        db.query(FoodOrder)
        .filter(
            FoodOrder.id == order_id,
            FoodOrder.group_id == group_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Food order not found"
        )

    if (
        order.user_id != current_user.id
        and membership.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the order owner or group admin can update this order"
        )

    order.status = new_status

    if order.user_id != current_user.id:
        create_notification(
            db,
            order.user_id,
            group_id,
            "food_status",
            f"Your food order '{order.item_name}' is now {new_status}"
        )

    db.commit()
    db.refresh(order)

    user = (
        db.query(User)
        .filter(User.id == order.user_id)
        .first()
    )

    return build_food_response(order, user)


@router.delete(
    "/{group_id}/food-orders/{order_id}"
)
def delete_food_order(
    group_id: int,
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = require_member(
        group_id,
        db,
        current_user
    )

    order = (
        db.query(FoodOrder)
        .filter(
            FoodOrder.id == order_id,
            FoodOrder.group_id == group_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Food order not found"
        )

    if (
        order.user_id != current_user.id
        and membership.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the order owner or group admin can delete this order"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Food order deleted successfully"
    }