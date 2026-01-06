from abc import abstractmethod, ABC

from domain.models.depallet import DepalletFrontage
from domain.models.part import Part
from domain.models.line import LineFrontage

class IWCSRepository(ABC):
    # ���i�v��
    @abstractmethod  # TODO modified
    def request_kotatsu(self, frontage: DepalletFrontage, part: Part):
        pass

    # �t���[���b�N�v��
    @abstractmethod  # TODO modified
    def request_flow_rack(self, frontage: DepalletFrontage, line_frontage: LineFrontage):
        pass

    # ���o
    @abstractmethod  # TODO modified
    def dispatch(self, frontage: DepalletFrontage):
        pass

    @abstractmethod  # TODO➞リン
    def insert_target_ids(self, button_id: int):
        pass

    @abstractmethod  # TODO➞リン
    def call_target_ids(self, button_id: int):
        pass

    # ���o
    @abstractmethod  # TODO modified
    def dispallet(self, depallet_area):
        pass

    # ���o
    @abstractmethod  # TODO modified
    def get_empty_kotatsu_status(self):
        pass

