# Pokedex Scraper

This project contains a script to setup a zilliz knowledgebase and contains a scraping / ingestion job to scrape pokedex data from https://pokemondb.net/pokedex and ingest it into the zilliz knowledgebase. This knowledgebase is used by the AI Pokedex Assistant to answer questions.

<img src="data/banner.png" alt="Pokedex Frontend Screenshot" width="300"/>

## AI Pokedex Project Repos

These are the repos that are used to create and run the AI Pokedex.

- [Knowledgebase and Scraper](https://github.com/vossenwout/pokedex-scraper)
- [Assistant API](https://github.com/vossenwout/pokedex-rag-api)
- [Frontend](https://github.com/vossenwout/pokedex-frontend)
- [Evaluation Framework](https://github.com/vossenwout/pokedex-rag-evaluation)

I created a youtube video where I explain the project: https://www.youtube.com/watch?v=dQw4w9WgXcQ

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management. You can install it with the following commands:
  - **macOS, Linux, or WSL:**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
  - **Windows (PowerShell):**
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/vossenwout/pokedex-scraper
    cd pokedex-scraper
    ```

2.  **Install dependencies:**

    Use Poetry to install the required Python packages.

    ```bash
    poetry install
    ```

## Configuration

To run the assistant you are required to create a `.env` file in the config folder of the project.

```bash
touch config/.env
```

This env file should contain the env vars of `.env.example`.

| Environment Variable             | Description                         | Where to get it              |
| -------------------------------- | ----------------------------------- | ---------------------------- |
| `GEMINI_API_KEY`                 | API key for accessing Gemini models | https://aistudio.google.com/ |
| `ZILLIZ_CLUSTER_PUBLIC_ENDPOINT` | Public endpoint for Zilliz cluster  | https://zilliz.com/          |
| `ZILLIZ_CLUSTER_TOKEN`           | Authentication token for Zilliz     | https://zilliz.com/          |

## Project Structure

- `src/rag_assistant/`: Contains the AI Pokedex assistant implementation.
- `src/server/`: Contains the FastAPI server.

## Running the API

1.  **Run the application:**

    ```bash
    poetry run python -m server
    ```

2.  **Access the API:**

    The API will be available at `http://localhost:8000`.

3.  **Access the API documentation:**

    The API documentation will be available at `http://localhost:8000/docs`.

I would recommend using the frontend to interact with the API. You can find the frontend repo [here](https://github.com/vossenwout/pokedex-frontend).
