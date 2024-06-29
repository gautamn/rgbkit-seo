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

usecase_prompt = '''
Please write 5 use cases as to why use {feature} in the form use case of 3-4 words and then desc in not more than 10-12 words.
The output should be in JSON format with below schema.
{
    "items": [
       {
            "h1": "Product Photo Enhancement",
            "p": "Improve product photos by removing distracting backgrounds."
        }
    ]
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
    sections=[] 
    feature_content = {}
    feature_content=create_intro(
            feature_content=feature_content,
            feature=feature
        )
    print(f"******* feature_content={feature_content}") 
    section_usecase=find_usecases(
            feature=feature
        ) 
    sections.append(section_usecase)
    
    section_faq=create_qna(
            feature=feature
        )
    sections.append(section_faq)
    
    feature_content["sections"] = sections
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

def find_usecases(feature):
    str=usecase_prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    result=json.loads(response)
    section_usecase={}
    section_usecase["title"] = f"Why use our {feature}"
    section_usecase["h2"] = ""
    section_usecase["type"] = "features"
    section_usecase["items"] = result["items"]
    return section_usecase

def create_qna(feature):
    str=qna_prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    print(f"content after prompt is replaced with feature name=[{str}]")
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    result=json.loads(response)
    section_faq={}
    section_faq["h1"] = "FAQ: Frequently Asked Questions"
    section_faq["h2"] = ""
    section_faq["type"] = "faq"
    section_faq["items"] = result['items']
    return section_faq   