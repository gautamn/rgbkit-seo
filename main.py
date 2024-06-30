import sys
from logger import get_logger
from content.generate_content import create_seo_content
from content.translate_content import translate_file_content

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
         if utility_name == 'SEO_CONTENT':
              if len(sys.argv) == 2:
                     logger.info("utility name or feature name is missing.")
                     logger.info("Usage: python main.py SEO_CONTENT <feature name in quotes>")
                     sys.exit()
              create_seo_content(sys.argv[2])

         # python main.py TRANSLATE C:/my-workspace/seo-content/gif-maker.json    
         elif utility_name == 'TRANSLATE':
              if len(sys.argv) == 2:
                     logger.info("utility name or feature name is missing.")
                     logger.info("Usage: python main.py TRANSLATE <absolute file path>")
                     sys.exit()
              translate_file_content(sys.argv[2])     


       
         
             


