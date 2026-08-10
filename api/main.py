from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.controllers.employee_controller import router as employee_router

app = FastAPI()
app.include_router(employee_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, _exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    _request: Request, _exc: Exception
) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/")
def read_root():
    return {"status": "FastAPI is running"}
