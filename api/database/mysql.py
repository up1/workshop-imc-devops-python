import os

import mysql.connector
# from opentelemetry.instrumentation.mysql import MySQLInstrumentor

# MySQLInstrumentor().instrument()


def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "employee_user"),
        password=os.getenv("MYSQL_PASSWORD", "employee_password"),
        database=os.getenv("MYSQL_DATABASE", "employee_db"),
    )