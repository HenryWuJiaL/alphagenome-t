import grpc
from concurrent import futures
import logging
import os

from alphagenome.protos.alphagenome.protos import dna_model_service_pb2_grpc
from alphagenome.protos.alphagenome.protos import dna_model_pb2
from alphagenome.models import dna_client
from alphagenome.data import genome

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
        # 1. Get the first request from the iterator (stream-stream, but we handle one for now)
        try:
            request = next(request_iterator)
        except StopIteration:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('No request provided')
            return

        # 2. Extract parameters from the gRPC request
        interval_proto = request.interval
        variant_proto = request.variant
        organism_proto = request.organism
        requested_outputs_proto = request.requested_outputs
        ontology_terms_proto = request.ontology_terms

        # 3. Map proto to Python objects
        interval = genome.Interval.from_proto(interval_proto)
        variant = genome.Variant.from_proto(variant_proto)
        # Organism: use default if not set
        organism = None
        if hasattr(dna_client, 'Organism'):
            for org in dna_client.Organism:
                if org.value == organism_proto:
                    organism = org
                    break
        if organism is None:
            organism = dna_client.Organism.HOMO_SAPIENS

        # requested_outputs: map proto enums to OutputType
        output_type_map = {ot.value: ot for ot in dna_client.OutputType}
        requested_outputs = [output_type_map.get(v, dna_client.OutputType.RNA_SEQ) for v in requested_outputs_proto]

        # ontology_terms: pass as None or [] for now (TODO: map if needed)
        ontology_terms = None
        if ontology_terms_proto:
            # TODO: Map ontology_terms_proto to ontology term objects/strings if needed
            ontology_terms = []

        # 4. Call AlphaGenome API
        api_key = os.environ.get('ALPHAGENOME_API_KEY')
        if not api_key:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('ALPHAGENOME_API_KEY environment variable is not set. Please set it with your AlphaGenome API key.')
            return
        model = dna_client.create(api_key)
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            organism=organism,
            requested_outputs=requested_outputs,
            ontology_terms=ontology_terms,
        )

        # 5. Map outputs to gRPC response
        # outputs.reference, outputs.alternate are likely Output objects
        response = dna_model_pb2.PredictVariantResponse()
        if hasattr(outputs, 'reference') and hasattr(outputs, 'alternate'):
            if hasattr(outputs.reference, 'to_proto'):
                response.reference_output.CopyFrom(outputs.reference.to_proto())
            if hasattr(outputs.alternate, 'to_proto'):
                response.alternate_output.CopyFrom(outputs.alternate.to_proto())
        yield response

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