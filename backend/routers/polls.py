from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import (
    Poll,
    PollOption,
    PollVote,
    GroupMember,
    User
)
from backend.schemas import (
    CreatePollRequest,
    PollResponse,
    PollOptionResponse,
    VotePollRequest,
    PollResultResponse,
    PollOptionResult
)
from backend.security import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["Polls"]
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


def get_poll_for_group(
    db: Session,
    group_id: int,
    poll_id: int
):
    poll = (
        db.query(Poll)
        .filter(
            Poll.id == poll_id,
            Poll.group_id == group_id
        )
        .first()
    )

    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found"
        )

    return poll


@router.post(
    "/{group_id}/polls",
    response_model=PollResponse,
    status_code=status.HTTP_201_CREATED
)
def create_poll(
    group_id: int,
    poll_data: CreatePollRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    question = poll_data.question.strip()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll question cannot be empty"
        )

    cleaned_options = []

    for option in poll_data.options:
        cleaned_option = option.strip()

        if not cleaned_option:
            continue

        if cleaned_option.lower() not in [
            existing.lower()
            for existing in cleaned_options
        ]:
            cleaned_options.append(cleaned_option)

    if len(cleaned_options) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A poll must have at least two different options"
        )

    if len(cleaned_options) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A poll can have a maximum of ten options"
        )

    new_poll = Poll(
        group_id=group_id,
        created_by=current_user.id,
        question=question
    )

    db.add(new_poll)
    db.flush()

    for option_text in cleaned_options:
        poll_option = PollOption(
            poll_id=new_poll.id,
            option_text=option_text
        )

        db.add(poll_option)

    db.commit()
    db.refresh(new_poll)

    options = (
        db.query(PollOption)
        .filter(
            PollOption.poll_id == new_poll.id
        )
        .order_by(
            PollOption.id.asc()
        )
        .all()
    )

    return {
        "id": new_poll.id,
        "group_id": new_poll.group_id,
        "created_by": new_poll.created_by,
        "question": new_poll.question,
        "created_at": new_poll.created_at,
        "options": options
    }


@router.get(
    "/{group_id}/polls",
    response_model=list[PollResponse]
)
def get_group_polls(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    polls = (
        db.query(Poll)
        .filter(
            Poll.group_id == group_id
        )
        .order_by(
            Poll.created_at.desc()
        )
        .all()
    )

    results = []

    for poll in polls:
        options = (
            db.query(PollOption)
            .filter(
                PollOption.poll_id == poll.id
            )
            .order_by(
                PollOption.id.asc()
            )
            .all()
        )

        results.append(
            {
                "id": poll.id,
                "group_id": poll.group_id,
                "created_by": poll.created_by,
                "question": poll.question,
                "created_at": poll.created_at,
                "options": options
            }
        )

    return results


@router.get(
    "/{group_id}/polls/{poll_id}",
    response_model=PollResponse
)
def get_poll(
    group_id: int,
    poll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    poll = get_poll_for_group(
        db,
        group_id,
        poll_id
    )

    options = (
        db.query(PollOption)
        .filter(
            PollOption.poll_id == poll.id
        )
        .order_by(
            PollOption.id.asc()
        )
        .all()
    )

    return {
        "id": poll.id,
        "group_id": poll.group_id,
        "created_by": poll.created_by,
        "question": poll.question,
        "created_at": poll.created_at,
        "options": options
    }


@router.post(
    "/{group_id}/polls/{poll_id}/vote",
    response_model=PollResultResponse
)
def vote_on_poll(
    group_id: int,
    poll_id: int,
    vote_data: VotePollRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    poll = get_poll_for_group(
        db,
        group_id,
        poll_id
    )

    option = (
        db.query(PollOption)
        .filter(
            PollOption.id == vote_data.option_id,
            PollOption.poll_id == poll.id
        )
        .first()
    )

    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll option not found"
        )

    existing_vote = (
        db.query(PollVote)
        .filter(
            PollVote.poll_id == poll.id,
            PollVote.user_id == current_user.id
        )
        .first()
    )

    if existing_vote:
        existing_vote.option_id = option.id
    else:
        new_vote = PollVote(
            poll_id=poll.id,
            option_id=option.id,
            user_id=current_user.id
        )

        db.add(new_vote)

    db.commit()

    return build_poll_results(
        db,
        poll,
        current_user.id
    )


@router.get(
    "/{group_id}/polls/{poll_id}/results",
    response_model=PollResultResponse
)
def get_poll_results(
    group_id: int,
    poll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_group_membership(
        db,
        group_id,
        current_user.id
    )

    poll = get_poll_for_group(
        db,
        group_id,
        poll_id
    )

    return build_poll_results(
        db,
        poll,
        current_user.id
    )


def build_poll_results(
    db: Session,
    poll: Poll,
    user_id: int
):
    options = (
        db.query(PollOption)
        .filter(
            PollOption.poll_id == poll.id
        )
        .order_by(
            PollOption.id.asc()
        )
        .all()
    )

    option_results = []

    total_votes = (
        db.query(PollVote)
        .filter(
            PollVote.poll_id == poll.id
        )
        .count()
    )

    for option in options:
        vote_count = (
            db.query(PollVote)
            .filter(
                PollVote.poll_id == poll.id,
                PollVote.option_id == option.id
            )
            .count()
        )

        option_results.append(
            PollOptionResult(
                id=option.id,
                option_text=option.option_text,
                vote_count=vote_count
            )
        )

    user_vote_record = (
        db.query(PollVote)
        .filter(
            PollVote.poll_id == poll.id,
            PollVote.user_id == user_id
        )
        .first()
    )

    user_vote = None

    if user_vote_record:
        user_vote = user_vote_record.option_id

    return PollResultResponse(
        id=poll.id,
        group_id=poll.group_id,
        created_by=poll.created_by,
        question=poll.question,
        created_at=poll.created_at,
        total_votes=total_votes,
        user_vote=user_vote,
        options=option_results
    )