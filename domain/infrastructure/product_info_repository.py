from abc import ABC,abstractmethod

from ..models.product import ProductInfo, Product

class IProductInfoRepository(ABC):

    # 製品取得
    @abstractmethod
    def get_product(self, line_id:int)->Product:
        pass
    
    # 製品実績情報取得
    @abstractmethod
    def get_product_info(self, line_id:int)->ProductInfo:
        pass


   




