import uuid
from sqlalchemy import CHAR, Column, String, DateTime, func
from configs.database import Base


def generate_uuid():
    return uuid.uuid4().bytes

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
