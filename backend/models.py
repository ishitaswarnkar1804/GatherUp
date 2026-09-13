from sqlalchemy import Column, Integer, String, Text, Date, Time, TIMESTAMP, Numeric, Boolean, text
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    invite_code = Column(String(20), unique=True, nullable=False, index=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    role = Column(String(30), nullable=False, default="member")
    joined_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class GroupMessage(Base):
    __tablename__ = "group_messages"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class EventParticipant(Base):
    __tablename__ = "event_participants"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="going")
    joined_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    question = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class PollOption(Base):
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, nullable=False)
    option_text = Column(String(255), nullable=False)


class PollVote(Base):
    __tablename__ = "poll_votes"

    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, nullable=False)
    option_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    voted_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=True)
    paid_by = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    paid = Column(Boolean, default=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=True)
    assigned_to = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default="pending")
    due_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class FoodOrder(Base):
    __tablename__ = "food_orders"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=True)
    uploaded_by = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=True, default="general")
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    token_hash = Column(String(64), nullable=True, unique=True)
    expires_at = Column(TIMESTAMP, nullable=True)
    verified_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
