import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    config = Config.load()
    config.validate()

    logger.info("Application started")
    logger.info(f"Database: {config.database_url[:20]}...")

    # Твоя логика здесь

if __name__ == "__main__":
    main()
