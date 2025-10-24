from sqlalchemy import Column, Integer, String
from .db import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)

    def __repr__(self) -> str:  # pragma: no cover - tiny convenience
        return f"<Person id={self.id} {self.first_name} {self.last_name} {self.email}>"
