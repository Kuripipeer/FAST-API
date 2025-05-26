from fastapi import FastAPI, HTTPException, Path, Query, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.album import Album as AlbumModel
from fastapi.encoders import jsonable_encoder

class User(BaseModel):
    email: str
    password: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales Invalidas")


app = FastAPI()
app.title = "Mi primera aplicación con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class Album(BaseModel):
    id: Optional[int] | None # Indicamos que es opcional
    title: str = Field(min_length=5, max_length=15)
    artist: str = Field(max_length=30)
    overview: str = Field(min_length=5, max_length=40)
    year: int = Field(le=2025)
    rating: float = Field(ge=1, le=10)
    genre: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi album",
                "artist": "Interprete",
                "overview": "Descripción",
                "year": 2025,
                "rating": 9.9,
                "genre": "Alternative"
            }
        }

albums = [
    {
        "id": 1,
        "title": "DAMN",
        "artist": "Kendrick Lamar",
        "overview": "Damn (estilizado como DAMN.; en español: Maldición) es el cuarto álbum de estudio del rapero estadounidense Kendrick Lamar. Fue publicado el 14 de abril de 2017 por Top Dawg Entertainment, Aftermath Entertainment e Interscope Records.​",
        "year": 2017,
        "rating": 10,
        "genre": "RAP"
    },
    {
        "id": 2,
        "title": "FOUR",
        "artist": "One direction",
        "overview": "Four es el cuarto álbum de estudio del grupo británico-irlandés One Direction, el cual fue lanzado el 17 de noviembre de 2014.",
        "year": 2014,
        "rating": 9,
        "genre": "POP"
    },
    {
        "id": 3,
        "title": "Rumours",
        "artist": "Fleetwood Mac",
        "overview": "Rumours es el undécimo álbum de estudio de la banda de rock anglo-estadounidense Fleetwood Mac, publicado el 4 de febrero de 1977.",
        "year": 1977,
        "rating": 9.5,
        "genre": "Rock"
    },
    {
        "id": 4,
        "title": "Sheer Heart Attack",
        "artist": "Queen",
        "overview": "Sheer Heart Attack es el tercer álbum de estudio de la banda británica de rock Queen, publicado en noviembre de 1974.",
        "year": 1974,
        "rating": 2,
        "genre": "Rock"
    },
    {
        "id": 5,
        "title": "Data",
        "artist": "Tainy",
        "overview": "Data es el primer álbum de estudio en solitario, y el segundo en su carrera musical, del productor discográfico y compositor puertorriqueño Tainy, incluyendo su previa colaboración en el álbum Dynasty con Yandel",
        "year": 2023,
        "rating": 10,
        "genre": "Latino"
    },
    {
        "id": 6,
        "title": "Teatro d'ira: Vol. I",
        "artist": "Måneskin",
        "overview": "Teatro d'ira: Vol. I es el segundo álbum de estudio de la banda de rock italiana Måneskin, lanzado el 19 de marzo de 2021.",
        "year": 2021,
        "rating": 9.8,
        "genre": "Rock"
    },
    {
        "id": 7,
        "title": "I Said I Love You First",
        "artist": "Selena Gomez & Benny Blanco",
        "overview": "I Said I Love You First is a collaborative studio album by American singer Selena Gomez and American record producer Benny Blanco.",
        "year": 2025,
        "rating": 8.8,
        "genre": "Pop"
    },
    {
        "id": 8,
        "title": "Demons Days",
        "artist": "Gorillaz",
        "overview": "Demon Days es el segundo álbum de estudio de la banda virtual británica Gorillaz, lanzado el 11 de mayo de 2005.",
        "year": 2004,
        "rating": 9,
        "genre": "Rock Alternativo"
    },
    {
        "id": 9,
        "title": "Evolve",
        "artist": "Imagin Dragons",
        "overview": "Evolve es el tercer álbum de estudio de la banda estadounidense de rock Imagine Dragons, lanzado el 23 de junio de 2017.",
        "year": 2017,
        "rating": 10,
        "genre": "Rock"
    },
    {
        "id": 10,
        "title": "Astroworld",
        "artist": "Travis Scott",
        "overview": "Astroworld es el tercer álbum de estudio del rapero estadounidense Travis Scott, lanzado el 3 de agosto de 2018.",
        "year": 2019,
        "rating": 10,
        "genre": "Hip-Hop"
    }
]

@app.get("/", tags=['Home'])
def message():
    return "Hello, World!"

@app.get('/albums', tags=['Albums'], response_model= List[Album], status_code=200, dependencies=[Depends(JWTBearer())])
def get_albums() -> List[Album]:
    db = Session()
    result = db.query(AlbumModel).all()
    return JSONResponse(status_code=200, content= jsonable_encoder(result))

@app.get('/albums/{id}', tags=['Albums'], response_model=Album)
def get_album(id: int = Path(ge=1, le=2000)) -> Album:
    db = Session()
    result = db.query(AlbumModel).filter(AlbumModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Album not found"})
    return JSONResponse(status_code=200,content= jsonable_encoder(result))

@app.get('/albums/', tags=['Albums'], response_model=List[Album])
def get_album_by_genre(genero: str = Query(min_length=3, max_length=15)) -> List[Album]:
    data = [item for item in albums if item['genre'] == genero]
    return JSONResponse(content = data)

@app.post('/albums', tags=['Albums'], response_model = dict, status_code=201)
def crear_album (album: Album) -> dict:
    db = Session()
    # Utilizamos el modelo y le pasamos la información a registrar
    new_album = AlbumModel(**album.model_dump())
    # Ahora desde la BD añadimos el Album
    db.add(new_album)
    #Guardamos los datos
    db.commit()
    albums.append(album)
    return JSONResponse(status_code=201,content = {"message" : "Se ha registrado el album"})

@app.put('/albums/{id}', tags=['Albums'], response_model = dict, status_code=200)
def update_album (id: int, album: Album) -> dict:
    for item in albums:
        if item['id'] == id:
            item['title'] = album.title
            item['artist'] = album.artist
            item['overview'] = album.overview
            item['year'] = album.year
            item['rating'] = album.rating
            item['genre'] = album.genre
            return JSONResponse(status_code=200,content={"message":"Se ha actualizado el album"})
    return JSONResponse(content=[])

@app.delete('/albums/{id}', tags=['Albums'], response_model= dict, status_code=200)
def delete_album(id: int) -> dict:
    for item in albums:
        if item['id'] == id:
            albums.remove(item)
            return JSONResponse(status_code=200,content={"message":"Se ha eliminado el album"})
    return JSONResponse(content=[])

# Realiza los endpoints para la venta de computadoras con una lista de 10 registros con los siguientes atributos:
# - id
# - brand
# - model
# - color
# - ram
# - storage
# - realiza los endpoints ya hechos en clase en lugar de get_by_genre seria get_by_brand de manera que se obtenga todo el cuerpo de la computadora por la brand
# en caso de se mas de una mostrara toas las que sean de la misma brand

class Computer(BaseModel):
    brand: str = Field(min_length=1, max_length=15)
    model: str = Field(max_length=30)
    color: str = Field(min_length=3, max_length=15)
    ram: str = Field(min_length=1, max_length=8)
    storage: str = Field(min_length=1, max_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "brand": "HP",
                "model": "Pavilion",
                "color": "Black",
                "ram": "16 GB",
                "storage" : "1TB"
            }
        }

computers = [
    {
        "id": 1,
        "brand": "HP",
        "model": "Pavilion",
        "color": "Negro",
        "ram": "8GB",
        "storage": "1TB"
    },
    {
        "id": 2,
        "brand": "HP",
        "model": "Omen",
        "color": "Negro",
        "ram": "16GB",
        "storage": "2TB"
    },
    {
        "id": 3,
        "brand": "HP",
        "model": "Spectre",
        "color": "Plata",
        "ram": "16GB",
        "storage": "1TB"
    },
    {
        "id": 4,
        "brand": "Dell",
        "model": "Inspiron",
        "color": "Negro",
        "ram": "8GB",
        "storage": "1TB"
    },
    {
        "id": 5,
        "brand": "Dell",
        "model": "XPS",
        "color": "Rojo",
        "ram": "16GB",
        "storage": "1TB"
    },
    {
        "id": 6,
        "brand": "Dell",
        "model": "Alienware",
        "color": "Azul",
        "ram": "32GB",
        "storage": "2TB"
    },
    {
        "id": 7,
        "brand": "Lenovo",
        "model": "IdeaPad",
        "color": "Verde",
        "ram": "8GB",
        "storage": "1TB"
    },
    {
        "id": 8,
        "brand": "Lenovo",
        "model": "Legion",
        "color": "Negro",
        "ram": "16GB",
        "storage": "1TB"
    },
    {
        "id": 9,
        "brand": "Lenovo",
        "model": "ThinkPad",
        "color": "Negro",
        "ram": "32GB",
        "storage": "2TB"
    },
    {
        "id": 10,
        "brand": "Apple",
        "model": "MacBook Air",
        "color": "Gris",
        "ram": "8GB",
        "storage": "256GB"
    },
    {
        "id": 11,
        "brand": "Apple",
        "model": "MacBook Pro",
        "color": "Gris",
        "ram": "16GB",
        "storage": "1TB"
    }
] 

@app.get('/computers', tags=['Computers'], response_model=List[Computer], status_code=200)
def get_computers() -> List[Computer]:
    return JSONResponse(status_code=200, content=computers)

@app.get('/computers/{id}', tags=['Computers'], response_model=Computer, responses={404: {"description": "Computer not found"}})
def get_computer(id: int = Path(ge=1, le=2000)) -> Computer:
    for computer in computers:
        if computer['id'] == id:
            return JSONResponse(status_code=200, content=computer)
    return JSONResponse(status_code=404, content= [])

@app.get('/computers/', tags=['Computers'], response_model=List[Computer], responses={404: {"description": "Computer not found"}})
def get_computer_by_brand(brand: str = Query(min_length=1, max_length=25)) -> List[Computer]:
    results = []
    for computer in computers:
        if computer['brand'].lower() == brand.lower():
            results.append(computer)
    if not results:
        return JSONResponse(status_code=404, content= [])
    return JSONResponse(status_code=200, content=results)

@app.post('/computers', tags=['Computers'], response_model= dict, status_code=201)
def crear_computer(computer: Computer) -> dict:
    new_id = max([comp['id'] for comp in computers], default=0) + 1
    computer_dict = {"id" : new_id}
    computer_dict.update(computer.dict())
    computers.append(computer_dict)
    return JSONResponse(status_code=201, content = {"message" : "Se ha registrado la computadora"})

@app.put('/computers/{id}', tags=['Computers'], response_model= dict, responses={404: {"description": "Computer not found"}})
def update_computer (id: int, computer: Computer) -> dict:
    for item in computers:
        if item['id'] == id:
            item['brand'] = computer.brand
            item['model'] = computer.model
            item['color'] = computer.color
            item['ram'] = computer.ram
            item['storage'] = computer.storage
            return JSONResponse(status_code=200, content={"message":"Se ha actualizado la computadora"})
    return JSONResponse(status_code=404, content={"message":"No se ha encontrado la computadora"})

@app.delete('/computers/{id}', tags=['Computers'], response_model= dict, responses={404: {"description": "Computer not found"}})
def delete_computer(id: int):
    for item in computers:
        if item['id'] == id:
            computers.remove(item)
            return JSONResponse(status_code=200, content={"message":"Se ha eliminado la computadora"})
    return JSONResponse(status_code=404, content={"message":"No se ha encontrado la computadora"})

@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token : str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


# uvicorn main:app --reload --port 8000 --host 0.0.0.0 -m -> python3 venv venv -> source venv/bin/activate -> pip install fastapi -> pip install uvicorn -> uvicorn main:app --reload --port 8000 --host 0.0.0.0 -> Deactivate