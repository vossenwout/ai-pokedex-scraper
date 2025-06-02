import json
import logging
from pathlib import Path

from markdownify import markdownify as md

from pokedex_scraper.items import PokedexEntry
from pokedex_scraper.spiders.pokedex_spider import PokedexSpider

logger = logging.getLogger(__name__)


class PokedexPipeline:
    def process_item(self, item: PokedexEntry, _: PokedexSpider):
        save_path = Path(f"data/raw/{item['pokemon_name']}")
        save_path.mkdir(parents=True, exist_ok=True)

        with open(save_path / "index.html", "w") as f:
            f.write(item["html"])

        with open(save_path / "index.md", "w") as f:
            f.write(md(item["html"], strip=["a"]))

        metadata = {
            "pokemon_name": item["pokemon_name"],
            "url": item["url"],
        }
        with open(save_path / "metadata.json", "w") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved {item['pokemon_name']} to {save_path}")
        return item
