import sys
from logger import get_logger
from content.generate_content import create_seo_content

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
              if len(sys.argv) == 1:
                     logger.info("utility name is missing.")
                     logger.info("Usage: python main.py SEO_CONTENT")
                     sys.exit()
              create_seo_content()                                                                                             
       
         
             


