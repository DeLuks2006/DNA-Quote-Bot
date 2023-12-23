from sqlalchemy import (
    Column,
    Integer,
    Text,
    VARCHAR,
    DateTime,
    Boolean,
    func,
    false,
)

from .base import Base


def SNOWFLAKE_ID(nullable: bool):
    return Column(VARCHAR(length=32), nullable=nullable)


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text(length=2048), nullable=False)
    author = Column(Text(length=256), nullable=False)
    submitted_by = SNOWFLAKE_ID(nullable=False)
    submitted_at = Column(DateTime, nullable=False, server_default=func.now())
    approved = Column(Boolean, nullable=False, server_default=false())
    approved_by = SNOWFLAKE_ID(nullable=True)
    approved_at = Column(DateTime, nullable=True)


class RandomQuoteChannel(Base):
    __tablename__ = "random_quote_channel"

    id = Column(Integer, primary_key=True, index=True)
    guild_id = SNOWFLAKE_ID(nullable=False)
    channel_id = SNOWFLAKE_ID(nullable=False)
