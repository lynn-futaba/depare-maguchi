from .shelf import Shelf

#�f�p���Ԍ�
class DepalletFrontage():
    
    def __init__(self, cell_code:str,frontage_id: int,name:str,priority:int):
        self.cell_code = cell_code
        self.name = name
        self.id = frontage_id
        self.shelf = None
        self.priority = priority
        self.signals = {}
        self.status = 0    # 0:empty�A1:booking�A2:using

        if not self.validate():
            raise ValueError("Invalid cell code format.")

    def is_using(self):
        if self.status == 2:
            return True
        return False

    def is_booking(self):
        if self.status == 1:
            return True
        return False

    def validate(self):
        if len(self.cell_code) >8:
            return False
        return True

    def set_shelf(self, shelf: Shelf):
        self.shelf = shelf
        self.status = 2

    def remove_shlef(self):
        self.shelf = None
        self.status = 0

# �f�p���G���A�i�Ԍ��O���[�v�j
class DepalletArea():
    def __init__(self,name):
        self.name=name
        self.frontages={}
       
    def register_frontage(self, frontage: DepalletFrontage):
        self.frontages[frontage.id] = frontage

    def get_by_id(self, id) -> DepalletFrontage | None:
        try:
            # print(f"[DepalletArea model >> get_by_id] : {id}")
            frontage = self.frontages[id]
            # print(f"[DepalletArea model >> frontage] : {frontage}")
            return frontage
        except KeyError:
            return None

    def get_flow_rack_frontage(self) -> DepalletFrontage | None:
        # print(f"[DepalletArea model >> get_flow_rack_frontage >> frontages] : {self.frontages.values()}")
        for frontage in self.frontages.values():
            # print(f"[DepalletArea model >> get_flow_rack_frontage >> frontage] : {frontage}")
            if frontage.shelf is not None and frontage.shelf.type == 2:
                return frontage
        return None

    def get_empty_frontage(self)->DepalletFrontage | None:
        # priority�Ń\�[�g���āA�D��x�̍������Ɏ擾
        sorted_frontages = sorted(
            self.frontages.values(), key=lambda f: f.priority)
        for frontage in sorted_frontages:
            if not frontage.is_using() and not frontage.is_booking():
                return frontage



