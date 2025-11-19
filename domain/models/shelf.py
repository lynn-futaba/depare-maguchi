from abc import ABC, abstractmethod

from .part import Part, Inventory,KotatsuInventory

# Shelf Interface
class Shelf(ABC):
    def __init__(self, shelf_id:str,type:int):
        self.id = shelf_id 
        self.type = type  # 1:コタツ, 2:フローラック
        if self.validate() is False:
            raise ValueError("Invalid Shelf data.")

    def validate(self) -> bool:
        if len(self.id) > 10:
            return False
        return True

    @abstractmethod
    def is_empty(self)->bool:
         pass

    @abstractmethod
    def get_by_part_number(self,part_number:str)->Part:
         pass
    @abstractmethod
    def get_by_kanban(self,part_number:str)->Part:
        pass

    @abstractmethod
    def add(self,part:Part,count:int):
         pass

    @abstractmethod
    def remove(self,part:Part,count:int):
         pass

# コタツ ※複数の部品在庫を持つ
class Kotatsu(Shelf):
    def __init__(self, shelf_id:str,inventories:list[KotatsuInventory]):
        _type = 1
        super().__init__(shelf_id,_type)
        self.inventories = inventories

    def is_empty(self) -> bool:
        return all(inventory.is_empty() for inventory in self.inventories)

    def get_by_part_number(self, part_number: str)-> Part :
        for inventory in self.inventories:
            try:
                if inventory.part.id == part_number:
                    return inventory.part
            except Exception as e:
                raise Exception(f"Error getting part by id: {e}")
        return None

    def get_by_kanban(self, kanban: str)-> Part :
        for inventory in self.inventories:
            try:
                if inventory.part.kanban_id == kanban:
                    return inventory.part
            except Exception as e:
                raise Exception(f"Error getting part by id: {e}")
        return None

    def add(self,part:Part,count:int):
        for inventory in self.inventories:
            try:
                if inventory.part == part:
                    inventory.add(count)
                    return
            except Exception as e:
                raise Exception(f"Error adding part: {e}") 
        raise Exception("Part not found in inventory.")

    def remove(self, part: Part, count: int):
        for inventory in self.inventories:
            try:
                if inventory.part == part:
                    inventory.remove(count)
                    return
            except Exception as e:
                raise Exception(f"Error removing part: {e}")
        raise Exception("Part not found in inventory.")

# フローラック　※ラックとして4つの部品在庫を持つ
class FlowRack(Shelf):
    def __init__(self, shelf_id: str):
        _type = 2
        super().__init__(shelf_id,_type)
        #頭からrack_position_id=1,2,3,4　設定なしの場合はNoneが入る
        self.rack= []
        self.dest_line_frontage_id:int = 0

    def is_empty(self) -> bool:
        if len(self.rack) == 0:
            return True
        return all(inventory.is_empty() for inventory in self.rack)

    def get_by_part_number(self, part_number: str)-> Part :
        for inventory in self.rack:
            try:
                if inventory is None:
                    continue
                if inventory.part.id == part_number:
                    return inventory.part
            except Exception as e:
                raise Exception(f"Error getting part by id: {e}")

    def get_by_kanban(self, kanban: str)-> Part :
        for inventory in self.rack:
            try:
                if inventory.part.kanban_id == kanban:
                    return inventory.part
            except Exception as e:
                raise Exception(f"Error getting part by id: {e}")
        return None    

    def set_inventories(self, inventories: list[Inventory]): 
        if len(inventories) > 4:
            raise ValueError("A FlowRack can hold up to 4 inventories.")
        self.rack = inventories

    def add(self, part: Part, count: int):
        for inventory in self.rack:
            try:
                if inventory.part == part:
                    inventory.add(count)
                    return
            except Exception as e:
                raise Exception(f"Error adding part: {e}")
        raise Exception("Part not found in inventory.")

    def remove(self, part: Part, count: int):
        for inventory in self.rack:
            try:
                if inventory.part == part:
                    inventory.remove(count)
                    return
            except Exception as e:
                raise Exception(f"Error removing part: {e}")
        raise Exception("Part not found in inventory.")