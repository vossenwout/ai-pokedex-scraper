from pymilvus import MilvusClient, DataType, Function, FunctionType
from dotenv import load_dotenv
import os

load_dotenv("config/.env")


def create_hybrid_collections():
    client = MilvusClient(
        uri=os.getenv("ZILLIZ_CLUSTER_PUBLIC_ENDPOINT"),
        token=os.getenv("ZILLIZ_CLUSTER_TOKEN"),
    )

    schema = client.create_schema(
        enable_dynamic_field=True, description="Pokedex data for a rag project."
    )

    # id field automatically generated
    schema.add_field(
        field_name="Auto_id",
        datatype=DataType.INT64,
        description="The Primary Key",
        is_primary=True,
        auto_id=True,
    )
    # allow for vector embedding search
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)

    # allow for metadata search
    schema.add_field(field_name="metadata", datatype=DataType.JSON)

    # allow for full text search
    schema.add_field(
        field_name="text",
        datatype=DataType.VARCHAR,
        max_length=10000,
        enable_analyzer=True,
    )
    schema.add_field(field_name="sparse", datatype=DataType.SPARSE_FLOAT_VECTOR)
    # automatically generate sparse vector from text
    bm25_function = Function(
        name="text_bm25_emb",
        input_field_names=["text"],
        output_field_names=["sparse"],
        function_type=FunctionType.BM25,
    )
    schema.add_function(bm25_function)
    # prepare index params
    index_params = client.prepare_index_params()

    # add vector index
    index_params.add_index(
        field_name="vector", metric_type="COSINE", index_type="AUTOINDEX"
    )

    # add sparse index
    index_params.add_index(
        field_name="sparse", index_type="AUTOINDEX", metric_type="BM25"
    )

    client.create_collection(
        collection_name="pokedex", schema=schema, index_params=index_params
    )


create_hybrid_collections()
