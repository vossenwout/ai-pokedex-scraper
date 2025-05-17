from google import genai
from dotenv import load_dotenv
import os

load_dotenv("config/.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def test_gemini():
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-05-06",
        contents="Explain how AI works in a few words",
    )
    print(response.text)


def test_embedding_exp():
    result = client.models.embed_content(
        model="gemini-embedding-exp-03-07", contents="What is the meaning of life?"
    )

    print(result)


def test_embedding():
    # https://ai.google.dev/gemini-api/docs/models#text-embedding-and-embedding
    result = client.models.embed_content(
        model="models/text-embedding-004", contents="What is the meaning of life?"
    )
    return result
    print(result)


embedding = test_embedding()

print(len(embedding.embeddings[0].values))
