import os

import requests

from logger import get_logger
from thirdparty.openai_assistant import AssistantAPI

logger = get_logger(__name__)

instructions = """
 
You are an SEO Expert. Your task is generate sitemap.xml for www.rgbkit.com.
You SEO file should be a vaild xml and should follow all the norms so that Search Engines can accept it. 

"""

prompt = """
Please help me in creating sitemap.xml that I will use for SEO purpose. You need to pick only the unique urls from the given 
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

"""

client = AssistantAPI.create_client(
    api_key="42ef311b5f274981be65da45d46bac65",
    api_version="2024-02-15-preview",
    azure_endpoint="https://njcswedencentral.openai.azure.com/",
)

assistant = client.beta.assistants.create(
    name="SEO Expert", instructions=instructions, model="njc-assistant-gpt4-32k"
)

valid_urls_filename = "valid_urls.txt"
output_sitemap_filename = "new_sitemap.xml"


def create_sitemap_file(new_urls_file_path):

    # Get the directory name
    directory = os.path.dirname(new_urls_file_path)
    print(f"directory={directory}")

    # Exclude page with 404 error
    valid_urls_file_path = os.path.join(directory, valid_urls_filename)

    exclude_invalid_urls(new_urls_file_path, valid_urls_file_path)

    with open(valid_urls_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Generate sitemap
    sitemap = generate_sitemap(content)

    # Save the response
    output_sitemap_file_path = os.path.join(directory, output_sitemap_filename)
    save_content(output_sitemap_file_path, sitemap)


def generate_sitemap(content):
    print("Read Entire File:\n", content)
    str = prompt.replace("{content}", content)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, assistant=assistant, thread=assistant_api.create_thread()
    )
    return response

def save_content(file_path, content):
    # Write content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"File created and content saved at: {file_path}")


def exclude_invalid_urls(new_urls_file_path, valid_urls_filepath):
    """Reads URLs from a file."""
    with open(new_urls_file_path, "r") as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]
    valid_urls = [url for url in urls if check_url(url)]

    write_valid_urls(valid_urls, valid_urls_filepath)


def check_url(url):
    """Checks if a URL returns a 404 status code."""
    try:
        response = requests.head(url)
        if response.status_code == 404:
            print(f"invalid 404 url detected={url}")
            return False
        return True
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False


def write_valid_urls(urls, output_file_path):
    """Writes valid URLs to a new file."""
    with open(output_file_path, "w") as file:
        for url in urls:
            file.write(url + "\n")
