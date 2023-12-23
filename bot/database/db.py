from typing import TypedDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Quote
from math import ceil


def create_session_maker(db_uri: str) -> sessionmaker:
    if not db_uri:
        raise ValueError("db_uri not provided")

    # check_same_thread needed for sqlite
    engine = create_engine(db_uri, connect_args={"check_same_thread": False})
    return sessionmaker(engine, autocommit=False, autoflush=False)


class QuotesResult(TypedDict):
    total: int
    pages: int
    quotes: list[Quote] | None


class Database:
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def add_quote(
        self, session: Session, author: str, text: str, submitter_id: str
    ) -> Quote:
        quote = Quote(text=text, author=author, submitted_by=submitter_id)
        session.add(quote)
        session.commit()
        session.refresh(quote)
        return quote

    def get_quote_by_text(self, session: Session, text: str) -> Quote | None:
        return session.query(Quote).filter(Quote.text == text).first()

    def get_quotes(
        self,
        session: Session,
        user_id: str,
        page: int = 0,
        limit: int = 25,
        only_unapproved: bool = True,
    ) ->  QuotesResult:
        if only_unapproved:
            query = session.query(Quote).filter(
                Quote.submitted_by == user_id and Quote.approved == False
            )
        else:
            query = session.query(Quote).filter(Quote.submitted_by == user_id)

        total = query.count()
        pages = ceil((total / limit) - 1)
        query = query.limit(limit).offset(page * limit)
        quotes = list(query)
        if len(quotes) == 0:
            quotes = None
        
        return {
            "total": total,
            "pages": pages,
            "quotes": quotes,
        }
