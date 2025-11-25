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
from .new_depallet_frontage_watcher import NewDepalletFrontegeWatcher, NewWatcherManager # TODO:

import application.utility as util

# デパレ作業アプリケーション
class DepalletApplication():

    def __init__(self):
        self.LINE_ID = (1, 2, 3, 4) #TODO: added 3,4
        self.PLAT_ID = (20, 21, 22, 23, 24, 25, 26, 27, 28, 29) # TODO: plat of maguchi 5,4,3,2,1 for both LINE A and B

        self._running  =True
        self.depallet_area = None
        self.new_depallet_area = None # TODO: added
        self.lines = None
        self.product_r = None
        self.product_l = None

        self.db = MysqlDb()

        self.depallet_service = DepalletService(DepalletAreaRepository(self.db), WcsControler(self.db))
        self.line_service = LineService(LineRepository(self.db), ProductInfoRepository(self.db))
        
        self.manager = WatcherManager()
        self.new_manager = NewWatcherManager() # TODO:

        self.lines = self.line_service.get_lines(self.LINE_ID)
        self.product_r, self.product_l = self.line_service.get_product_infos(self.lines)
        self.depallet_area = self.depallet_service.get_depallet_area(self.LINE_ID)
        self.new_depallet_area = self.depallet_service.update_depallet_area(self.PLAT_ID) # TODO: added

    def start(self):
        for frontage in self.depallet_area.frontages.values():
            watcher = DepalletFrontegeWatcher(frontage, self.depallet_service)
            self.manager.add_watcher(watcher)
        self.manager.start_all()

    def stop(self):
        self.manager.stop_all()

     # TODO: added 
    def new_start(self):
        for new_frontage in self.new_depallet_area.update_frontages.values():
            watcher = NewDepalletFrontegeWatcher(new_frontage, self.depallet_service)
            self.new_manager.add_watcher(watcher)
        self.new_manager.start_all()

    # TODO:
    def new_stop(self):
        self.new_manager.stop_all()

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
    def fetch_part(self, frontage_id:int, part_id:int):
        # print(f"[DepalletApplication >> fetch_part >> part_id ] : {part_id}")
        try:
            source = self.depallet_area.get_by_id(frontage_id)
            # print(f"[DepalletApplication >> fetch_part >> source ] : {source}")
            if source is None:
                raise Exception("No frontage found")
            
            dest = self.depallet_area.get_flow_rack_frontage()
            # print(f"[DepalletApplication >> fetch_part >> dest ] : {dest}")
            if dest is None:
                raise Exception("No flow rack frontage found")

            # part = source.shelf.get_by_kanban(part_id)
            part = source.shelf.get_by_kanban(part_id) # TODO: testing
            # print(f"[DepalletApplication >> fetch_part >> part ] : {part}")
            if part is None:
                raise Exception("No part found")
            
            self.depallet_service.depalletizing(source.shelf, dest.shelf, part)
           
        except Exception as e:
            raise Exception(f"Error depalletizing: {e}")
        
        
    def update_maguchi_signal_input(self, line_frontage_id):
        print("[DepalletApplication >> update_maguchi_signal_input >> line_frontage_id ]")
        try:
            self.depallet_service.update_maguchi_signal_input(line_frontage_id)
        except Exception as e:
            raise Exception(f"DepalletApplication >> update_maguchi_signal_input >> Error: {e}")

    def to_maguchi_set_values(self, line_frontage_id):
        print("[DepalletApplication >> to_maguchi_set_values >> line_frontage_id ] :")
        try:
            self.depallet_service.to_maguchi_set_values(line_frontage_id)
        except Exception as e:
            raise Exception(f"DepalletApplication >> to_maguchi_set_values >> Error: {e}")

     # コタツに部品を戻す
    def return_part(self, frontage_id:int, part_id:int):
        try:
            dest = self.depallet_area.get_by_id(frontage_id)
            # print(f"[return_part >> dest] : {dest}")

            if dest is None:
                raise Exception("No frontage found")
            
            source = self.depallet_area.get_flow_rack_frontage()
            # print(f"[return_part >> source] : {source}")

            if source is None:
                # print(f"[return_part >> source is None] : {source}")
                raise Exception("No flow rack frontage found")

            part = source.shelf.get_by_kanban(part_id)
            # print(f"[return_part >> part] : {part}")

            # Check if the part was actually found TODO: testing
            if part is None:
                # print(f"[return_part >> part is None] : {part}")
                raise Exception(f"Part with ID '{part_id}' not found in the source shelf.")
            
            self.depallet_service.depalletizing(source.shelf, dest.shelf, part)
           
        except Exception as e:
            # print(f"[return_part >> Error depalletizing] : {e}")
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
     
    def complete(self):
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
        return util.to_json(flow_rack_frontage.shelf)
    
    # TODO: Added 
    def update_depallet_area_json(self):
        return util.to_json(self.new_depallet_area)
    
    


if __name__ == "__main__":

   app = DepalletApplication()
   app.start()
   app.new_start()
   try:
        while True:
            sleep(1)
            print(app.get_lines_json())
            print("----------------------")
            print(app.get_depallet_area_json())
            print("----------------------")
            print(app.update_depallet_area_json())
            print("----------------------")
            print(app.get_product_infos_json())
   except KeyboardInterrupt:
       app.manager.stop_all()
       app.new_manager.stop_all()
       print("Stopped by user")

  


  