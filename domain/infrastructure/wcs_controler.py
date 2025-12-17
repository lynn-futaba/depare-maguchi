from abc import abstractmethod, ABC

from domain.models.depallet import DepalletFrontage
from domain.models.part import Part
from domain.models.line import LineFrontage


class IWcsControler(ABC):
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

