from api.models.employee import EmployeeCreate, EmployeeResponse
from api.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def create_employee(self, employee: EmployeeCreate) -> EmployeeResponse:
        return self.repository.create(employee)