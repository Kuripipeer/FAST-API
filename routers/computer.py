from fastapi import Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.computer import ComputerService
from schemas.computer import Computer

computer_router = APIRouter()

@computer_router.get('/computers', tags=['Computers'], response_model=List[Computer], status_code=200, dependencies=[Depends(JWTBearer())])
def get_computers() -> List[Computer]:
    db = Session()
    result = ComputerService(db).get_computers()
    return JSONResponse(status_code=200, content= jsonable_encoder(result))

@computer_router.get('/computers/{id}', tags=['Computers'], response_model=Computer, responses={404: {"description": "Computer not found"}}, dependencies=[Depends(JWTBearer())])
def get_computer(id: int = Path(ge=1, le=2000)) -> Computer:
    db = Session()
    result = ComputerService(db).get_computer(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Computer not found"})
    return JSONResponse(status_code=200, content= jsonable_encoder(result))

@computer_router.get('/computers/', tags=['Computers'], response_model=List[Computer], responses={404: {"description": "Computer not found"}}, dependencies=[Depends(JWTBearer())])
def get_computer_by_brand(brand: str = Query(min_length=1, max_length=25)) -> List[Computer]:
    db = Session()
    result = ComputerService(db).get_computer_by_brand(brand)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Computer not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@computer_router.post('/computers', tags=['Computers'], response_model= dict, status_code=201, dependencies=[Depends(JWTBearer())])
def crear_computer(computer: Computer) -> dict:
    db = Session()
    ComputerService(db).create_computer(computer)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la computadora"})

@computer_router.put('/computers/{id}', tags=['Computers'], response_model= dict, responses={404: {"description": "Computer not found"}}, dependencies=[Depends(JWTBearer())])
def update_computer (id: int, computer: Computer) -> dict:
    db = Session()
    result = ComputerService(db).get_computer(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Computer not found"})
    ComputerService(db).update_computer(id, computer)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la computadora"})

@computer_router.delete('/computers/{id}', tags=['Computers'], response_model= dict, responses={404: {"description": "Computer not found"}}, dependencies=[Depends(JWTBearer())])
def delete_computer(id: int):
    db = Session()
    result = ComputerService(db).get_computer(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Computer not found"})
    ComputerService(db).delete_computer(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la computadora"})
