import repository.employee_repository as er

def get_all_employee_service():
    return er.get_all_employee()

def get_employee_by_id_service(id):
    return er.get_employee_by_id(id)

def get_employee_by_phone_service(phone):
    return er.get_employee_by_phone(phone)