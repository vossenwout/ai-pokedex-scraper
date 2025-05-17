from pokedex_scraper.utils.logging import init_logging
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

if os.path.exists("config/logging.yaml"):
    init_logging("config/logging.yaml")
    logger.info("Logging initialized")
else:
    logger.error("Logging config not found")

if os.path.exists("config/.env"):
    load_dotenv("config/.env")
    logger.info("Environment variables loaded")
else:
    logger.error("Environment variables not found")
