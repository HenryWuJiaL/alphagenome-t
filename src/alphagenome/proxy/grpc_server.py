import grpc
from concurrent import futures
import logging

from alphagenome.protos.alphagenome.protos import dna_model_service_pb2_grpc

class DnaModelService(dna_model_service_pb2_grpc.DnaModelServiceServicer):
    def PredictSequence(self, request_iterator, context):
        logging.info("PredictSequence called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PredictInterval(self, request_iterator, context):
        logging.info("PredictInterval called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PredictVariant(self, request_iterator, context):
        logging.info("PredictVariant called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ScoreInterval(self, request_iterator, context):
        logging.info("ScoreInterval called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ScoreVariant(self, request_iterator, context):
        logging.info("ScoreVariant called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ScoreIsmVariant(self, request_iterator, context):
        logging.info("ScoreIsmVariant called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetadata(self, request, context):
        logging.info("GetMetadata called")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dna_model_service_pb2_grpc.add_DnaModelServiceServicer_to_server(DnaModelService(), server)
    server.add_insecure_port('[::]:50051')
    print('gRPC server running on port 50051...')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()