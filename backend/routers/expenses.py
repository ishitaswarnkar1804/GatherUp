from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import (
    Expense,
    ExpenseSplit,
    Event,
    GroupMember,
    User
)
from backend.schemas import (
    CreateExpenseRequest,
    ExpenseResponse,
    ExpenseSplitResponse,
    MarkExpensePaidRequest
)
from backend.security import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["Expenses"]
)


def check_group_membership(
    db: Session,
    group_id: int,
    user_id: int
):
    membership = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )

    return membership


def get_expense_for_group(
    db: Session,
    group_id: int,
    expense_id: int
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.group_id == group_id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense


def build_expense_response(
    db: Session,
    expense: Expense
):
    payer = (
        db.query(User)
        .filter(User.id == expense.paid_by)
        .first()
    )

    splits = (
        db.query(ExpenseSplit, User)
        .join(
            User,
            User.id == ExpenseSplit.user_id
        )
        .filter(
            ExpenseSplit.expense_id == expense.id
        )
        .order_by(ExpenseSplit.id.asc())
        .all()
    )

    split_results = []

    for split, user in splits:
        split_results.append(
            ExpenseSplitResponse(
                id=split.id,
                expense_id=split.expense_id,
                user_id=split.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                amount=split.amount,
                paid=split.paid
            )
        )

    return ExpenseResponse(
        id=expense.id,
        group_id=expense.group_id,
        event_id=expense.event_id,
        paid_by=expense.paid_by,
        paid_by_first_name=payer.first_name,
        paid_by_last_name=payer.last_name,
        title=expense.title,
        amount=expense.amount,
        expense_date=expense.expense_date,
        description=expense.description,
        created_at=expense.created_at,
        splits=split_results
    )


@router.post(
    "/{group_id}/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(
    group_id: int,
    expense_data: CreateExpenseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    if expense_data.event_id is not None:
        event = (
            db.query(Event)
            .filter(
                Event.id == expense_data.event_id,
                Event.group_id == group_id
            )
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found in this group"
            )

    member_ids = {
        membership.user_id
        for membership in (
            db.query(GroupMember)
            .filter(
                GroupMember.group_id == group_id
            )
            .all()
        )
    }

    split_user_ids = [
        split.user_id
        for split in expense_data.splits
    ]

    if len(split_user_ids) != len(set(split_user_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user cannot appear more than once in an expense split"
        )

    invalid_users = [
        user_id
        for user_id in split_user_ids
        if user_id not in member_ids
    ]

    if invalid_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All expense split users must be members of this group"
        )

    split_total = sum(
        (
            split.amount
            for split in expense_data.splits
        ),
        Decimal("0.00")
    )

    expense_total = expense_data.amount

    if split_total != expense_total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Expense amount is {expense_total}, "
                f"but the split total is {split_total}"
            )
        )

    new_expense = Expense(
        group_id=group_id,
        event_id=expense_data.event_id,
        paid_by=current_user.id,
        title=expense_data.title.strip(),
        amount=expense_total,
        expense_date=expense_data.expense_date,
        description=(
            expense_data.description.strip()
            if expense_data.description
            else None
        )
    )

    db.add(new_expense)
    db.flush()

    for split_data in expense_data.splits:
        expense_split = ExpenseSplit(
            expense_id=new_expense.id,
            user_id=split_data.user_id,
            amount=split_data.amount,
            paid=split_data.user_id == current_user.id
        )

        db.add(expense_split)

    db.commit()
    db.refresh(new_expense)

    return build_expense_response(
        db,
        new_expense
    )


@router.get(
    "/{group_id}/expenses",
    response_model=list[ExpenseResponse]
)
def get_group_expenses(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.group_id == group_id
        )
        .order_by(
            Expense.expense_date.desc(),
            Expense.id.desc()
        )
        .all()
    )

    return [
        build_expense_response(
            db,
            expense
        )
        for expense in expenses
    ]


@router.get(
    "/{group_id}/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    group_id: int,
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    expense = get_expense_for_group(
        db,
        group_id,
        expense_id
    )

    return build_expense_response(
        db,
        expense
    )


@router.patch(
    "/{group_id}/expenses/{expense_id}/splits/{user_id}",
    response_model=ExpenseSplitResponse
)
def update_expense_split_paid_status(
    group_id: int,
    expense_id: int,
    user_id: int,
    payment_data: MarkExpensePaidRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = check_group_membership(
        db,
        group_id,
        current_user.id
    )

    expense = get_expense_for_group(
        db,
        group_id,
        expense_id
    )

    if user_id != current_user.id and membership.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own expense share"
        )

    expense_split = (
        db.query(ExpenseSplit)
        .filter(
            ExpenseSplit.expense_id == expense.id,
            ExpenseSplit.user_id == user_id
        )
        .first()
    )

    if not expense_split:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense split not found"
        )

    expense_split.paid = payment_data.paid

    db.commit()
    db.refresh(expense_split)

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    return ExpenseSplitResponse(
        id=expense_split.id,
        expense_id=expense_split.expense_id,
        user_id=expense_split.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        amount=expense_split.amount,
        paid=expense_split.paid
    )