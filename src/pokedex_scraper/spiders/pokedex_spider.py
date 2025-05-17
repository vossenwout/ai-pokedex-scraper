import scrapy
import logging
import re
from pokedex_scraper.items import PokedexEntry
from scrapy.http import HtmlResponse

logger = logging.getLogger(__name__)


class PokedexSpider(scrapy.Spider):
    name = "pokedex_spider"
    start_urls = ["https://pokemondb.net/static/sitemaps/pokemondb.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pokedex_scraper.pipelines.PokedexPipeline": 300,
        }
    }

    def parse(self, response):

        # Extract all <loc> elements from the XML
        logger.debug("Extracting URLs from XML")

        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = response.xpath("//s:url/s:loc/text()", namespaces=ns).getall()

        for url in urls:

            # examples we want to scrape:
            # https://pokemondb.net/pokedex/pidgeot
            # https://pokemondb.net/pokedex/charizard

            if re.match(r"^https://pokemondb\.net/pokedex/[^/]+$", url):
                yield scrapy.Request(url, callback=self.parse_pokemon)

    def parse_pokemon(self, response: HtmlResponse):
        html = response.xpath(
            '//main[@id="main" and contains(@class, "main-content") and contains(@class, "grid-container")]'
        ).get()

        # Select all direct children of <main> that are NOT <nav>
        content_parts = response.xpath(
            '//main[@id="main" and contains(@class, "main-content") and contains(@class, "grid-container")]/*[not(self::nav)]'
        ).getall()

        # Join the pieces back into one HTML string
        cleaned_html = "".join(content_parts)

        yield PokedexEntry(
            pokemon_name=response.url.split("/")[-1],
            url=response.url,
            html=cleaned_html,
        )
