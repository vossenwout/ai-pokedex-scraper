from pymilvus import MilvusClient, DataType, Function, FunctionType, AnnSearchRequest
from dotenv import load_dotenv
import os
from pymilvus import WeightedRanker
from google import genai


load_dotenv("config/.env")


client = MilvusClient(
    uri=os.getenv("ZILLIZ_CLUSTER_PUBLIC_ENDPOINT"),
    token=os.getenv("ZILLIZ_CLUSTER_TOKEN"),
)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _embed_content(content: str) -> list[float]:
    result = gemini_client.models.embed_content(
        model="models/text-embedding-004", contents=content
    )
    return result.embeddings[0].values


def full_text_search(query: str):
    search_params = {
        "params": {"level": 10},
    }
    r = client.search(
        collection_name="pokedex",
        data=[query],
        anns_field="sparse",
        limit=1,
        search_params=search_params,
        output_fields=["metadata", "text"],
    )
    return r


def hybrid_search(query: str):
    ranker = WeightedRanker(0.5, 0.5)
    embedding = _embed_content(query)
    semantic_search = AnnSearchRequest(
        data=[embedding],
        anns_field="vector",
        param={"metric_type": "COSINE"},
        limit=2,
    )
    text_search = AnnSearchRequest(
        data=[query],
        anns_field="sparse",
        param={"level": 10, "metric_type": "BM25"},
        limit=2,
    )
    r = client.hybrid_search(
        collection_name="pokedex",
        reqs=[text_search, semantic_search],
        limit=2,
        ranker=ranker,
        output_fields=["metadata", "text"],
    )

    return r


print(hybrid_search("Shellder"))
