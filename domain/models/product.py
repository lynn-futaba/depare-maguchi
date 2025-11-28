# 製品
class Product():

    def __init__(self, id:str, kanban_id:str, line_id:int, name:str):

        self.id = id  # product_id
        self.kanban_id = kanban_id  # 背番号
        self.line_id = line_id  # 生産ラインID
        self.name = name  # 製品名

        if self.validate() is False:
            raise ValueError("Invalid Product data.")

    def validate(self) -> bool:
        if len(self.id) <= 0 or self.line_id <= 0 or len(self.kanban_id) <= 0:
            return False
        return True

#生産情報
class ProductInfo():

    def __init__(self, product:Product, name:str, output_num:int=0, planned_num:int=0):
        self.product = product
        self.planned_num = planned_num  #計画台数 (デフォルト0)
        self.output_num = output_num  # 実績台数 (デフォルト0)
        
        if self.validate() is False:
            raise ValueError("Invalid ProductInfo data.")

    def validate(self) -> bool:
        if self.planned_num < 0 or self.output_num < 0:
            return False
        return True


    




