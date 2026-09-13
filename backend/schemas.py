from datetime import date, time, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str




class EmailOnlyRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    email_verified: bool = False

    class Config:
        from_attributes = True


class CreateGroupRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None


class GroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    invite_code: str
    created_by: int

    class Config:
        from_attributes = True


class JoinGroupRequest(BaseModel):
    invite_code: str = Field(min_length=1, max_length=20)


class GroupMemberResponse(BaseModel):
    id: Optional[int] = None
    user_id: int
    role: str
    first_name: str
    last_name: str
    email: EmailStr

class CreateEventRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: date
    event_time: Optional[time] = None
    location: Optional[str] = Field(default=None, max_length=255)


class EventResponse(BaseModel):
    id: int
    group_id: int
    created_by: int
    title: str
    description: Optional[str]
    event_date: date
    event_time: Optional[time]
    location: Optional[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EventParticipantResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    status: str

    class Config:
        from_attributes = True


class EventParticipationRequest(BaseModel):
    status: str


class CreatePollRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    options: List[str] = Field(min_length=2)


class PollOptionResponse(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True


class PollResponse(BaseModel):
    id: int
    group_id: int
    created_by: int
    question: str
    created_at: Optional[datetime] = None
    options: List[PollOptionResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class VotePollRequest(BaseModel):
    option_id: int


class PollOptionResult(BaseModel):
    id: int
    option_text: str
    vote_count: int


class PollResultResponse(BaseModel):
    id: int
    group_id: int
    created_by: int
    question: str
    created_at: Optional[datetime] = None
    total_votes: int
    user_vote: Optional[int] = None
    options: List[PollOptionResult]


class ExpenseSplitRequest(BaseModel):
    user_id: int
    amount: Decimal = Field(gt=0)


class CreateExpenseRequest(BaseModel):
    event_id: Optional[int] = None
    paid_by: Optional[int] = None
    title: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    expense_date: date
    description: Optional[str] = None
    splits: List[ExpenseSplitRequest] = Field(min_length=1)


class ExpenseSplitResponse(BaseModel):
    id: int
    expense_id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    amount: Decimal
    paid: bool

    class Config:
        from_attributes = True


class ExpenseResponse(BaseModel):
    id: int
    group_id: int
    event_id: Optional[int]
    paid_by: int
    paid_by_first_name: str = ""
    paid_by_last_name: str = ""
    title: str
    amount: Decimal
    expense_date: date
    description: Optional[str]
    created_at: Optional[datetime] = None
    splits: List[ExpenseSplitResponse] = []

    class Config:
        from_attributes = True


class MarkExpensePaidRequest(BaseModel):
    paid: bool


class CreateTaskRequest(BaseModel):
    event_id: Optional[int] = None
    assigned_to: Optional[int] = None
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[date] = None


class UpdateTaskStatusRequest(BaseModel):
    status: str


class UpdateTaskRequest(BaseModel):
    status: str


class TaskResponse(BaseModel):
    id: int
    group_id: int
    event_id: Optional[int]
    assigned_to: Optional[int]
    assigned_to_first_name: Optional[str] = None
    assigned_to_last_name: Optional[str] = None
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[date]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateFoodOrderRequest(BaseModel):
    event_id: Optional[int] = None
    item_name: str = Field(min_length=1, max_length=255)
    quantity: int = Field(default=1, ge=1, le=100)
    price: Decimal = Field(ge=0)


class UpdateFoodOrderStatusRequest(BaseModel):
    status: str


class UpdateFoodOrderRequest(BaseModel):
    status: str


class FoodOrderResponse(BaseModel):
    id: int
    group_id: int
    event_id: Optional[int]
    user_id: int
    ordered_by: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    item_name: str
    quantity: int
    price: Decimal
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateGalleryItemRequest(BaseModel):
    event_id: Optional[int] = None
    image_url: str = Field(min_length=1, max_length=500)
    caption: Optional[str] = Field(default=None, max_length=255)


class CreateGalleryRequest(BaseModel):
    event_id: Optional[int] = None
    image_url: str = Field(min_length=1, max_length=500)
    caption: Optional[str] = Field(default=None, max_length=255)


class GalleryResponse(BaseModel):
    id: int
    group_id: int
    event_id: Optional[int]
    uploaded_by: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: str
    caption: Optional[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MarkNotificationRequest(BaseModel):
    is_read: bool


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: Optional[str]
    is_read: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True