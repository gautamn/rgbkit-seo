from openai import AzureOpenAI
from logger import get_logger
import traceback, time, json
from dotenv import load_dotenv
from thirdparty.openai_assistant import AssistantAPI

logger = get_logger(__name__)

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

intro_prompt = '''
Please write below content for feature {feature}. The output should be in JSON format with below schema.
{

	"title" : "Free Remove Background Tool for Exceptional Image Editing",
	"desc": "Effortlessly trim away the clutter from your images with our free Remove Background tool",
	"keywords": [
        "Remove background online",
        "Background removal",
        "Online background eraser",
        "Background replacement",
        "Transparent background",
        "AI background removal"
    ],
	"intro": {
        "img": {
            "src": "assets/img/no-preview.png",
            "alt": ""
        },
        "title": "Free Online Remove Background Tool",
        "desc": "Experience Seamless Image Enhancement with our Free Remove Background Tool",
        "uploadBtnText": "Upload Image",
        "dragDropText": "Drag & Drop image files!"
    }
}
'''

qna_prompt = '''
Please write 7 SEO friendly question and answer around {feature}. The output should be in JSON format with below schema.
{
    "items": [
        {
            "ques": "How effective is the free Remove Background tool?",
            "ans": "You can expect high-quality, professional results with our free Remove Background tool."
        }
    ]
}
    

    
'''    

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
    feature_content = {}
    feature_content=create_intro(
            feature_content=feature_content,
            feature=feature
        )
    feature_content = create_qna(
            feature_content=feature_content,
            feature=feature
        )
    print(f"feature_content={feature_content}") 
    
def create_intro(feature_content, feature):
    str=intro_prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    print(f"content after prompt is replaced with feature name=[{str}]")
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    feature_content=json.loads(response)
    return feature_content

def create_qna(feature_content, feature):
    str=qna_prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    print(f"content after prompt is replaced with feature name=[{str}]")
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    items=json.loads(response)
    feature_content["h1"] = "FAQ: Frequently Asked Questions"
    feature_content["h2"] = ""
    feature_content["type"] = "faq"
    feature_content["items"] = items
    return feature_content   