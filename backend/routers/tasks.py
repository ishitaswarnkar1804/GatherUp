from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Event, GroupMember, Task, User
from backend.schemas import (
    CreateTaskRequest,
    TaskResponse,
    UpdateTaskStatusRequest
)
from backend.security import get_current_user
from backend.routers._helpers import create_notification, require_member, require_admin


router = APIRouter(prefix="/groups", tags=["Tasks"])

ALLOWED_STATUSES = {
    "pending",
    "in_progress",
    "completed"
}


def build_task_response(db: Session, task: Task):
    assigned = None

    if task.assigned_to:
        assigned = (
            db.query(User)
            .filter(User.id == task.assigned_to)
            .first()
        )

    return {
        "id": task.id,
        "group_id": task.group_id,
        "event_id": task.event_id,
        "assigned_to": task.assigned_to,
        "assigned_to_first_name": (
            assigned.first_name if assigned else None
        ),
        "assigned_to_last_name": (
            assigned.last_name if assigned else None
        ),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "due_date": task.due_date,
        "created_at": task.created_at
    }


@router.get(
    "/{group_id}/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    group_id: int,
    event_id: int | None = None,
    task_status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(group_id, db, current_user)

    query = db.query(Task).filter(
        Task.group_id == group_id
    )

    if event_id is not None:
        query = query.filter(Task.event_id == event_id)

    if task_status is not None:
        if task_status not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail="Invalid task status"
            )

        query = query.filter(Task.status == task_status)

    tasks = (
        query
        .order_by(
            Task.status.asc(),
            Task.due_date.asc(),
            Task.created_at.desc()
        )
        .all()
    )

    return [
        build_task_response(db, task)
        for task in tasks
    ]


@router.post(
    "/{group_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    group_id: int,
    data: CreateTaskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(group_id, db, current_user)

    if data.assigned_to is not None:
        assigned_member = (
            db.query(GroupMember)
            .filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == data.assigned_to
            )
            .first()
        )

        if not assigned_member:
            raise HTTPException(
                status_code=400,
                detail="Assigned user is not a member of this group"
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

    task = Task(
        group_id=group_id,
        event_id=data.event_id,
        assigned_to=data.assigned_to,
        title=data.title.strip(),
        description=data.description,
        due_date=data.due_date,
        status="pending"
    )

    db.add(task)

    if data.assigned_to and data.assigned_to != current_user.id:
        create_notification(
            db,
            data.assigned_to,
            group_id,
            "task_assigned",
            f"{current_user.first_name} assigned you the task: {task.title}"
        )

    db.commit()
    db.refresh(task)

    return build_task_response(db, task)


@router.patch(
    "/{group_id}/tasks/{task_id}/status",
    response_model=TaskResponse
)
def update_task_status(
    group_id: int,
    task_id: int,
    data: UpdateTaskStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_member(group_id, db, current_user)

    new_status = data.status.lower().strip()

    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Status must be pending, in_progress, or completed"
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.group_id == group_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    old_status = task.status
    task.status = new_status

    if (
        new_status == "completed"
        and old_status != "completed"
        and task.assigned_to
        and task.assigned_to != current_user.id
    ):
        create_notification(
            db,
            task.assigned_to,
            group_id,
            "task_completed",
            f"{current_user.first_name} completed the task: {task.title}"
        )

    db.commit()
    db.refresh(task)

    return build_task_response(db, task)


@router.delete(
    "/{group_id}/tasks/{task_id}"
)
def delete_task(
    group_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(group_id, db, current_user)

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.group_id == group_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }