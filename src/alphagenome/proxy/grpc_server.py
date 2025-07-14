import grpc
from concurrent import futures

# Import your generated gRPC modules here
# from src.alphagenome.protos import dna_model_service_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add your gRPC servicer to the server here
    # dna_model_service_pb2_grpc.add_DnaModelServiceServicer_to_server(YourServicer(), server)
    server.add_insecure_port('[::]:50051')
    print('gRPC server running on port 50051...')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()