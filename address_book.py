from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Dict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")      

class Name(Field):
    def __init__(self, value):
         super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not re.match(r'^\d{10}$', phone):
            raise ValueError("Invalid phone number format. Use 10 digits.")
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]
    
    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
        
    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            self.birthday = Birthday(birthday)
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name] 
        
    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        today = datetime.today().date()
        upcoming_birthdays=[]
        for record in self.data.values():
            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)
            
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)
                   
            if birthday_this_year.weekday() == 5:
                birthday_this_year += timedelta(days = 2)
            if birthday_this_year.weekday() == 6:
                birthday_this_year += timedelta(days = 1)
                
            days_to_birthday = (birthday_this_year - today).days
            
            if days_to_birthday <=7:
                upcoming_birthdays.append({
                    "name" : record.name.value,
                    "congratulation_date" : birthday_this_year.strftime("%Y.%m.%d") 
                })
        return upcoming_birthdays	