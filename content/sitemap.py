from logger import get_logger
import traceback, time, json
from dotenv import load_dotenv
from thirdparty.openai_assistant import AssistantAPI
import os

logger = get_logger(__name__)

instructions = '''
 
You are an SEO Expert. Your task is generate sitemap.xml for www.rgbkit.com.
You SEO file should be a vaild xml and should follow all the norms so that Search Engines can accept it. 

'''

prompt = '''
Please help me in creating sitemap.xml that I will use for SEO purpose. You need to pick the urls from the given 
text below and add url in loc tag and current timestamp in lastmod tag. The format of the tag would be '2024-06-26T11:55:48+00:00'. 

The structure of the sitemap.xml is 

<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 
    http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
    <url>
    <loc>https://www.rgbkit.com/</loc>
    <lastmod>2024-06-26T11:55:48+00:00</lastmod>
    </url> 
<urlset>

Make ensure that only xml response is returned in the output and no text is included before or after the xml root tag <urlset>. 

CONTENT: {content}

'''

client = AssistantAPI.create_client(
            api_key="42ef311b5f274981be65da45d46bac65",
            api_version="2024-02-15-preview",
            azure_endpoint="https://njcswedencentral.openai.azure.com/"
        )

assistant = client.beta.assistants.create(
                name="SEO Expert",
                instructions=instructions,
                model="njc-assistant-gpt4-32k"
            )

def create_sitemap_file(file_path):
   #print(f"file_path={file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sitemap=generate_sitemap(content)    

    # Get the directory name
    directory_name = os.path.dirname(file_path)    
    print(f"directory_name={directory_name}")

    # Get the base name (file name)
    file_name=os.path.basename(file_path)
    print(f"file_name:{file_name}")

    output_file_name = "new_sitemap.xml"
    save_content(directory_name, output_file_name , sitemap)

def generate_sitemap(content):
    print("Read Entire File:\n", content)
    str=prompt.replace("{content}", content)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    return response 

def save_content(directory, file_name, content):   
    # Create the full file path
    file_path = os.path.join(directory, file_name)

    # Create the directory if it does not exist
    os.makedirs(directory, exist_ok=True)

    # Write content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"File created and content saved at: {file_path}")       