from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import current_timestamp
from random_quiz.db import DeclarativeBase


class BaseTable(DeclarativeBase):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    dt_created = Column(
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        doc="Date and time of create (type TIMESTAMP)",
    )
    dt_updated = Column(
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        onupdate=current_timestamp(),
        nullable=False,
        doc="Date and time of last update (type TIMESTAMP)",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name)
                   for column in self.__table__.columns}
        return (f'<{self.__tablename__}: ' +
                ", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))
                + '>')
