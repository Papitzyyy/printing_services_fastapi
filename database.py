from sqlmodel import SQLModel, create_engine, Session

# simple SQLite engine for conceptual model
DATABASE_URL = "sqlite:///./papiprints.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
