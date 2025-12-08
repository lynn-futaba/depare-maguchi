import copy

from domain.models.shelf import FlowRack
from domain.models.line import Line, LineFrontage
from domain.models.depallet import DepalletFrontage
from domain.models.product import Product, ProductInfo
from domain.infrastructure.line_repository import ILineRepository
from domain.infrastructure.product_info_repository import IProductInfoRepository
from domain.infrastructure.wcs_controler import IWcsControler

from typing import Sequence, Tuple

class LineService:

    def __init__(self,line_repo: ILineRepository, product_info_repo: IProductInfoRepository):
        self.line_repo = line_repo
        self.product_info_repo = product_info_repo
    
    def get_lines(self, line_id_list)->list[Line]:
        try:
            if not line_id_list:
                raise Exception("line_id_list is empty")
            lines = self.line_repo.get_lines(line_id_list)
            return lines
        except Exception as e:
            raise Exception(f"Error loading lines: {e}")
        
    def get_product_infos(self, lines: Sequence[Line]) -> tuple[ProductInfo, ProductInfo, ProductInfo, ProductInfo]:
        
        if lines is None:
            raise ValueError("get_product_infos: 'lines' is None. Load lines before calling this method.")
        if len(lines) < 4:
            ids = [getattr(l, "id", None) for l in lines]
            raise ValueError(
                f"get_product_infos: expected 4 lines (A_R, A_L, B_R, B_L) but got {len(lines)}. "
                f"Received IDs={ids}. Check line-loading logic."
            )

        try:
            a_product_r = self.product_info_repo.get_product_info(lines[0].id) # TODO➞リン: a_product_r, Aライン R
            a_product_l = self.product_info_repo.get_product_info(lines[1].id) # TODO➞リン: a_product_l, Aライン L
            b_product_r = self.product_info_repo.get_product_info(lines[2].id) # TODO➞リン: b_product_r, Bライン R
            b_product_l = self.product_info_repo.get_product_info(lines[3].id) # TODO➞リン: b_product_l, Bライン L
            return a_product_r, a_product_l, b_product_r, b_product_l  # TODO➞リン: l,r to a_product_r, a_product_l, b_product_r, b_product_l
        except Exception as e:
            ids = [getattr(l, "id", None) for l in lines]
            # Preserve original stack to see exactly where it failed
            raise RuntimeError(f"get_product_infos: repo call failed for line IDs={ids}")


    def supply_parts(self, frontage:DepalletFrontage):
       try:
           if frontage.shelf is None:
               raise Exception("Frontage shelf is None")
           self.line_repo.supply_parts(frontage.shelf)
       except Exception as e:
           raise Exception(f"Error supplying parts: {e}")


       
