import sys

from content.create_blog import write_blog
from content.generate_content import create_seo_content
from content.sitemap import create_sitemap_file
from content.translate_content import translate_file_content
from logger import get_logger
from utils.file_utils import find_missing_urls

logger = get_logger(__name__)

if __name__ == "__main__":

    logger.info("Running SEO Writer for basic file operations!")

    if len(sys.argv) <= 1:
        logger.info("Invalid Commands! No utility name provided in the given command")
        logger.info("Usage: python main.py <UTILITY NAME> [PARAMS]")
        logger.info("Exiting the program...")
        sys.exit()
    else:
        utility_name = sys.argv[1]
        # python main.py SEO_CONTENT "Crop Image"
        if utility_name == "SEO_CONTENT":
            if len(sys.argv) == 2:
                logger.info("utility name or feature name is missing.")
                logger.info(
                    "Usage: python main.py SEO_CONTENT <feature name in quotes> <researched keywords>"
                )
                sys.exit()
            create_seo_content(sys.argv[2], sys.argv[3])

        # python main.py TRANSLATE "I:/My Drive/rgbkit-sharedcontent/tools/compress-png.json"
        elif utility_name == "TRANSLATE":
            if len(sys.argv) == 2:
                logger.info("utility name or feature name is missing.")
                logger.info("Usage: python main.py TRANSLATE <absolute file path>")
                sys.exit()
            translate_file_content(sys.argv[2])

        # python main.py WRITE_BLOG "Remove Bankground"
        elif utility_name == "WRITE_BLOG":
            if len(sys.argv) == 2:
                logger.info("utility name or feature name is missing.")
                logger.info("Usage: python main.py WRITE_BLOG <feature name in quotes>")
                sys.exit()
            write_blog(sys.argv[2])

        # python main.py GEN_SITEMAP "I:/My Drive/rgbkit-sharedcontent/sitemap/new_urls.txt"
        elif utility_name == "GEN_SITEMAP":
            if len(sys.argv) == 2:
                logger.info("utility name or feature name is missing.")
                logger.info("Usage: python main.py GEN_SITEMAP <absolute file path>")
                sys.exit()
            create_sitemap_file(sys.argv[2])

        # python main.py FIND_DIFF "I:/My Drive/rgbkit-sharedcontent/sitemap/all-liveurls-19072024.txt" "I:/My Drive/rgbkit-sharedcontent/sitemap/new_urls.txt"
        elif utility_name == "FIND_DIFF":
            if len(sys.argv) == 2:
                logger.info("utility name or feature name is missing.")
                logger.info("Usage: python main.py FIND_DIFF <absolute live url file path> <absolute new url file path>")
                sys.exit()
            find_missing_urls(sys.argv[2], sys.argv[3])    
