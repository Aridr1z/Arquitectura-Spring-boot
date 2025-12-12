from datetime import datetime
from typing import Any, Dict, List, Tuple
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument


class ProductRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, product: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.collection.insert_one(product)
            return product
        except DuplicateKeyError as exc:
            raise ValueError("PRODUCT_ALREADY_EXISTS") from exc

    def get_by_id(self, product_id: str) -> Dict[str, Any] | None:
        return self.collection.find_one({"_id": product_id})

    def update(self, product_id: str, updates: Dict[str, Any]) -> Dict[str, Any] | None:
        updates["updatedAt"] = datetime.utcnow()
        return self.collection.find_one_and_update(
            {"_id": product_id},
            {"$set": updates},
            return_document=ReturnDocument.AFTER,
        )

    def delete(self, product_id: str) -> bool:
        result = self.collection.delete_one({"_id": product_id})
        return result.deleted_count > 0

    def list_products(self, page: int, page_size: int) -> Tuple[List[Dict[str, Any]], int]:
        skip = max(page - 1, 0) * page_size
        cursor = self.collection.find().skip(skip).limit(page_size).sort("createdAt", -1)
        items = list(cursor)
        total = self.collection.count_documents({})
        return items, total
