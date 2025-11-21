from abc import abstractmethod, ABC

from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.line import LineFrontage
from domain.models.shelf import Kotatsu, FlowRack, Shelf

class IDepalletAreaRepository(ABC):
    # デパレタイズエリア情報取得
    @abstractmethod # TODO
    def get_depallet_area(self,line_id_list:list)->DepalletArea:
       pass
    
    # デパレ間口の状態取得
    @abstractmethod # TODO
    def is_frontage_ready(self, frontage:DepalletFrontage)->bool:
        pass
    # コタツ保存

    @abstractmethod # TODO
    def save_kotatsu(self, shelf: Kotatsu):
        pass
    # コタツ取得

    @abstractmethod # TODO
    def get_kotatsu(self, frontage: DepalletFrontage) -> Kotatsu:
        pass

    @abstractmethod # TODO
    def get_flow_rack(self,frontage:LineFrontage)->FlowRack:
        pass

    @abstractmethod # TODO
    def update_maguchi_signal_input(self, line_frontage_id: int):
        pass

    @abstractmethod # TODO
    def to_maguchi_set_values(self, line_frontage_id: int):
        pass
      

   




