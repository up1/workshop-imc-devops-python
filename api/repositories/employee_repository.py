from collections.abc import Callable
from typing import Protocol

from mysql.connector import IntegrityError

from api.models.employee import EmployeeCreate, EmployeeResponse


class EmployeeAlreadyExistsError(Exception):
    pass


class EmployeeRepository(Protocol):
    def create(self, employee: EmployeeCreate) -> EmployeeResponse: ...


class MySQLEmployeeRepository:
    def __init__(self, connection_factory: Callable):
        self.connection_factory = connection_factory

    def create(self, employee: EmployeeCreate) -> EmployeeResponse:
        connection = self.connection_factory()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO employees (name, email, position)
                VALUES (%s, %s, %s)
                """,
                (employee.name, str(employee.email), employee.position),
            )
            connection.commit()
            return EmployeeResponse(id=cursor.lastrowid, **employee.model_dump())
        except IntegrityError as exc:
            connection.rollback()
            if exc.errno == 1062:
                raise EmployeeAlreadyExistsError from exc
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()