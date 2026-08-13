from assistant import Assistant
from translations import COMMAND_ALIASES
from weather import weather
from joke import joke
from fact import get_fact
from datetime import datetime
from difflib import get_close_matches
from cmd_commands import Notemixin , CalcMixin,TodoMixin,RemindersMixin
from templates import get_response
from translations import translate , text_reshape_farsi
from search import search_query
# from voice_io import listen
class Command( Notemixin , CalcMixin,TodoMixin,RemindersMixin):
    def __init__(self,assistant):
        self.assistant = assistant
        self.commands = {
        name[4:]: getattr(self, name)
        for name in dir(self)
        if name.startswith("cmd_") 
        }
        print(self.commands.keys())
        self.operation_list = ['/','*','-','+']
        self.NO_TRANSLATE = ['help', 'stats', 'show_settings']
        self.command_count = 0
        self.last_output = ''
        self.gui_mode = False
    def set_gui_mode(self, enabled=True):
        self.gui_mode = enabled
    def get_input(self, prompt):
        if self.gui_mode:
            try:
                from tkinter import simpledialog
                root = self.assistant.gui_root 
                return simpledialog.askstring("Input", prompt, parent=root)
            except:
                return input(prompt)
        else:
            return input(prompt)
    def get_amount(self):
        while True:
            try:
                ask = int(input(self.get_input('how much? : ')))
                return ask
            except ValueError:
                print('enter number')
    def command_update(self):
        self.command_count += 1
    def cmd_save(self):
        self.assistant.save()
        return True , ('data save')
    def load(self):
        result = self.assistant.load()
        return result
    def cmd_help(self):
        commands_names = ' , '.join(self.commands.keys()) 
        data = {'commands': commands_names}
        msg = get_response('help',data)
        return True , text_reshape_farsi(msg)
    def cmd_gold(self):
        if self.assistant.is_gold_empty:
            return True , 'gold is zero'
        data = {'gold' : self.assistant.gold}
        result = get_response('gold',data)
        msg = str(result)
        return True , msg
    def cmd_add_gold(self):
        gold = self.get_amount()
        self.assistant.add_gold(gold)
        return True , (f'gold added\ncurrent gold : {self.assistant.gold}')
    def cmd_hello(self):
        data = {'user' : self.assistant.user_name}
        msg = get_response('hello',data)
        return True , str(msg) 
    def cmd_name(self):       
        return True  , (f'My name is {self.assistant.name}') 
    def cmd_bye(self):
        return False,('Goodbye!')
    def cmd_time(self):
        now = datetime.now()
        return True ,(f'currnet time: {now.hour} : {now.minute}')
    def cmd_date(self):
        now = datetime.now()
        return True , (f'today : {now.year}/{now.month}/{now.day}')
    def cmd_stats(self):
        mode = 'Smart' if self.assistant.smart_mode else "Normal"
        return True, (
        f'Name : {self.assistant.user_name}\n'
        f'Gold : {self.assistant.gold}\n'
        f'Commands : {self.command_count}'
        f'Mode : {mode}'
    )
    def cmd_change_city(self):
        city = self.assistant.get_input("where do you live? : ")
        if city is None:  
            return True, "City change cancelled."
        self.assistant.city = city
        self.assistant.save()
        return True, f"city updated to {city}"
    def cmd_city(self):
        if not self.assistant.city:
            city = self.assistant.set_city()
            return True , city
        city = self.assistant.show_city()
        return True , city
    def cmd_history(self):
        if self.assistant.show_history():
            return True ,'done'
        return True , 'history is empty'
    def cmd_set_language(self):
        lang = self.assistant.set_language()
        return True, f"language set to {lang}"
    def cmd_show_language(self):
        return True, self.assistant.language
    def cmd_about(self):
        return True, (
        f"{self.assistant.name}\n"
        "Version 0.1\n"
        "Created by Sina"
    )
    def cmd_show_settings(self):
        return True , self.assistant.show_settings()
    def cmd_weather(self):
        result = weather(self.assistant)
        if isinstance (result,dict):
            msg = get_response('weather',result)
        else:
            msg = str(result)
        return True , msg
    def cmd_fact(self):
        fact_text = get_fact(self.assistant)
        data = {'fact':fact_text}
        msg = get_response('fact',data)
        return True , msg
    def cmd_joke(self):
        joke_text = joke(self.assistant)
        data = {'joke': joke_text}
        msg = get_response('joke',data)
        return True , msg

    def fuzzy_match(self,text):
        command_name = [key for key in COMMAND_ALIASES.keys()]
        matches = get_close_matches(text,command_name,n=1,cutoff=0.6)
        if matches:
            return matches[0]
        return None  
    def cmd_search(self, gui_callback=None):
        if gui_callback:
            return gui_callback()  
        else:
            query = input("What do you want to search? ")
            result = search_query(query)
            return True, result
    def run_smart_mode(self):
        while True:
            ask = input('\ntalk to nova plus : ')
            if ask in ('exit','bye','smart mode off','خروج'):
                result , msg = self.cmd_toggle_smart_mode()
                print(msg)
                return 
            if ask == '':
                print('cant be empty!')
            print('Nova : ')
            text_reshape_farsi(self.assistant.smart_mode_history.ollama_chat(ask))
    def cmd_toggle_smart_mode(self): 
        if self.assistant.smart_mode == False:  
            self.assistant.smart_mode = True
            self.assistant.load_smart_history()
            return True , ' smart mode activated'
        if self.assistant.smart_mode == True:
            self.assistant.smart_mode = False
            self.assistant.save_smart_history()
            return True , 'smart mode diactivated'
    def process_command(self, command):
        cmd = COMMAND_ALIASES.get(command, command)
        if cmd in self.commands:
            action = self.commands.get(cmd)
        else:
            fuzzy_cmd = self.fuzzy_match(cmd)
            if fuzzy_cmd:
                if fuzzy_cmd in COMMAND_ALIASES.keys():
                    cmd = COMMAND_ALIASES[fuzzy_cmd]
                else:
                    cmd = fuzzy_cmd
                if cmd in self.commands:
                    print(f"Did you mean '{cmd}'?")
                    action = self.commands[cmd]
                else:
                    action = None
            else:
                action = None    
        if not action:
            if self.assistant.smart_mode:
                response = self.assistant.smart_mode_history.ollama_chat(command)
                self.last_output = response
                return
            self.last_output = "Unknown command"
            print("Unknown command")
            return 
        if self.assistant.smart_mode:
            if command.lower() in ('exit', 'bye', 'smart mode off', 'خروج'):
                self.cmd_toggle_smart_mode()
                self.last_output = "حالت هوشمند خاموش شد."
                return
            response = self.assistant.smart_mode_history.ollama_chat(command)
            self.last_output = response
            return
        self.assistant.add_history(command)
        self.command_update()
        result, msg = action()
        self.last_output = msg                  
        if cmd not in self.NO_TRANSLATE:
            translations = translate(msg)
            text = text_reshape_farsi(translations)
            print(text)
            self.last_output = text 
        else:
            print(msg)
            self.last_output = msg
        return result

if __name__ == '__main__':
    nova = Assistant('Nova')
    nova_command = Command(nova)
    nova.greet()
    loaded = nova_command.load()
    if loaded:
        print('load found')
    else:
        nova.greet_user()
    while True:
        if nova_command.assistant.smart_mode:
            nova_command.run_smart_mode()
        command = input('your command : ')
        if  not command:
            print('type again')
            continue
        if not nova_command.process_command(command):
            break
