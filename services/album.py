from models.album import Album as AlbumModel
from schemas.album import Album

class AlbumService:
    def __init__(self, db) -> None:
        self.db = db

    def get_albumes(self):
        result = self.db.query(AlbumModel).all()
        return result

    def get_album(self, id):
        result = self.db.query(AlbumModel).filter(AlbumModel.id == id).first()
        return result
    
    def get_albus_by_genre(self, genre):
        result = self.db.query(AlbumModel).filter(AlbumModel.genre == genre).all()
        return result
    
    def create_album(self, album: Album):
        new_album = AlbumModel(**album.model_dump())
        self.db.add(new_album)
        self.db.commit()
        return
    
    def update_album(self, id: int, album: Album):
        album = self.db.query(AlbumModel).filter(AlbumModel.id == id).first()
        album.title = album.title
        album.artist = album.artist
        album.overview = album.overview
        album.year = album.year
        album.rating = album.rating
        album.genre = album.genre
        self.db.commit()
        return
    
    def delete_album(self, id: int):
        self.db.query(AlbumModel).filter(AlbumModel.id == id).delete()
        self.db.commit()
        return