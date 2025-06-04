from models.computer import Computer as ComputerModel
from schemas.computer import Computer

class ComputerService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_computers(self):
        result = self.db.query(ComputerModel).all()
        return result
    
    def get_computer(self, id):
        result = self.db.query(ComputerModel).filter(ComputerModel.id == id).first()
        return result
    
    def get_computer_by_brand(self, brand):
        result = self.db.query(ComputerModel).filter(ComputerModel.brand.ilike(brand)).all()
        return result
    
    def create_computer(self, computer):
        new_computer = ComputerModel(**computer.model_dump())
        self.db.add(new_computer)
        self.db.commit()
        return
    
    def update_computer(self, id: int, computer: Computer):
        comp = self.db.query(ComputerModel).filter(ComputerModel.id == id).first()
        comp.brand = computer.brand
        comp.model = computer.model
        comp.color = computer.color
        comp.ram = computer.ram
        comp.storage = computer.storage
        self.db.commit()
        return
    
    def delete_computer(self, id: int):
        self.db.query(ComputerModel).filter(ComputerModel.id == id).delete()
        self.db.commit()
        return