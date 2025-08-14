import uuid
from ..extensions import db
from .users import User
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, default="")
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now())

    admin_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
