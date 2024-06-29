from openai import AzureOpenAI
from logger import get_logger
import traceback, time, json
from dotenv import load_dotenv
from thirdparty.openai_assistant import AssistantAPI

logger = get_logger(__name__)

# client = AzureOpenAI(
#     api_key="42ef311b5f274981be65da45d46bac65",
#     api_version="2024-02-15-preview",
#     azure_endpoint = "https://njcswedencentral.openai.azure.com/"
# )

instructions = '''
 
You are a SEO writer and create content for getting good page rank of image editing tools.
You content should be SEO friendly and should be optimised for improving the SEO ranking of indexed pages. 
The content of different parts should be different from each other but should be SEO friendly. 
'''

prompt = '''

Please write below content for feature {feature}.

1. Title : this should not be more than 50 charaters. Should include with word "Free".

2. meta-description: this should be more than 150 character.

3. meta-keywords: top 10 keywords around feature {feature} with high search volumes.

4. question and answer: 5 SEO friendly question and answer around {feature}.

5. use cases of {feature} : 5 use cases as to why use {feature} in the form use case of 3-4 words and then desc in not more than 10-12 words.

6. Heading : 1 line about the {feature} in not more than 50-60 characters.

7. Paragraph : 2-4 lines about the {feature} in which usecases will be mentioned. 


'''

# Create an assistant
# assistant = client.beta.assistants.create(
#     name="SEO Writer",
#     instructions=instructions,
#     model="njc-assistant-gpt4-32k" #You must replace this value with the deployment name for your model.
# )

client = AssistantAPI.create_client(
            api_key="42ef311b5f274981be65da45d46bac65",
            api_version="2024-02-15-preview",
            azure_endpoint="https://njcswedencentral.openai.azure.com/"
        )

assistant = client.beta.assistants.create(
                name="Guilty Judgment Pronouncement Assistant",
                instructions=instructions,
                model="njc-assistant-gpt4-32k"
            )
 
def create_seo_content():
    feature = 'Png Maker'
    str=prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        client=client,
        content=str, 
        assistant=assistant, 
        prompt=prompt, 
        thread=assistant_api.create_thread())
    print(f"response={response}")