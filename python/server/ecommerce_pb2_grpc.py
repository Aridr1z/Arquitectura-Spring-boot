# Generated manually to avoid plugin dependency
import grpc

import server.ecommerce_pb2 as ecommerce__pb2


class GreeterStub(object):
    def __init__(self, channel):
        self.SayHello = channel.unary_unary(
            '/ecommerce.Greeter/SayHello',
            request_serializer=ecommerce__pb2.HelloRequest.SerializeToString,
            response_deserializer=ecommerce__pb2.HelloReply.FromString,
        )


class GreeterServicer(object):
    def SayHello(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GreeterServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'SayHello': grpc.unary_unary_rpc_method_handler(
            servicer.SayHello,
            request_deserializer=ecommerce__pb2.HelloRequest.FromString,
            response_serializer=ecommerce__pb2.HelloReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'ecommerce.Greeter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


class ProductServiceStub(object):
    def __init__(self, channel):
        self.CreateProduct = channel.unary_unary(
            '/ecommerce.ProductService/CreateProduct',
            request_serializer=ecommerce__pb2.CreateProductRequest.SerializeToString,
            response_deserializer=ecommerce__pb2.ProductResponse.FromString,
        )
        self.GetProductById = channel.unary_unary(
            '/ecommerce.ProductService/GetProductById',
            request_serializer=ecommerce__pb2.GetProductRequest.SerializeToString,
            response_deserializer=ecommerce__pb2.ProductResponse.FromString,
        )
        self.UpdateProduct = channel.unary_unary(
            '/ecommerce.ProductService/UpdateProduct',
            request_serializer=ecommerce__pb2.UpdateProductRequest.SerializeToString,
            response_deserializer=ecommerce__pb2.ProductResponse.FromString,
        )
        self.DeleteProduct = channel.unary_unary(
            '/ecommerce.ProductService/DeleteProduct',
            request_serializer=ecommerce__pb2.DeleteProductRequest.SerializeToString,
            response_deserializer=ecommerce__pb2.DeleteProductResponse.FromString,
        )
        self.ListProducts = channel.unary_unary(
            '/ecommerce.ProductService/ListProducts',
            request_serializer=ecommerce__pb2.ListProductsRequest.SerializeToString,
            response_deserializer=ecommerce__pb2.ListProductsResponse.FromString,
        )


class ProductServiceServicer(object):
    def CreateProduct(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProductById(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProduct(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProduct(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProducts(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProductServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'CreateProduct': grpc.unary_unary_rpc_method_handler(
            servicer.CreateProduct,
            request_deserializer=ecommerce__pb2.CreateProductRequest.FromString,
            response_serializer=ecommerce__pb2.ProductResponse.SerializeToString,
        ),
        'GetProductById': grpc.unary_unary_rpc_method_handler(
            servicer.GetProductById,
            request_deserializer=ecommerce__pb2.GetProductRequest.FromString,
            response_serializer=ecommerce__pb2.ProductResponse.SerializeToString,
        ),
        'UpdateProduct': grpc.unary_unary_rpc_method_handler(
            servicer.UpdateProduct,
            request_deserializer=ecommerce__pb2.UpdateProductRequest.FromString,
            response_serializer=ecommerce__pb2.ProductResponse.SerializeToString,
        ),
        'DeleteProduct': grpc.unary_unary_rpc_method_handler(
            servicer.DeleteProduct,
            request_deserializer=ecommerce__pb2.DeleteProductRequest.FromString,
            response_serializer=ecommerce__pb2.DeleteProductResponse.SerializeToString,
        ),
        'ListProducts': grpc.unary_unary_rpc_method_handler(
            servicer.ListProducts,
            request_deserializer=ecommerce__pb2.ListProductsRequest.FromString,
            response_serializer=ecommerce__pb2.ListProductsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'ecommerce.ProductService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of the pattern generated by protoc; kept for compatibility
class ProductService(object):
    @staticmethod
    def CreateProduct(request, target, options=(), channel_credentials=None, call_credentials=None,
                      insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ecommerce.ProductService/CreateProduct',
                                             ecommerce__pb2.CreateProductRequest.SerializeToString,
                                             ecommerce__pb2.ProductResponse.FromString,
                                             options, channel_credentials, insecure, call_credentials,
                                             compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProductById(request, target, options=(), channel_credentials=None, call_credentials=None,
                       insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ecommerce.ProductService/GetProductById',
                                             ecommerce__pb2.GetProductRequest.SerializeToString,
                                             ecommerce__pb2.ProductResponse.FromString,
                                             options, channel_credentials, insecure, call_credentials,
                                             compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateProduct(request, target, options=(), channel_credentials=None, call_credentials=None,
                      insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ecommerce.ProductService/UpdateProduct',
                                             ecommerce__pb2.UpdateProductRequest.SerializeToString,
                                             ecommerce__pb2.ProductResponse.FromString,
                                             options, channel_credentials, insecure, call_credentials,
                                             compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteProduct(request, target, options=(), channel_credentials=None, call_credentials=None,
                      insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ecommerce.ProductService/DeleteProduct',
                                             ecommerce__pb2.DeleteProductRequest.SerializeToString,
                                             ecommerce__pb2.DeleteProductResponse.FromString,
                                             options, channel_credentials, insecure, call_credentials,
                                             compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListProducts(request, target, options=(), channel_credentials=None, call_credentials=None,
                     insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ecommerce.ProductService/ListProducts',
                                             ecommerce__pb2.ListProductsRequest.SerializeToString,
                                             ecommerce__pb2.ListProductsResponse.FromString,
                                             options, channel_credentials, insecure, call_credentials,
                                             compression, wait_for_ready, timeout, metadata)
