import json
from abc import ABC
from typing import List, Optional, Type, TypeVar

from app.internal.firebase import db
from google.cloud.firestore import Transaction
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseDAO(ABC):

    model: Type[T] = None

    def __init__(self, collection_path: str):
        self.collection_reference = db.collection(collection_path)
        if not self.model or not issubclass(self.model, BaseModel):
            raise AttributeError("Subclass DAOs must define a pydantic model.")

    def _model_dump_json(self, data: T, **kwargs) -> dict:
        return json.loads(data.model_dump_json(**kwargs))

    async def get(self, id: str, batch: Optional[Transaction] = None) -> Optional[T]:
        doc = await self.collection_reference.document(id).get(transaction=batch)
        if doc.exists:
            return self.model(**doc.to_dict())
        return None

    # def get_all(self):
    #     return self.model.get_all()

    async def create(
        self,
        payload: T,
        id: Optional[str] = None,
        batch: Optional[Transaction] = None,
    ):
        doc = self.collection_reference.document(id or getattr(payload, "id", None))
        data = self._model_dump_json(payload)
        if isinstance(batch, Transaction):
            await batch.set(doc, data)
        else:
            await doc.set(data)

    async def batch_create(self, items: List[T]):
        batch = db.batch()
        count = 1
        firestore_batch_limit = 500

        for item in items:
            await self.create(item, batch=batch)
            count += 1
            if count % firestore_batch_limit == 0:
                await batch.commit()
        await batch.commit()

    # def update(self, **kwargs):
    #     return self.model.update(**kwargs)

    # def delete(self, **kwargs):
    #     return self.model.delete(**kwargs)
