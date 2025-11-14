from abc import ABC, abstractmethod

from domain.models.line import Line
from domain.models.shelf import FlowRack

class ILineRepository(ABC):

    # ライン情報取得
    @abstractmethod
    def get_lines(self,line_id_list:list)->list[Line]:
        pass

    @abstractmethod
    def supply_parts(self,flow_rack:FlowRack):
        pass





