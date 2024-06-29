from openai import AzureOpenAI
from logger import get_logger
import time, json

logger = get_logger(__name__)

class AssistantAPI:
    def __init__(self, client):
        self.client = client

    @staticmethod
    def create_client(api_key, api_version, azure_endpoint):
        return AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
    
    def create_assistant(self, name, instructions, model="njc-assistant-gpt4-32k"):
        return self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
    
    def create_thread(self):
        return self.client.beta.threads.create()
    
    def execute_thread_with_multiple_contents(self, content_parts, prompt, assistant, thread):
        all_responses_in_str = []  # To store messages from all parts
        try:      
            for i, content in enumerate(content_parts, start=1):          
                logger.debug(f"processing part {i} of {len(content_parts)}, length: {len(content)}")
                new_prompt = prompt.replace("{text}", content)
                #logger.debug("$$$$$$$$$$$ new_prompt=%s", new_prompt)
                result = self.call_assistant_api(
                            assistant=assistant,
                            content=new_prompt, 
                            thread=thread
                        )
                logger.debug("$$$ chunk result=%s", result)
                all_responses_in_str.append(result)
        except Exception as e:
                logger.error(e)
                logger.error("error occured while getting data for chunks!") 
        return all_responses_in_str


    def execute_thread_with_content(self, content, summarizer_assistant, prompt, thread):
        result=''
        try:
            str = ''
            if content is not None:
                if len(content) > 32000:
                    content = content[:32000] #just take 32 chacters for summary
                str=prompt.replace("{text}", content)
            else:
                str = prompt    
            #logger.debug("content=%s", content)
            #logger.debug("prompt=%s", str)
            result = self.call_assistant_api(
                        assistant=summarizer_assistant,
                        content=str,
                        thread=thread
                    )
        except Exception as e:
                logger.error(e)
                logger.error("error occured while getting content summary!!")
        
        return result


    def execute_thread_with_json_content(self, content, assistant, thread):
        result=''
        try:
            result = self.call_assistant_api(
                        assistant=assistant,
                        content=content,
                        thread=thread
                    )
        except Exception as e:
                logger.error(e)
                logger.error("error occured while getting content summary!!")
        
        return result        


    def call_assistant_api(self, assistant, content, thread):
        result = ""
        try:
            #thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=content
            )
            thread_messages = self.client.beta.threads.messages.list(thread.id)
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

            start_time = time.time()
            status = run.status
            while status not in ["completed", "cancelled", "expired", "failed"]:
                time.sleep(5)
                run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                elapsed_time = time.time() - start_time
                logger.debug(f"elapsed time: {int(elapsed_time // 60)} minutes {int(elapsed_time % 60)} seconds")
                status = run.status
                logger.debug(f'status: {status}')
            
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            json_response = json.loads(messages.model_dump_json())
            arr = json_response["data"]
            for item in arr:
                if item["role"] == "assistant":
                    result = item["content"][0]["text"]["value"]
        except Exception as e:
                logger.error(e)
                logger.error("Error occured while calling Assistant API!")        
        
        return result            