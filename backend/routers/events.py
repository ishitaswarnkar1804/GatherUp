from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import (
    Event,
    EventParticipant,
    GroupMember,
    User
)
from backend.schemas import (
    CreateEventRequest,
    EventResponse,
    EventParticipationRequest,
    EventParticipantResponse
)
from backend.security import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["Events"]
)


ALLOWED_STATUSES = {
    "going",
    "maybe",
    "not_going"
}


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


def get_event_for_group(
    db: Session,
    group_id: int,
    event_id: int
):
    event = (
        db.query(Event)
        .filter(
            Event.id == event_id,
            Event.group_id == group_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event


@router.post(
    "/{group_id}/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
def create_event(
    group_id: int,
    event_data: CreateEventRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    new_event = Event(
        group_id=group_id,
        created_by=current_user.id,
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,
        event_time=event_data.event_time,
        location=event_data.location
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    creator_participation = EventParticipant(
        event_id=new_event.id,
        user_id=current_user.id,
        status="going"
    )

    db.add(creator_participation)
    db.commit()

    return new_event


@router.get(
    "/{group_id}/events",
    response_model=list[EventResponse]
)
def get_group_events(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    events = (
        db.query(Event)
        .filter(
            Event.group_id == group_id
        )
        .order_by(
            Event.event_date.asc(),
            Event.event_time.asc()
        )
        .all()
    )

    return events


@router.get(
    "/{group_id}/events/{event_id}",
    response_model=EventResponse
)
def get_event(
    group_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    return get_event_for_group(
        db,
        group_id,
        event_id
    )


@router.delete(
    "/{group_id}/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_event(
    group_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    event = get_event_for_group(
        db,
        group_id,
        event_id
    )

    if event.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the event creator can delete this event"
        )

    participants = (
        db.query(EventParticipant)
        .filter(
            EventParticipant.event_id == event.id
        )
        .all()
    )

    for participant in participants:
        db.delete(participant)

    db.delete(event)
    db.commit()

    return None


@router.get(
    "/{group_id}/events/{event_id}/participants",
    response_model=list[EventParticipantResponse]
)
def get_event_participants(
    group_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    event = get_event_for_group(
        db,
        group_id,
        event_id
    )

    participants = (
        db.query(EventParticipant, User)
        .join(
            User,
            User.id == EventParticipant.user_id
        )
        .filter(
            EventParticipant.event_id == event.id
        )
        .order_by(
            EventParticipant.joined_at.asc()
        )
        .all()
    )

    return [
        {
            "user_id": participant.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "status": participant.status,
            "joined_at": participant.joined_at
        }
        for participant, user in participants
    ]


@router.post(
    "/{group_id}/events/{event_id}/participation",
    response_model=EventParticipantResponse
)
def join_event(
    group_id: int,
    event_id: int,
    participation_data: EventParticipationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    event = get_event_for_group(
        db,
        group_id,
        event_id
    )

    participation_status = (
        participation_data.status.lower().strip()
    )

    if participation_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be going, maybe, or not_going"
        )

    participation = (
        db.query(EventParticipant)
        .filter(
            EventParticipant.event_id == event.id,
            EventParticipant.user_id == current_user.id
        )
        .first()
    )

    if participation:
        participation.status = participation_status
    else:
        participation = EventParticipant(
            event_id=event.id,
            user_id=current_user.id,
            status=participation_status
        )
        db.add(participation)

    db.commit()
    db.refresh(participation)

    return {
        "user_id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "status": participation.status,
        "joined_at": participation.joined_at
    }


@router.delete(
    "/{group_id}/events/{event_id}/participation",
    status_code=status.HTTP_204_NO_CONTENT
)
def leave_event(
    group_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    event = get_event_for_group(
        db,
        group_id,
        event_id
    )

    if event.created_by == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The event creator cannot leave their own event"
        )

    participation = (
        db.query(EventParticipant)
        .filter(
            EventParticipant.event_id == event.id,
            EventParticipant.user_id == current_user.id
        )
        .first()
    )

    if not participation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not participating in this event"
        )

    db.delete(participation)
    db.commit()

    return None