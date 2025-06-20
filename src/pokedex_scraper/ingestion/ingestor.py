import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pymilvus import MilvusClient
from tqdm import tqdm

load_dotenv("config/.env")


class Ingestor:
    def __init__(
        self,
        source_dir: Path,
        embedding_model: str = "models/text-embedding-004",
        milvus_collection_name: str = "pokedex",
    ) -> None:
        self.source_dir = source_dir
        if not os.getenv("GEMINI_API_KEY"):
            raise OSError("GEMINI_API_KEY not found in environment variables")
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        if not os.getenv("ZILLIZ_CLUSTER_PUBLIC_ENDPOINT"):
            raise OSError(
                "ZILLIZ_CLUSTER_PUBLIC_ENDPOINT not found in environment variables"
            )
        if not os.getenv("ZILLIZ_CLUSTER_TOKEN"):
            raise OSError("ZILLIZ_CLUSTER_TOKEN not found in environment variables")
        self.kb = MilvusClient(
            uri=os.getenv("ZILLIZ_CLUSTER_PUBLIC_ENDPOINT"),
            token=os.getenv("ZILLIZ_CLUSTER_TOKEN"),
        )
        self.milvus_collection_name = milvus_collection_name
        self.embedding_model = embedding_model

    def _embed_content(self, content: str) -> list[float]:
        result = self.gemini_client.models.embed_content(
            model=self.embedding_model,
            contents=content,
        )
        return result.embeddings[0].values

    def _insert_knowledge(self, content: str, metadata: dict):
        embedding = self._embed_content(content)
        self.kb.insert(
            collection_name=self.milvus_collection_name,
            data=[
                {
                    "metadata": metadata,
                    "text": content,
                    "vector": embedding,
                },
            ],
        )

    def run(self):
        chunked_pokedex_dirs = [d for d in self.source_dir.iterdir() if d.is_dir()]
        for chunked_pokedex_dir in tqdm(
            chunked_pokedex_dirs, desc="Inserting knowledge"
        ):
            with open(chunked_pokedex_dir / "metadata.json") as f:
                metadata = json.load(f)

            # glob .md
            md_chunks = [f for f in chunked_pokedex_dir.iterdir() if f.suffix == ".md"]
            for md_chunk in md_chunks:
                with open(md_chunk) as f:
                    content = f.read()
                self._insert_knowledge(content, metadata)


if __name__ == "__main__":
    Ingestor(source_dir=Path("data/chunked")).run()
