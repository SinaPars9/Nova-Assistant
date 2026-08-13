from datetime import datetime
class Reminder:    
    def __init__(self,assisstant):
        self.assistant = assisstant
        self.reminders = {}
    @property
    def is_empty(self):
        return len(self.reminders) <= 0
    def show_reminders(self):
        if not self.is_empty:
            now = datetime.now()
            for count , item in enumerate(self.reminders,1):
                desc = self.reminders[item]['description']
                status = self.reminders[item]['status']
                created_at = self.reminders[item]['created_at']
                deadline = self.reminders[item]['deadline']
                remaining= deadline - now
                print(f'{count}. {item}: {desc} [{status}]\ncreated at : {created_at}\ndeadline: {deadline}\nreaming : {remaining}')
            return True
        return False
    def get_deadline(self):
        while True:
            try:
                deadline = self.assistant.get_input('enter dead line (yyyy/mm/dd hh:mm) : ')
                deadline = datetime.strptime(deadline,'%Y/%m/%d %H:%M')
                return deadline
            except ValueError:
                print('wrong format')
                continue
    def get_reminders(self):
        while True:
            try:
                name = self.assistant.get_input('what do you want to add? : ').lower()
                if name == '' :
                    raise ValueError
                if name in self.reminders:
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
    def add_reminders(self):
        now = datetime.now()
        name , description = self.get_reminders()
        deadline = self.get_deadline()
        self.reminders[name] = {
            'description' : description,
            'status' : 'undone',
            'created_at' : now,
            'deadline' : deadline,
        }
        return True
    def remove_reminders(self):
        if not self.is_empty:
            while True:
                reminders_keys =list(self.reminders.keys())
                self.show_reminders()
                try:
                    ask = int(self.assistant.get_input(f'{len(self.reminders) + 1}. Back\nchoose one : '))
                    if not (1<= ask <=len(self.reminders) + 1 ):
                        raise ValueError
                except ValueError:
                    print('enter number one the list!')
                    continue
                if ask == len(self.reminders) + 1 :
                    return True
                get = reminders_keys[ask  -1 ]
                self.reminders.pop(get)
                return True
        else:
            return False
    def toggle_reminders(self):
        if not self.is_empty:
            while True:
                reminders_keys =list(self.reminders.keys())
                self.show_reminders()
                try:
                    ask = int(self.assistant.get_input(f'{len(self.reminders) + 1}. Back\nchoose one to toggle status : '))
                    if not (1<= ask <=len(self.reminders) + 1 ):
                        raise ValueError
                except ValueError:
                    print('enter number one the list!')
                    continue
                if ask == len(self.reminders) + 1 :
                    return True
                get = reminders_keys[ ask  -1 ]
                current_status = self.reminders[get]['status']
                self.reminders[get]['status'] = 'done' if current_status == 'undone' else 'undone'
                return True
        else:
            return False
    def check_reminders(self):
        now = datetime.now()
        overdue = []
        if not self.is_empty:
            for name, data in self.reminders.items():
                if data['status'] == 'undone':
                    if data['deadline'] <= now:
                        overdue.append(f"Reminder: {name}\nDescription : {data['description']}")
            return overdue
        return False
    def to_dict(self):
        new_dict = {}
        for key , value in self.reminders.items():
            item_data = {
                'description': value['description'],
                'status': value['status'],
                'created_at': value['created_at'].isoformat(),
                'deadline': value['deadline'].isoformat()
            }
            new_dict[key] = item_data
        return new_dict
    def from_dict(self,data):
        new_dict={}
        for key , value in data.items():
            item_data = {
                'description': value['description'],
                'status': value['status'],
                'created_at':datetime.fromisoformat(value['created_at']),
                'deadline': datetime.fromisoformat(value['deadline'])
            }
            new_dict[key] = item_data
        self.reminders.update(new_dict)        


