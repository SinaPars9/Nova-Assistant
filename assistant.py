import json
import requests
from todomanager import TodoManager
from task_reminder import Reminder
from config import MAX_HISTORY
from chat import ollama
class Assistant:
    def __init__(self, name):
        self.name = name
        self.user_name = None
        self.gold = 100
        self.note = []
        self.history = []
        self.max_history = MAX_HISTORY
        self.city = None
        self.language ='fa'
        self.todos = TodoManager(self)
        self.reminders = Reminder(self)
        self.gui_root = None
        self.use_gui_input = False
        self.smart_mode = False
        self.smart_mode_history = ollama()
    def set_gui_root(self, root):
        self.gui_root = root
        self.use_gui_input = True
    def get_input(self, prompt):
        if self.gui_root:
            from tkinter import simpledialog
            return simpledialog.askstring("Input", prompt, parent=self.gui_root)
        else:
            return input(prompt)
    def greet(self):
        print(f"Hello! I am {self.name}")
    @property
    def is_gold_empty(self):
        return self.gold <= 0
    def add_gold(self, amount):
        self.gold += amount
    def get_name(self):
        self.user_name = input('what is your name? : ')
        return self.user_name
    def greet_user(self):
        user_name = self.get_name()
        print(f'hello {user_name}')
    def add_note(self,text : str):
        self.note.append(text)
    def remove_note(self,text:str):
        self.note.remove(text)
    @property
    def is_empty(self):
        return len(self.note) == 0
    def show_note(self):
        if  self.is_empty:
            return False
        for count, note in enumerate(self.note, 1):
            print(f'{count}. {note}')
        return True
    def add_history(self,command):
        if len(self.history) >= self.max_history:
            self.history.pop(0)
        if command != 'history':
            self.history.append(command)
    @property
    def history_is_empty(self):
        return len(self.history) == 0
    def show_history(self):
        if not self.history_is_empty:
            for count , item in enumerate(self.history,1):
                print(f'{count}. {item}')
            return True
        return False
    def set_city(self):
        self.city = input('where do you live? : ')
        return self.city
    def show_city(self):
        if self.city:
            return self.city
        return False
    def set_language(self):
        while True:
            lang = input("Language (fa/en): ").lower()
            if lang in ("fa", "en"):
                self.language = lang
                return lang
            print("choose fa or en")
    def show_settings(self):
        return (f'Language : {self.language}\nCity : {self.city}')
    def  get_coordinates(self):
        if not self.city:
            return None
        url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={self.city}"
        )
        try:
            response = requests.get(url,timeout=10)
            data = response.json()
            if "results" not in data:
                return None
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
            return lat, lon
        except requests.RequestException:
            return None
    def to_dict(self):
        return {
            "name": self.name,
            "user_name": self.user_name,
            "gold": self.gold,
            'note':self.note,
            'history' :self.history,
            'city' : self.city,
            'language': self.language,
            'to do list': self.todos.todos,
            'reminders' : self.reminders.to_dict()
            
        }
    def save(self):
        with open("nova_ai.json","w") as file:
            json.dump(self.to_dict(), file)
    def load(self):
        try:
            with open("nova_ai.json","r") as file:
                data = json.load(file)
            self.name = data["name"]
            self.user_name = data["user_name"]
            self.gold = data["gold"]
            self.note = data['note']
            self.history = data ['history']
            self.city = data['city']
            self.language = data['language']
            self.todos.todos = data['to do list']
            self.reminders.from_dict(data['reminders'])
            return True
        except FileNotFoundError:
            return False
    def save_smart_history(self):
        with open("smart_history.json", "w") as file:
            json.dump(self.smart_mode_history.history, file)

    def load_smart_history(self):
        try:
            with open("smart_history.json", "r") as file:
                self.smart_mode_history.history = json.load(file)
        except FileNotFoundError:
            pass

