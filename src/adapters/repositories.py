from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from src.adapters.database import Base


class AbstractRepository(ABC):

    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abstractmethod
    def create(self, values):
        raise NotImplementedError

    @abstractmethod
    def update(self, key: int, values: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, model: type[Base], session: Session) -> None:
        self.model = model
        self.session = session

    def list(self):
        stmt = select(self.model)
        res = self.session.scalars(stmt).all()
        return res

    def get(self, key):
        res = self.session.get(self.model, key)
        return res

    def create(self, values):
        instance = self.model(**values)
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, key: int, values):
        instance = self.session.get(self.model, key)
        for k, v in values.items():
            setattr(instance, k, v)

        self.session.commit()

        return instance

    def delete(self, key: int):
        instance = self.session.get(self.model, key)
        self.session.delete(instance)
        self.session.commit()
