from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    web_scraper,
)


def main():
    url = "https://nexunity.tech"
    tags_to_extract = ["title", "links", "h1", "p"]
    result = web_scraper.scrape(url, tags_to_extract)

    for tag, content in result.items():
        if isinstance(content, list):
            logger.info(f"{tag}: {len(content)} items")
        else:
            logger.info(f"{tag}: {content}")


if __name__ == "__main__":
    main()
