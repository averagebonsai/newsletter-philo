from model_utils import get_neon_client, get_openai_client, get_gemini_client
from tinyfish import get_tinyfish_news

chat_model = 'gpt-5-nano'
chat_prompt = "There should be 5 news articles and 2 opinion pieces. Summarise each article into roughly 2 paragraphs or 200 words. Ensure that arguments are fully fleshed out along with any counterarguments. Do not add in your own opinions. Do not address me, simply give the summary."
gemini_model = 'gemini-2.5-flash'
gemini_prompt = "There are summaries of 5 news articles and 2 opinion pieces here. For each piece, place it in conversation with a relevant political philosopher and historian. Ideally, this should be a response in support of or against one of the viewpoints raised in the article. Introducing a third, unconsidered perspective is also good. Do not edit the article summary, but add another paragraph at the end of the summary detailing what this philosopher or historian might say. This paragraph should be around 150-200 words. Briefly raise 1 contention with this viewpoint too. Remove all formatting (bolding, horizontal lines)."

def summariser(): 
    client = get_openai_client() 
    try: 
        response = client.responses.create(
            model = chat_model, 
            input = [{
                "role": "user", 
                "content": chat_prompt
                }]
        )
        return response.output_text
    except Exception as e: 
        print(f"Unable to get summary: {e}")
        return None

def philosopher(response_text): 
    client = get_gemini_client()
    try: 
        response = client.models.generate_content(
            model = gemini_model, 
            contents = f"{gemini_prompt} {response_text} {gemini_prompt}"
        )
        return response.text
    except Exception as e: 
        print(f"Unable to get philosophy commentary: {e}")
        return None 

def to_database(entry): 
    



if __name__ == "__main__": 
    philosopher(summariser())


    
    

