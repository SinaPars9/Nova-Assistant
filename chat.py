from ollama import chat
from tools import get_weather,get_fact,get_joke,search_web
class ollama:
    def __init__(self,model = 'nova-light'):
        self.model = model
        self.history = []
        self.tools = [get_joke,get_fact,get_weather,search_web]
    def ollama_chat(self,command):
        self.history.append(
            {'role': 'user',
            'content':command
            }
        )
        stream = chat(
            model= self.model, 
            messages=self.history,
            tools=self.tools,
            stream= False
        )
        if stream['message'].get('tool_calls'):
            tool_call = stream['message']['tool_calls'][0]
            func_name = tool_call['function']['name']
            args = tool_call['function']['arguments']

            if func_name == 'get_weather':
                result = get_weather(**args)
            elif func_name == 'get_joke':
                result = get_joke()
            elif func_name == 'get_fact':
                result = get_fact()
            elif func_name == 'search_web':
                result = search_web(**args)
            else:
                result = 'unknown tool'
            self.history.append({
                'role':'tool',
                'content': result
            })
            final_response = chat(
                model=self.model,
                messages=self.history,
                stream=True
            )
                
            reply = ''
            for chunk in final_response:
                part = chunk['message']['content']
                print(part, end='', flush=True)
                reply += part 
            self.history.append({'role': 'assistant', 'content': reply})
            return reply
        else:
            stream_response = chat(
                model=self.model,
                messages=self.history,
                stream=True
            )
            reply = ''
            for chunk in stream_response:
                part = chunk['message']['content']
                print(part, end='', flush=True)
                reply += part
            self.history.append({'role': 'assistant', 'content': reply})
            return  reply

