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

intro_prompt = '''
Please write below content for feature {feature}. The output should be in JSON format with below schema.
Please also include my keywords list {keywords} in your generated "keywords".
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
            "src": "",
            "alt": ""
        },
        "title": "Free Online Remove Background Tool",
        "desc": "Experience Seamless Image Enhancement with our Free Remove Background Tool",
        "uploadBtnText": "Upload Image",
        "dragDropText": "Drag & Drop image files!"
    }
}
'''

heading_prompt = '''
Please write 1 line about the {feature} in not more than 50-60 characters.
The output should be in JSON format with below schema.
{
    "type": "heading",
    "h1": "Experience Seamless Image Enhancement with our Free Remove Background Tool",
    "p": "Make your images stand out with our free Remove Background tool, designed to delete unwanted backgrounds effortlessly. Try it now to unlock the true potential of your pictures!"
}

'''

usecase_prompt = '''
Please write 5 use cases as to why use {feature} in the form use case of 3-4 words and then desc in not more than 10-12 words.
Please also include my keywords list {keywords} in your generated content.
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

detailed_usecase_prompt = '''
Please write 5 use cases of {feature} . The 'p' element in below json should be about 3-5 sentence about the usecase.
You need to included researched keywords {keywords} in your content. 
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
Please write 7 SEO friendly question and answer around {feature}. 
Please also include my keywords list {keywords} in your generated "keywords".
The output should be in JSON format with below schema.
{
    "items": [
        {
            "ques": "How effective is the free Remove Background tool?",
            "ans": "You can expect high-quality, professional results with our free Remove Background tool."
        }
    ]
}
   
'''

steps = '''

{
        "type": "steps",
        "h1": "How to Use Our Free {feature}",
        "p": "",
        "steps": [
            {
                "title": "Upload Your Photo",
                "desc": "Upload your photo or image from your computer",
                "url": ""
            },
            {
                "title": "Wait for Second",
                "desc": "It will take 5 to 8 second to {feature}",
                "url": ""
            },
            {
                "title": "Download",
                "desc": "Download your photo with {feature}",
                "url": ""
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
                name="SEO Writer",
                instructions=instructions,
                model="njc-assistant-gpt4-32k"
            )
 
def create_seo_content(feature, keywords):
    #feature = 'Gif Maker' 
    sections=[] 
    feature_content = {}
    feature_content=create_intro(
            feature_content=feature_content,
            feature=feature,
            keywords=keywords
        )
    
    section_steps=steps.replace("{feature}", feature)
    sections.append(json.loads(section_steps))
    
    section_heading=find_heading(
            feature=feature
        ) 
    sections.append(section_heading)
    
    detailed_usecases=find_detailed_usecases(
            feature=feature,
            keywords=keywords
        )
    for detailed_usecase in detailed_usecases: 
        sections.append(detailed_usecase)
    
    usecases=find_usecases(
            feature=feature,
            keywords=keywords
        ) 
    sections.append(usecases)
    
    section_faq=create_qna(
            feature=feature
        ) 
    sections.append(section_faq)
    
    feature_content["sections"] = sections
    print("*********************************************************************************")
    print(f"feature_content={feature_content}") 
    print("*********************************************************************************")
    
def create_intro(feature_content, feature, keywords):
    str=intro_prompt.replace("{feature}", feature)
    str=str.replace("{keywords}", keywords)
    assistant_api = AssistantAPI(client)
    print(f"content after prompt is replaced with feature name=[{str}]")
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    
    print(f"$$$$$$$$$$$$$$$$$$$ response={response}")
    feature_content=json.loads(response)
    return feature_content

def find_heading(feature):
    str=heading_prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    result=json.loads(response)
    section_heading={}
    section_heading["type"] = result['type']
    section_heading["h1"] = result['h1']
    section_heading["p"] = result['p']
    return section_heading

def find_detailed_usecases(feature, keywords:str|None=None):
    str=detailed_usecase_prompt.replace("{feature}", feature)
    str=str.replace("{keywords}", keywords)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    result=json.loads(response)
    
    arr = []
    for item in result["items"]:
        print(f"item={item}")
        tmp_usecase = {}
        tmp_usecase["type"]= "section"
        tmp_usecase["h1"]= item["h1"]
        tmp_usecase["p"]= item["p"]
        tmp_usecase["img"]={
                "src": "assets/img/no-preview.png",
                "alt": ""
            }
        tmp_usecase["buttons"]=[]
        arr.append(tmp_usecase)
    return arr

def find_usecases(feature, keywords:str|None=None):
    str=usecase_prompt.replace("{feature}", feature)
    str=str.replace("{keywords}", keywords)
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