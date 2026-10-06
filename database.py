from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date
)

from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASE_URL = "sqlite:///studplanner.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


# ==========================================
# STUDY SESSION TABLE
# ==========================================

class StudySession(Base):

    __tablename__ = "study_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subject = Column(
        String,
        nullable=False
    )

    topic = Column(
        String,
        nullable=False
    )

    study_date = Column(
        Date,
        default=date.today
    )

    start_time = Column(
        String,
        nullable=False
    )

    end_time = Column(
        String,
        nullable=False
    )

    duration = Column(
        Float,
        default=1.0
    )

    completed = Column(
        Boolean,
        default=False
    )


# ==========================================
# SUBJECT TABLE
# ==========================================

class Subject(Base):

    __tablename__ = "subjects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    difficulty = Column(
        String,
        default="Medium"
    )

    target_hours = Column(
        Float,
        default=1.0
    )

    completed_hours = Column(
        Float,
        default=0.0
    )


# ==========================================
# DATABASE FUNCTIONS
# ==========================================

def init_db():

    Base.metadata.create_all(
        bind=engine
    )


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )


def get_db():

    return SessionLocal()
