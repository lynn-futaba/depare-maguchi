from time import sleep

from domain.models.line import LineFrontage
from domain.models.part import Part
from domain.models.shelf import Kotatsu,FlowRack

from domain.services.depallet_service import DepalletService
from domain.services.line_service import LineService

from infrastructure.mysql.depallet_area_repository import DepalletAreaRepository
from infrastructure.mysql.wcs_controler import WcsControler
from infrastructure.mysql.line_repository import LineRepository
from infrastructure.mysql.product_repository import ProductInfoRepository
from infrastructure.mysql.mysql_db import MysqlDb

from .depallet_frontage_watcher import DepalletFrontegeWatcher, WatcherManager

import application.utility as util

# デパレ作業アプリケーション
class DepalletApplication():

    def __init__(self):
        # self.LINE_ID = (1, 2)
        self.LINE_ID = (1, 2, 3, 4)
        self._running  =True
        self.depallet_area =None
        self.lines =None
        self.product_r = None
        self.product_l = None
        self.db = MysqlDb()
        # self.depallet_service = DepalletService(DepalletAreaRepository(self.db), WcsControler(self.db))
        # TODO: added try-except
        try:
            self.depallet_service = DepalletService(
                DepalletAreaRepository(self.db),
                WcsControler(self.db)
            )
        except Exception as e:
            import traceback
            print("Error initializing DepalletService:", e)
            traceback.print_exc()
            raise

        self.line_service = LineService(LineRepository(self.db), ProductInfoRepository(self.db))
        self.manager = WatcherManager()

        self.lines = self.line_service.get_lines(self.LINE_ID)
        self.product_r, self.product_l = self.line_service.get_product_infos(self.lines)
        self.depallet_area = self.depallet_service.get_depallet_area(self.LINE_ID)

    def start(self):
        for frontage in self.depallet_area.frontages.values():
            watcher = DepalletFrontegeWatcher(frontage, self.depallet_service)
            self.manager.add_watcher(watcher)
        self.manager.start_all()

    def stop(self):
        self.manager.stop_all()

    def update_line_data(self):
        self.lines = self.line_service.get_lines(self.LINE_ID)
        self.product_r, self.product_l = self.line_service.get_product_infos(self.lines)

    def depallet_start(self,line_frontage_id: int):
        self.request_target_flow_rack(line_frontage_id)
        self._request_target_kotatsu(line_frontage_id)
        
    def request_target_flow_rack(self, line_frontage_id: int):
          try:
              for line in self.lines:
                    line_frontage = line.get_by_id(line_frontage_id)
                    if line_frontage is not None:
                        break
              if line_frontage is None:
                  raise Exception("Line frontage not found")
              self.depallet_service.request_flow_rack(self.depallet_area, line_frontage)
          
          except Exception as e:
              raise Exception(f"Error requesting flow rack: {e}")

    def _request_target_kotatsu(self, line_frontage_id: int):
        try:
            for line in self.lines:
                    line_frontage = line.get_by_id(line_frontage_id)
                    if line_frontage is not None:
                        break
            if line_frontage is None:
                  raise Exception("Line frontage not found")
            self.depallet_service.request_parts(self.depallet_area, line_frontage)
        except Exception as e:
            raise Exception(f"Error requesting kotatsu: {e}")

    # フローラックに部品を置く
    def fetch_part(self, frontage_id:int,part_id:int):
        try:
            source = self.depallet_area.get_by_id(frontage_id)
            if source is None:
                raise Exception("No frontage found")
            dest = self.depallet_area.get_flow_rack_frontage()
            if dest is None:
                raise Exception("No flow rack frontage found")

            part = source.shelf.get_by_kanban(part_id)

            self.depallet_service.depalletizing(source.shelf, dest.shelf, part)
           
        except Exception as e:
            raise Exception(f"Error depalletizing: {e}")

     # コタツに部品を戻す
    def return_part(self, frontage_id:int,part_id:int):
        try:
            dest = self.depallet_area.get_by_id(frontage_id)
            if dest is None:
                raise Exception("No frontage found")
            source = self.depallet_area.get_flow_rack_frontage()
            if source is None:
                raise Exception("No flow rack frontage found")

            part = source.shelf.get_by_kanban(part_id)

            self.depallet_service.depalletizing(source.shelf, dest.shelf, part)
           
        except Exception as e:
            raise Exception(f"Error depalletizing: {e}")
        
    def return_kotatsu(self,frontage_id:int):
        try:
            frontage = self.depallet_area.get_by_id(frontage_id)
            if frontage is None:
                raise Exception("No frontage found")
            if frontage.shelf is None:
                raise Exception("No shelf in frontage")
            if not isinstance(frontage.shelf, Kotatsu):
                raise Exception("Shelf is not Kotatsu")
            self.depallet_service.dispatch(frontage)

        except Exception as e:
            raise Exception(f"Error returning kotatsu: {e}")
     
    def complate(self):
        try:
            flow_rack_frontage = self.depallet_area.get_flow_rack_frontage()
            if flow_rack_frontage is None:
                raise Exception("No flow rack frontage found")
            if flow_rack_frontage.shelf.is_empty():
                raise Exception("Flow rack is empty")
            self.line_service.supply_parts(flow_rack_frontage)
            self.depallet_service.dispatch(flow_rack_frontage)

            for frontage in self.depallet_area.frontages.values():
                if frontage.shelf is not None:
                    self.depallet_service.dispatch(frontage)
              
        except Exception as e:
            raise Exception(f"Error completing depalletizing: {e}")

    def get_lines_json(self):
        return util.to_json(self.lines)

    def get_product_infos_json(self):
        return util.to_json(self.product_l), util.to_json(self.product_r)

    def get_depallet_area_json(self):
        return util.to_json(self.depallet_area)

    def get_flow_rack_json(self):
        flow_rack_frontage = self.depallet_area.get_flow_rack_frontage()
        if  flow_rack_frontage is None:
            return "{}"
        return util.to_json( flow_rack_frontage.shelf)


if __name__ == "__main__":

   app = DepalletApplication()
   app.start()
   try:
        while True:
            sleep(1)
            print(app.get_lines_json())
            print("----------------------")
            print(app.get_depallet_area_json())
            print("----------------------")
            print(app.get_product_infos_json())
   except KeyboardInterrupt:
       app.manager.stop_all()
       print("Stopped by user")

  


  