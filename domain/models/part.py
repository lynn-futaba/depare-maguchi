#部品
class Part():
    def __init__(self,part_id:str,kanban_id:str,name:str,car_model_id:int):
        self.id = part_id 
        self.kanban_id = kanban_id
        self.name = name
        self.car_model_id = car_model_id
        if self.validate() is False:
            raise ValueError("Invalid Part data.")

    def validate(self) -> bool:
        if len(self.id)<=0:
            return False
        return True

    def __eq__(self, other):
        if other is None or not isinstance(other, Part): return False
        return self.id== other.id or self.kanban_id == other.kanban_id

# 部品在庫　※1種類の部品のみ
class Inventory():
    def __init__(self,id:int,part:Part,case_quantity:int):
        self.id = id
        if part is None:
            raise ValueError("Part cannot be None.")
        self.part =part
        self.case_quantity = case_quantity
        if self.validate_count(case_quantity) is False:
            raise ValueError("Invalid Inventory data.")

    def is_empty(self) -> bool:
       return self.case_quantity == 0

    # 追加・削除時は0より大きい数値のみ許可
    def validate_count(self, count) -> bool:
        return count >= 0

    def add(self, count: int):
        if not self.validate_count(count):
            raise ValueError("Count must be greater than zero.")
        self.case_quantity += count

    def remove(self, count: int):
        if not self.validate_count(count):
            raise ValueError("Count must be greater than zero.")
        
        if self.case_quantity < count:
            raise ValueError(
                "Insufficient inventory to remove the requested count.")
        self.case_quantity -= count

    def reset_count(self):
        self.case_quantity = 0

 # コタツ部品在庫　※信号IDと初期値も持つ
class KotatsuInventory(Inventory):
    def __init__(self, id: int, part: Part, case_quantity: int,
                 fetch_signal_id,fetch_count_signal_id,count_signal_id,part_no_signal_id):

        super().__init__(id, part, case_quantity)

        self.initial_quantity = case_quantity
        self.fetch_signal_id = fetch_signal_id
        self.fetch_count_signal_id = fetch_count_signal_id
        self.count_signal_id = count_signal_id # いらんかも
        self.part_no_signal_id = part_no_signal_id # いらんかも