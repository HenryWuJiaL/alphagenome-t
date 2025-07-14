import grpc
from alphagenome.protos.alphagenome.protos import dna_model_service_pb2_grpc, dna_model_pb2

# 构造请求
interval = dna_model_pb2.Interval(
    chromosome='chr22',
    start=35677410,
    end=36725986,
    strand=dna_model_pb2.STRAND_UNSTRANDED,
)
variant = dna_model_pb2.Variant(
    chromosome='chr22',
    position=36201698,
    reference_bases='A',
    alternate_bases='C',
)
request = dna_model_pb2.PredictVariantRequest(
    interval=interval,
    variant=variant,
    requested_outputs=[dna_model_pb2.OUTPUT_TYPE_RNA_SEQ],
    # 可选: organism/ontology_terms
)

# 连接并调用
channel = grpc.insecure_channel('localhost:50051')
stub = dna_model_service_pb2_grpc.DnaModelServiceStub(channel)
responses = stub.PredictVariant(iter([request]))
for response in responses:
    print(response)