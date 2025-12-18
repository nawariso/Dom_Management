from typing import Generic, Iterable, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from backend.app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class Repository(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def add(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        return instance

    def get(self, object_id: int) -> Optional[ModelType]:
        return self.session.get(self.model, object_id)

    def list(self) -> List[ModelType]:
        return list(self.session.query(self.model).all())

    def delete(self, instance: ModelType) -> None:
        self.session.delete(instance)
