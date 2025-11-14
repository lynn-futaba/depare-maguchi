import copy

from domain.models.shelf import FlowRack
from domain.models.line import Line, LineFrontage
from domain.models.depallet import DepalletFrontage
from domain.models.product import Product, ProductInfo
from domain.infrastructure.line_repository import ILineRepository
from domain.infrastructure.product_repository import IProductInfoRepository
from domain.infrastructure.wcs_controler import IWcsControler

class LineService:

    def __init__(self,line_repo:ILineRepository,
                 product_info_repo:IProductInfoRepository):
        self.line_repo = line_repo
        self.product_info_repo = product_info_repo
    
    def get_lines(self,line_id_list)->list[Line]:
        try:
            if not line_id_list:
                raise Exception("line_id_list is empty")
            lines = self.line_repo.get_lines(line_id_list)
            return lines
        except Exception as e:
            raise Exception(f"Error loading lines: {e}")
        
    def get_product_infos(self, lines: list[Line]) -> tuple[ProductInfo, ProductInfo]:
        try:
            r = self.product_info_repo.get_product_info(lines[0].id)
            l = self.product_info_repo.get_product_info(lines[1].id)
            return l, r
        except Exception as e:
            raise Exception(f"Error getting product infos: {e}")
    
    # TODO: added this one to fix the LINE error
    # def get_product_infos(self, lines: list[Line]) -> tuple[ProductInfo, ProductInfo]:
    #     try:
    #         if len(lines) < 2:
    #             print("Warning: Less than 2 lines found, returning None.")
    #             return None, None
    #         r = self.product_info_repo.get_product_info(lines[0].id)
    #         l = self.product_info_repo.get_product_info(lines[1].id)
    #         return l, r
    #     except Exception as e:
    #         raise Exception(f"Error getting product infos: {e}")

    def supply_parts(self, frontage:DepalletFrontage):
       try:
           if frontage.shelf is None:
               raise Exception("Frontage shelf is None")
           self.line_repo.supply_parts(frontage.shelf)
       except Exception as e:
           raise Exception(f"Error supplying parts: {e}")


       
