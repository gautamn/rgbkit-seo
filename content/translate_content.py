from logger import get_logger
import traceback, time, json
from dotenv import load_dotenv
from thirdparty.openai_assistant import AssistantAPI
import os

logger = get_logger(__name__)

instructions = '''
 
You are a language translator. Your task is to translate given content into a list of languages.
You content should be SEO friendly, crisp, clear and should be optimised for improving the SEO ranking of indexed pages. 

'''

prompt = '''
The below content is to be translated into the language with code {language_code}. You need to find out the language 
from the language code nd translate the page accordingly.

- The output should be in JSON format with below schema.
- Only the values in the json content is to be translated. 
- Do not process values of keys: src, type, buttons.
- No json keys to be translated. Only value to be translated.
- The final json should be a valid json without any illegal characters.
- Just provide the json and no extra comments before or after the json. 



CONTENT: {content}



'''

lang_codes = ["de", "fr", "ru", "tr", "id", "pt", "ro", "es", "ja", "it", "hi", "ar", "nl", "ko", "th", "vi"]
#lang_codes = ["ind"]
              
client = AssistantAPI.create_client(
            api_key="42ef311b5f274981be65da45d46bac65",
            api_version="2024-02-15-preview",
            azure_endpoint="https://njcswedencentral.openai.azure.com/"
        )

assistant = client.beta.assistants.create(
                name="Language Translator",
                instructions=instructions,
                model="njc-assistant-gpt4-32k"
            )
 
def translate_file_content(file_path):
   #print(f"file_path={file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Get the directory name
    directory_name = os.path.dirname(file_path)    
    print(f"directory_name={directory_name}")

    # Get the base name (file name)
    file_name=os.path.basename(file_path)
    print(f"file_name:{file_name}")

    for lang_code in lang_codes:
        try:
            lang_specific_content=translate_content(content, lang_code)
            file_name_without_extension = file_name.replace(".json", "")
            output_file_name = file_name_without_extension + "_" + lang_code + ".json"
            save_content(directory_name, output_file_name , lang_specific_content)
        except Exception as e:
                logger.error(e)
                logger.error("error occured while translation into lang code = %s!", lang_code)    

def save_content(directory, file_name, content):   
    # Create the full file path
    file_path = os.path.join(directory, file_name)

    # Create the directory if it does not exist
    os.makedirs(directory, exist_ok=True)

    # Write content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"File created and content saved at: {file_path}")
    
def translate_content(content, lang_code):
    #print("Read Entire File:\n", content)
    str=prompt.replace("{content}", content)
    str=str.replace("{language_code}", lang_code)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    feature_content=response
    #print(feature_content)
    return feature_content    

