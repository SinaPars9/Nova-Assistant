class TodoManager:
    def __init__(self,assistant):
        self.assistant = assistant
        self.todos = {}
    def get_todos(self):
        while True:
            try:
                name = self.assistant.get_input('what do you want to add? : ').lower()
                if name == '' :
                    raise ValueError
                if name in self.todos:
                    ask = self.assistant.get_input(f'{name} already in your list!\nDo you want to overwrite it? enter ->(yes/no) : ').lower()
                    if ask == '' or ask not in ('yes','no'):
                        raise ValueError
                    elif ask == 'no':
                        continue 
                    elif ask == 'yes':
                        description = self.assistant.get_input('add a description? : ').lower()
                        return name , description
                else:
                    description = self.assistant.get_input('add a description? : ').lower()
                    if description == '':
                        raise ValueError
                    return name , description  
            except ValueError:
                print('cant enter empty or number')
                continue
    @property
    def is_empty(self):
        return len(self.todos) <= 0
    def show_todos(self):
        if not self.is_empty:
            for count , item in enumerate(self.todos,1):
                desc = self.todos[item]['description']
                status = self.todos[item]['status']
                print(f'{count}. {item}: {desc} [{status}]')
            return True
        else:
            return False
    def add_todos(self):
        name ,description = self.get_todos()
        self.todos[name] = {
            'description' : description,
            'status': 'undone'
        }
        return True
    def remove_todos(self):
        if not self.is_empty:
            while True:
                todo_list = list(self.todos.keys())
                self.show_todos()
                try:
                    ask = int(self.assistant.get_input(f'{len(self.todos)+ 1}.Back\nchoose one : '))
                    if not (1<= ask <= len(self.todos) + 1):
                        raise ValueError
                except ValueError:
                    print('enter number on the list')
                    continue
                if ask == len(self.todos) + 1 :
                    return True
                get = todo_list[ask  - 1]
                self.todos.pop(get)
                print(f'{get} removed')
                return True
        else:
            return False
    def toggle_status(self):
        if not self.is_empty:
            while True:
                todo_list = list(self.todos.keys())
                self.show_todos()
                try:
                    ask = int(self.assistant.get_input(f'{len(self.todos) + 1}. Back\nchoose one to toggle status: '))
                    if not (1 <= ask <= len(self.todos) + 1):
                        raise ValueError
                except ValueError:
                    print('enter number on the list')
                    continue
                if ask == len(self.todos) + 1:
                    return True
                get = todo_list[ask - 1]
                current_status = self.todos[get]["status"]
                self.todos[get]["status"] = "done" if current_status == "undone" else "undone"
                print(f'{get} status changed to "{self.todos[get]["status"]}"')
                return True
        else:
            return False


