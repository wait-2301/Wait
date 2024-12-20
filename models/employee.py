class Employee:
    def __init__(self, user_id, first_name, last_name, position, table_name, phone, password_hash):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.table_name = table_name
        self.phone = phone
        self.password_hash = password_hash