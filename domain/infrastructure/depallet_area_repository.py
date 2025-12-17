from abc import abstractmethod, ABC

from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.line import LineFrontage
from domain.models.shelf import Kotatsu, FlowRack, Shelf


class IDepalletAreaRepository(ABC):
    # デパレタイズエリア情報取得
    @abstractmethod  # TODO➞リン
    def get_depallet_area(self, line_id_list: list) -> DepalletArea:
        pass

    # デパレ間口の状態取得
    @abstractmethod  # TODO➞リン
    def is_frontage_ready(self, frontage: DepalletFrontage)->bool:
        pass
    # コタツ保存

    @abstractmethod  # TODO➞リン
    def save_kotatsu(self, shelf: Kotatsu):
        pass
    # コタツ取得

    @abstractmethod  # TODO➞リン
    def get_kotatsu(self, frontage: DepalletFrontage) -> Kotatsu:
        pass

    @abstractmethod  # TODO➞リン
    def get_flow_rack(self, frontage: LineFrontage) -> FlowRack:
        pass

    @abstractmethod  # TODO➞リン
    def insert_target_ids(self, line_frontage_id: int):
        pass

    @abstractmethod  # TODO➞リン
    def call_target_ids(self, line_frontage_id: int):
        pass

    @abstractmethod  # TODO➞リン: added
    def get_depallet_area_by_plat(self, plat_list, button_id: int) -> DepalletArea:
        pass

    @abstractmethod  # TODO➞リン: added
    def call_AMR_return(self, line_frontage_id: int):
        pass

    @abstractmethod  # TODO➞リン: added
    def insert_kanban_nuki(self):
        pass

    @abstractmethod  # TODO➞リン: added
    def insert_kanban_sashi(self):
        pass

    

    
      

   




