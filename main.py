from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        self.validate_phone(phone)
        super().__init__(phone)

    def validate_phone(self, phone):
        if not (phone.isdigit() and len(phone) == 10):
            raise ValueError('Phone is not valid')


class Birthday(Field):
    def __init__(self, birthday):
        self.validate_birthday(birthday)
        super().__init__(birthday)

    def validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Birthday is not valid. Please use the format YYYY-MM-DD')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        valid_phone = Phone(phone)
        self.phones.append(valid_phone)

    def remove_phone(self, phone):
        valid_phone = Phone(phone)
        if any(valid_phone.value == p.value for p in self.phones):
            self.phones = [p for p in self.phones if valid_phone.value != p.value]
        else:
            raise ValueError(f"Phone ({phone}) not found in the record")

    def edit_phone(self, old_phone_value, new_phone_value):
        old_phone = Phone(old_phone_value)
        if any(old_phone.value == p.value for p in self.phones):
            self.phones = [Phone(new_phone_value) if p.value == old_phone.value else p for p in self.phones]
        else:
            raise ValueError(f"Phone ({old_phone_value}) not found in the record")

    def find_phone(self, phone):
        valid_phone = Phone(phone)
        return next((p for p in self.phones if p.value == valid_phone.value), None)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            return (next_birthday - today).days
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record
        else:
            raise ValueError("Here you can add only records")

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            print(f"This contact doesn't exist")

    def __iter__(self):
        return iter(self.data.values())

    def iterator(self, batch_size=5):
        for i in range(0, len(self.data), batch_size):
            yield list(self.data.values())[i:i + batch_size]
