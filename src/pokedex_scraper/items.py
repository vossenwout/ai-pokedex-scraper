import scrapy


class PokedexEntry(scrapy.Item):
    pokemon_name = scrapy.Field()
    url = scrapy.Field()
    html = scrapy.Field()
