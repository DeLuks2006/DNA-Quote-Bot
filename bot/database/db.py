from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from bot.database.models import Quote


def create_session_maker(db_uri: str) -> sessionmaker:
    if not db_uri:
        raise ValueError("db_uri not provided")

    # check_same_thread needed for sqlite
    engine = create_engine(db_uri, connect_args={"check_same_thread": False})
    return sessionmaker(engine, autocommit=False, autoflush=False)


class Database:
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def add_quote(
        self, session: Session, author: str, text: str, submitter_id: int
    ) -> Quote:
        quote = Quote(text=text, author=author, submitted_by=submitter_id)
        session.add(quote)
        session.commit()
        session.refresh(quote)
        return quote

    def get_quote_by_text(self, session: Session, text: str) -> Quote | None:
        return session.query(Quote).filter(Quote.text == text).first()

    def get_quote(self, session: Session, quote_id: int) -> Quote | None:
        return session.get(Quote, quote_id)

    def get_quotes(
        self,
        session: Session,
        user_id: str = None,
        only_unapproved: bool = True,
    ) -> list[Quote] | None:
        query = session.query(Quote)
        if only_unapproved:
            query = query.filter(Quote.approved == False)
        if user_id:
            query = query.filter(Quote.submitted_by == user_id)

        quotes = list(query)
        if len(quotes) == 0:
            quotes = None
        return quotes

    def remove_quote(self, session: Session, quote_id: int) -> None:
        quote = self.get_quote(session, quote_id)
        if quote is not None:
            session.delete(quote)
            session.commit()

    def approve_quote(self, session: Session, quote_id: int, user_id: int) -> None:
        quote = self.get_quote(session, quote_id)
        now = datetime.utcnow()
        if quote:
            quote.approved = True
            quote.approved_by = user_id
            quote.approved_at = now
            session.commit()
