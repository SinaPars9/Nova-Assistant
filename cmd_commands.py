
class Notemixin:
    def get_note(self):
        note = self.assistant.get_input('enter your note : ')
        return note
    def cmd_add_note(self):
        note = self.get_note()
        self.assistant.add_note(note)
        return True , ('note added')
    def get_index(self):
        while True:
            try:
                index = int( self.assistant.get_input('choose one : '))
                if not (1<= index <= len(self.assistant.note)):
                    raise ValueError
                return index
            except ValueError:
                print('enter number on the menu')
    def cmd_remove_note(self):
        if not self.assistant.is_empty:
            self.assistant.show_note()
            index = self.get_index()
            note = self.assistant.note[index - 1]
            self.assistant.remove_note(note)
            return True , ('note removed')
        else:
            return True , ('note is empty')
    def cmd_show_note(self):
        if self.assistant.show_note():
            return True , 'done'
        return True, "note is empty" 
class CalcMixin:
    def get_number(self):
        while True:
            try:
                num1 = int( self.assistant.get_input('enter first number : '))
                num2 = int( self.assistant.get_input('enter second number : '))
                return num1 , num2
            except ValueError:
                print('enter number')
    def get_operation(self):
        for item in self.operation_list:
            print(item)
        while True:
            try:
                get_op =  self.assistant.get_input('choose your opration : ')
                if get_op not in self.operation_list:
                    raise ValueError
                return get_op
            except ValueError:
                print('eneter opration frome list')
    def cmd_calc(self):
        while True:
            num1 , num2 = self.get_number()
            op = self.get_operation()
            try:
                if op == self.operation_list[0]:
                    if num2 == 0:
                        raise ZeroDivisionError
                    return True , num1 / num2
                if op == self.operation_list[1]:
                    return True , num1 * num2
                if op == self.operation_list[2]:
                    return True , num1 - num2
                if op == self.operation_list[3]:
                    return True , num1 + num2 
            except ZeroDivisionError:
                print('num2 cant be zero')
                continue
class TodoMixin:
    def cmd_add_todos(self):
        result = self.assistant.todos.add_todos()
        return True , 'Done'
    def cmd_remove_todos(self):
        result = self.assistant.todos.remove_todos()
        if not result:
            return True , 'to do list is empty'
        return True , 'Done'
    def cmd_show_todos(self):
        result = self.assistant.todos.show_todos()
        if not result:
            return True , 'to do list is empty'
        return True , 'Done'
    def cmd_toggle_status(self):
        result = self.assistant.todos.toggle_status()
        if not result:
           return True , 'to do list is empty'
        return True , 'Done'     
class RemindersMixin:
    def cmd_show_reminders(self):
        result = self.assistant.reminders.show_reminders()
        if result:
            return True ,'Done'
        return True, 'reminders list is empty'
    def cmd_add_reminders(self):
        result = self.assistant.reminders.add_reminders()
        return True , 'Done'
    def cmd_remove_reminders(self):
        result = self.assistant.reminders.remove_reminders()
        if not result:
           return True , 'reminders list is empty'
        return True ,' Done'
    def cmd_toggle_reminders(self):
        result = self.assistant.reminders.toggle_reminders()
        if not result:
           return True , 'reminders list is empty'
        return True ,' Done'
    def cmd_check_reminders(self):
        if self.assistant.reminders.is_empty:
            return True , 'reminders list is empty'
        overdue = self.assistant.reminders.check_reminders()
        if not overdue:
            return True ,  'no overdue reminders'
        output = " Overdue reminders:\n" + "\n".join(overdue)
        return True , output  