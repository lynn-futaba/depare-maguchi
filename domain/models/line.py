from domain.models.part import Inventory

#ライン供給間口
class LineFrontage():
    def __init__(self, cell_code:str,name:str, frontage_id:int,car_model_id:int):
        self.name = name
        self.id = frontage_id
        self.car_model_id = car_model_id
        self.inventories =[]
        # if not self.validate():
        #     raise ValueError("Invalid cell code format.")

    # def validate(self):
    #     if len(self.cell_code) > 8:
    #         return False
    #     return True
    def set_inventories(self, inventories: list[Inventory]):
        self.inventories = inventories

#ライン
class Line():
    def __init__(self, id, name, process):
        self.id = id
        self.name = name
        self.frontages= {}
        self.process= process
       
    def register_frontage(self, frontage:LineFrontage):
        self.frontages[frontage.name] = frontage
        
    def get_by_name(self, name) -> LineFrontage | None:
        try:
            frontage = self.frontages[name]
            return frontage
        except KeyError:
            return None

    def get_by_id(self, id) -> LineFrontage | None:
        try:
           for frontage in self.frontages.values():
               if frontage.id == id:
                    return frontage
        except KeyError:
            return None

