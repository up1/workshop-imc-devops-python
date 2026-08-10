from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.database.mysql import get_mysql_connection
from api.models.employee import EmployeeCreate, EmployeeResponse
from api.repositories.employee_repository import (
    EmployeeAlreadyExistsError,
    EmployeeRepository,
    MySQLEmployeeRepository,
)
from api.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/employees", tags=["employees"])


def get_employee_repository() -> EmployeeRepository:
    return MySQLEmployeeRepository(get_mysql_connection)


def get_employee_service(
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)],
) -> EmployeeService:
    return EmployeeService(repository)


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(
    employee: EmployeeCreate,
    service: Annotated[EmployeeService, Depends(get_employee_service)],
):
    try:
        return service.create_employee(employee)
    except EmployeeAlreadyExistsError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid request body"},
        )