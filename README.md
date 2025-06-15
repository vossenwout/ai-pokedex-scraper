# Pokedex Scraper

This project contains a script to setup a zilliz knowledgebase and contains a scraping / ingestion job to scrape pokedex data from https://pokemondb.net/pokedex and ingest it into the zilliz knowledgebase. This knowledgebase is used by the AI Pokedex Assistant to answer questions.

<img src="assets/banner.png" alt="Pokedex Frontend Screenshot" width="300"/>

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

This env file should contain the env vars of `config/.env.example`.

| Environment Variable             | Description                         | Where to get it              |
| -------------------------------- | ----------------------------------- | ---------------------------- |
| `GEMINI_API_KEY`                 | API key for accessing Gemini models | https://aistudio.google.com/ |
| `ZILLIZ_CLUSTER_PUBLIC_ENDPOINT` | Public endpoint for Zilliz cluster  | https://zilliz.com/          |
| `ZILLIZ_CLUSTER_TOKEN`           | Authentication token for Zilliz     | https://zilliz.com/          |

## Project Structure

- `scripts/create_kb.py`: Contains the script to create the zilliz knowledgebase.
- `src/pokedex_scraper/__main__.py`: Contains the Scrapy job to scrape the pokedex data to `data/raw` folder.
- `src/pokedex_scraper/chunking/chunker.py`: Contains the script to chunk the scraped data stored in `data/raw` folder into smaller chunks. Results are stored in `data/chunked` folder.
- `src/pokedex_scraper/ingestion/ingestor.py`: Contains the script to ingest the chunked data from `data/chunked` folder into the zilliz knowledgebase.

## Running the Scraper

1. **Create the zilliz knowledgebase:**

   ```bash
   poetry run python scripts/create_kb.py
   ```

2. **Run the scraper:**

   ```bash
   poetry run python -m pokedex_scraper
   ```

3. **Chunk the scraped data:**

   ```bash
   poetry run python src/pokedex_scraper/chunking/chunker.py
   ```

4. **Ingest the chunked data into the zilliz knowledgebase:**

   ```bash
   poetry run python src/pokedex_scraper/ingestion/ingestor.py
   ```
