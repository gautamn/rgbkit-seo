from logger import get_logger
from thirdparty.openai_assistant import AssistantAPI

logger = get_logger(__name__)

instructions = '''

You are a great SEO writer. You job is to write blogs for various features of http://www.rgbkit.com. 
The content should be crisp, clear and SEO optimised.

'''

blog_prompt = '''

Please write a blog on feature {feature}. The blog should have following sections:


Title: 
Create a catchy and descriptive title that includes the primary keyword. Keep it within 60 characters.

Meta Description: 
Write a concise meta description (150-160 characters) that summarizes the content and includes the main keyword. Make it enticing to encourage clicks.

Introduction:
Start with a strong introduction that includes the primary keyword.
Clearly state what the blog post will cover to engage readers from the beginning.


Headers and Subheaders (H1, H2, H3):
Use headings to break up content into easily readable sections.
Include relevant keywords in subheadings to improve SEO and readability.

Content:
Provide high-quality, valuable, original, and informative content.
Aim for comprehensive coverage of the topic to satisfy user intent.
Naturally integrate primary and secondary keywords throughout the post without keyword stuffing.
Write in a clear, concise, and conversational style.
Use short paragraphs, bullet points, and lists to enhance readability.

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

def write_blog(feature):
    str=blog_prompt.replace("{feature}", feature)
    assistant_api = AssistantAPI(client)
    response = assistant_api.execute_thread_with_content(
        content=str, 
        assistant=assistant,
        thread=assistant_api.create_thread())
    print(f"response:\n{response}")