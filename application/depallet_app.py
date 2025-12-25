from time import sleep

from domain.models.line import LineFrontage
from domain.models.part import Part
from domain.models.shelf import Kotatsu,FlowRack

from domain.services.depallet_service import DepalletService
from domain.services.line_service import LineService
from domain.services.wcs_service import WCSService


from infrastructure.mysql.depallet_area_repository import DepalletAreaRepository
from infrastructure.mysql.wcs_repository import WCSRepository
from infrastructure.mysql.line_repository import LineRepository
from infrastructure.mysql.product_info_repository import ProductInfoRepository
from infrastructure.mysql.mysql_db import MysqlDb

from .depallet_frontage_watcher import DepalletFrontegeWatcher, WatcherManager
from .new_depallet_frontage_watcher import NewDepalletFrontegeWatcher, NewWatcherManager # TODO➞リン:
from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS, LOG_FOLDER, LOG_FILE  # ログ用

import logging
import application.utility as util

# ログ出力開始
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)


# デパレ作業アプリケーション
class DepalletApplication():

    def __init__(self):
        self.LINE_ID = (1, 2, 3, 4)  # TODO: added 3,4
        self.PLAT_ID_LIST = (29, 28, 27, 26, 25, 24, 23, 22, 21, 20)  # TODO➞リン: plat of maguchi 5,4,3,2,1 for both LINE A and B
        self.button_id = 0  # TODO➞リン: button id from R1, R2, R3, L1, L2, L3 for both A and B Line from frontend

        self._running = True
        self.depallet_area = None
        self.new_depallet_area = None  # TODO➞リン: added
        self.lines = None
        self.product_r = None
        self.product_l = None

        self.db = MysqlDb()

        self.depallet_service = DepalletService(DepalletAreaRepository(self.db), WCSRepository(self.db))

        self.wcs_service = WCSService(WCSRepository(self.db))

        # self.depallet_support = WCSRepository(self.db)
        self.line_service = LineService(LineRepository(self.db), ProductInfoRepository(self.db))

        self.manager = WatcherManager()
        self.new_manager = NewWatcherManager()  # TODO➞リン:

        self.lines = self.line_service.get_lines(self.LINE_ID)
        self.a_product_r, self.a_product_l, self.b_product_r, self.b_product_l = self.line_service.get_product_infos(self.lines)

        self.depallet_area = self.depallet_service.get_depallet_area(self.LINE_ID)
        self.new_depallet_area = self.depallet_service.get_depallet_area_by_plat(self.PLAT_ID_LIST) # TODO➞リン: added

    def start(self):
        for frontage in self.depallet_area.frontages.values():
            watcher = DepalletFrontegeWatcher(frontage, self.depallet_service)
            self.manager.add_watcher(watcher)
        self.manager.start_all()

    def stop(self):
        self.manager.stop_all()

    # TODO➞リン: added
    def new_start(self):
        logging.info(f"[DepalletApplication >> self.new_depallet_area.update_frontages.values() ] : {self.new_depallet_area.update_frontages.values()}")
        for new_frontage in self.new_depallet_area.update_frontages.values():
            watcher = NewDepalletFrontegeWatcher(new_frontage, self.depallet_service)
            self.new_manager.add_watcher(watcher)
        self.new_manager.start_all()

    # TODO➞リン:
    def new_stop(self):
        self.new_manager.stop_all()

    def update_line_data(self):
        self.lines = self.line_service.get_lines(self.LINE_ID)
        self.a_product_r, self.a_product_l, self.b_product_r, self.b_product_l = self.line_service.get_product_infos(self.lines)

    def depallet_start(self, line_frontage_id: int):
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
    def fetch_part(self, frontage_id: int, part_id: int):
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
            part = source.shelf.get_by_kanban(part_id) # TODO➞リン: testing
            # print(f"[DepalletApplication >> fetch_part >> part ] : {part}")
            if part is None:
                raise Exception("No part found")

            self.depallet_service.depalletizing(source.shelf, dest.shelf, part)

        except Exception as e:
            raise Exception(f"Error depalletizing: {e}")

    def insert_target_ids(self, button_id):
        try:
            self.wcs_service.insert_target_ids(button_id)
            logging.info("[DepalletApplication >> insert_target_ids() >> 成功]")
        except Exception as e:
            logging.error(f"[DepalletApplication >> insert_target_ids() >> エラー]: {e}")
            raise Exception(f"DepalletApplication >> insert_target_ids >> エラー]: {e}")

    def call_target_ids(self, button_id):
        try:
            logging.info("[DepalletApplication >> call_target_ids() >> 成功]")
            self.wcs_service.call_target_ids(button_id)
        except Exception as e:
            logging.error(f"[DepalletApplication >> call_target_ids() >> エラー] : {e}")
            raise Exception(f"DepalletApplication >> call_target_ids() >> エラー]: {e}")

    def call_AMR_return(self, line_frontage_id):
        try:
            logging.info("[DepalletApplication >> call_AMR_return() >> 成功]")
            self.depallet_service.call_AMR_return(line_frontage_id)
        except Exception as e:
            logging.error(f"[DepalletApplication >> call_AMR_return() >> エラー] : {e}")
            raise Exception(f"DepalletApplication >> call_AMR_return() >> エラー]: {e}")
        
    def call_AMR_flowrack_only(self, line_frontage_id):
        try:
            logging.info("[DepalletApplication >> call_AMR_flowrack_only() >> 成功]")
            self.depallet_service.call_AMR_flowrack_only(line_frontage_id)
        except Exception as e:
            logging.error(f"[DepalletApplication >> call_AMR_flowrack_only() >> エラー] : {e}")
            raise Exception(f"DepalletApplication >> call_AMR_flowrack_only() >> エラー]: {e}")
        
    def insert_kanban_nuki(self):
        try:
            logging.info("[DepalletApplication >> insert_kanban_nuki() >> 成功]")
            self.depallet_service.insert_kanban_nuki()
        except Exception as e:
            logging.error(f"[DepalletApplication >> insert_kanban_nuki() >> エラー] : {e}")
            raise Exception(f"DepalletApplication >> insert_kanban_nuki() >> エラー]: {e}")

    def insert_kanban_sashi(self):
        try:
            logging.info("[DepalletApplication >> insert_kanban_sashi() >> 成功]")
            self.depallet_service.insert_kanban_sashi()
        except Exception as e:
            logging.error(f"[DepalletApplication >> insert_kanban_sashi() >> エラー] : {e}")
            raise Exception(f"DepalletApplication >> insert_kanban_sashi >> エラー]: {e}")
    
    def insert_kanban_yobi_dashi(self):
        try:
            logging.info("[DepalletApplication >> insert_kanban_yobi_dashi() >> 成功]")
            self.depallet_service.insert_kanban_yobi_dashi()
        except Exception as e:
            logging.error(f"[DepalletApplication >> insert_kanban_yobi_dashi() >> エラー] : {e}")
            raise Exception(f"DepalletApplication >> insert_kanban_yobi_dashi >> エラー]: {e}")

    # コタツに部品を戻す
    def return_part(self, frontage_id: int, part_id: int):
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
            # print(f"[return_part >> エラー] depalletizing] : {e}")
            raise Exception(f"Error depalletizing: {e}")

    def return_kotatsu(self, frontage_id: int):
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

    def get_product_infos_json(self): # TODO➞リン: changed to a_product_r, self.a_product_l, self.b_product_r, self.b_product_l
        return util.to_json(self.a_product_r), util.to_json(self.a_product_l), util.to_json(self.b_product_r), util.to_json(self.b_product_l) 

    def get_depallet_area_json(self):
        return util.to_json(self.depallet_area)

    def get_flow_rack_json(self):
        flow_rack_frontage = self.depallet_area.get_flow_rack_frontage()
        if flow_rack_frontage is None:
            return "{}"
        return util.to_json(flow_rack_frontage.shelf)

    # TODO➞リン: Added
    def get_depallet_area_by_plat_json(self):
        logging.info(f"[DepalletApplication >> get_depallet_area_by_plat_json >> self.new_depallet_area] : {self.new_depallet_area}")
        self.new_depallet_area = self.depallet_service.get_depallet_area_by_plat(self.PLAT_ID_LIST)  # TODO➞リン: added
        self.wcs_service.dispallet(self.new_depallet_area)
        logging.info(f"[app.py >> get_depallet_area_by_plat_json() >> Take Count saved to DB successfully]")
        return util.to_json(self.new_depallet_area)

if __name__ == "__main__":

    app = DepalletApplication()
    # app.start()
    app.new_start()
    try:
        while True:
            sleep(1)
            logging.info(f"[DepalletApplication >> get_lines_json()] : {app.get_lines_json()}")
            logging.info("----------------------")
            logging.info(f"[DepalletApplication >> get_depallet_area_json()] : {app.get_depallet_area_json()}")
            logging.info("----------------------")
            logging.info(f"[DepalletApplication >> get_depallet_area_by_plat_json()] : {app.get_depallet_area_by_plat_json()}")
            logging.info("----------------------")
            logging.info(f"[DepalletApplication >> get_product_infos_json()] : {app.get_product_infos_json()}")
    except KeyboardInterrupt:
        #  app.manager.stop_all()
        app.new_manager.stop_all()
        print("Stopped by user")

  


  