from fastapi import Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.album import AlbumService
from schemas.album import Album

album_router = APIRouter()

@album_router.get('/albums', tags=['Albums'], response_model= List[Album], status_code=200, dependencies=[Depends(JWTBearer())])
def get_albums() -> List[Album]:
    db = Session()
    result = AlbumService(db).get_albumes()
    return JSONResponse(status_code=200, content= jsonable_encoder(result))

@album_router.get('/albums/{id}', tags=['Albums'], response_model=Album, dependencies=[Depends(JWTBearer())])
def get_album(id: int = Path(ge=1, le=2000)) -> Album:
    db = Session()
    result = AlbumService(db).get_album(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Album not found"})
    return JSONResponse(status_code=200,content= jsonable_encoder(result))

@album_router.get('/albums/', tags=['Albums'], response_model=List[Album], dependencies=[Depends(JWTBearer())])
def get_album_by_genre(genero: str = Query(min_length=3, max_length=15)) -> List[Album]:
    db =  Session()
    result = AlbumService(db).get_albus_by_genre(genero)
    return JSONResponse(status_code=200, content = jsonable_encoder(result))

@album_router.post('/albums', tags=['Albums'], response_model = dict, status_code=201, dependencies=[Depends(JWTBearer())])
def crear_album (album: Album) -> dict:
    db = Session()
    AlbumService(db).create_album(album)
    return JSONResponse(status_code=201,content = {"message" : "Se ha registrado el album"})

@album_router.put('/albums/{id}', tags=['Albums'], response_model = dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_album (id: int, album: Album) -> dict:
    db = Session()
    result = AlbumService(db).get_album(id, album)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Album not found"})
    AlbumService(db).update_album(id, album)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el album"})

@album_router.delete('/albums/{id}', tags=['Albums'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_album(id: int) -> dict:
    db = Session()
    result = AlbumService(db).get_album(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Album not found"})
    AlbumService(db).delete_album(id)
    return JSONResponse(status_code=200, content={"message": "Se ha Eliminado el album"})