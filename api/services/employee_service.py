import logging

from api.models.employee import EmployeeCreate, EmployeeResponse
from api.repositories.employee_repository import EmployeeRepository

logger = logging.getLogger(__name__)


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def create_employee(self, employee: EmployeeCreate) -> EmployeeResponse:
        logger.debug("Creating employee %s", employee.email)
        return self.repository.create(employee)