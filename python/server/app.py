import logging
import os
from concurrent import futures
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

import grpc

from db.connection import get_database
from db.product_repository import ProductRepository
from server import ecommerce_pb2, ecommerce_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def document_to_product_message(document: Dict[str, Any]) -> ecommerce_pb2.Product:
    details = document.get("details") or {}
    created_at = document.get("createdAt") or datetime.utcnow()
    created_at_iso = created_at.isoformat()

    return ecommerce_pb2.Product(
        id=document.get("_id", ""),
        seller_id=document.get("sellerId", ""),
        type=document.get("type", ""),
        title=document.get("title", ""),
        price=float(document.get("price", 0)),
        details={k: str(v) for k, v in details.items()},
        created_at=created_at_iso,
    )


def product_request_to_document(product: ecommerce_pb2.Product, include_id: bool = True) -> Dict[str, Any]:
    created_at = datetime.fromisoformat(product.created_at) if product.created_at else None
    payload: Dict[str, Any] = {
        "sellerId": product.seller_id,
        "type": product.type,
        "title": product.title,
        "price": product.price,
        "details": dict(product.details),
    }
    if include_id:
        payload["_id"] = product.id or str(uuid4())
        payload["createdAt"] = created_at or datetime.utcnow()
    elif created_at:
        payload["createdAt"] = created_at
    return payload


class GreeterService(ecommerce_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        name = request.name or "World"
        message = f"Hello, {name}!"
        return ecommerce_pb2.HelloReply(message=message)


class ProductService(ecommerce_pb2_grpc.ProductServiceServicer):
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def CreateProduct(self, request, context):
        product = request.product
        if not product.title or not product.seller_id or not product.type:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "title, seller_id and type are required")

        document = product_request_to_document(product)
        try:
            created = self.repository.create(document)
        except ValueError:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "Product with the same id already exists")

        return ecommerce_pb2.ProductResponse(product=document_to_product_message(created))

    def GetProductById(self, request, context):
        if not request.id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id is required")

        document = self.repository.get_by_id(request.id)
        if not document:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

        return ecommerce_pb2.ProductResponse(product=document_to_product_message(document))

    def UpdateProduct(self, request, context):
        product = request.product
        if not product.id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id is required")

        document = product_request_to_document(product, include_id=False)
        updated = self.repository.update(product.id, document)
        if not updated:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

        return ecommerce_pb2.ProductResponse(product=document_to_product_message(updated))

    def DeleteProduct(self, request, context):
        if not request.id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id is required")

        deleted = self.repository.delete(request.id)
        if not deleted:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

        return ecommerce_pb2.DeleteProductResponse(deleted=True)

    def ListProducts(self, request, context):
        page = request.page if request.page > 0 else 1
        page_size = request.page_size if request.page_size > 0 else 20

        items, total = self.repository.list_products(page, page_size)
        products = [document_to_product_message(doc) for doc in items]

        return ecommerce_pb2.ListProductsResponse(
            products=products,
            page=page,
            page_size=page_size,
            total=total,
        )


def serve():
    grpc_port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    try:
        database = get_database()
        repository = ProductRepository(database.get_collection("products"))
        logger.info("Connected to MongoDB at %s:%s", os.getenv("DB_HOST", "db"), os.getenv("DB_PORT", "27017"))
    except Exception as exc:  # pragma: no cover - defensive logging for runtime environments
        logger.exception("Failed to initialize database connection: %s", exc)
        raise

    ecommerce_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    ecommerce_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(repository), server)

    server.add_insecure_port(f"0.0.0.0:{grpc_port}")
    logger.info("gRPC server listening on port %s", grpc_port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    try:
        serve()
    except Exception:
        logger.exception("gRPC server terminated due to an unrecoverable error")
        raise
