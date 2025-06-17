from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class ORMSessionManager:
    """
    Manages SQLAlchemy ORM sessions using a context manager pattern.

    Provides reusable access to scoped sessions for database transactions.
    """

    def __init__(self, engine):
        """
        Initializes the session manager with a SQLAlchemy engine.

        Args:
            engine (sqlalchemy.engine.Engine): SQLAlchemy engine used for session binding.
        """

        self.session_factory = sessionmaker(bind=engine)

    @property
    def session(self):
        """
        Provides a new SQLAlchemy session from the session factory.

        Returns:
            sqlalchemy.orm.Session: A new session instance.
        """

        return self.session_factory()

    @contextmanager
    def session_scope(self):
        """
        Provides a transactional scope around a series of operations.

        Ensures proper commit, rollback, and closure of the session context.

        Yields:
            sqlalchemy.orm.Session: A session object within the managed scope.
        """

        session = self.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Session rolled back: {e} ")
        finally:
            session.close()
