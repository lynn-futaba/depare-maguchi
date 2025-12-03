from domain.models.line import LineFrontage
from domain.models.shelf import FlowRack, Kotatsu, Shelf
from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.part import Part
from domain.infrastructure.depallet_area_repository import IDepalletAreaRepository
from domain.infrastructure.wcs_controler import IWcsControler

class DepalletService:

    def __init__(self, depallet_area_repo:IDepalletAreaRepository, wcs:IWcsControler):

        self.depallet_area_repo = depallet_area_repo
        self.wcs = wcs

    def get_depallet_area(self, line_id_list:list)->DepalletArea:
        try:
            if not line_id_list:
                raise Exception("line_id_list is empty")
            area = self.depallet_area_repo.get_depallet_area(line_id_list)
            # print(f"[DepalletService >> get_depallet_area >> area Result] : {area}") # TODO: testing
            return area
        
        except Exception as e:
            raise Exception(f"Error loading depallet area: {e}")
    
    def is_frontage_ready(self, frontage:DepalletFrontage)->bool:    
        try:
            return self.depallet_area_repo.is_frontage_ready(frontage)
        except Exception as e:
            raise Exception(f"Error checking frontage readiness: {e}")
    
    # デパレタイズ（コタツ<->フローラック）
    def depalletizing(self, source:Shelf, dest:Shelf, target:Part):

        # 🎯 CRITICAL FIX: Check if the part object is None before using it.
        if target is None:
        # Raise an exception that clearly states the required object is missing.
            raise ValueError("Cannot depalletize: The 'target' part object passed to depalletizing service is None.")

        # print(f"[DepalletService >> depalletizing >> dest] : {dest.values()}")
        # print(f"[DepalletService >> depalletizing >> source] : {source.values()}")
        # print(f"[DepalletService >> depalletizing >> target] : {target.values()}")

        try:
            dest.add(target, 1)
            # print("[DepalletService >> depalletizing >> dest coming] :")
        except Exception as e:
            raise Exception(f"Error during depalletizing: {e}")

        try:    
            source.remove(target, 1)
            # print("[DepalletService >> depalletizing >> source coming] :")
        except Exception as e:
            dest.remove(target, 1)
            raise Exception(f"Error during depalletizing: {e}")

    #コタツ取得
    def set_kotatsu(self,frontage:DepalletFrontage):
        try:
            if frontage.shelf is not None:
                return  # すでにセットされている場合は何もしない
            kotastu = self.depallet_area_repo.get_kotatsu(frontage)
            if kotastu is None:
                return
            frontage.set_shelf(kotastu)
            for inventory in frontage.shelf.inventories:
                print(f"Kotatsu Inventory - Part ID: {inventory.part.id}, Case Quantity: {inventory.case_quantity}")
        except Exception as e:
            raise Exception(f"Error setting kotatsu: {e}")

     # コタツ保存
    def _save_kotatsu(self, shelf: Shelf):
        try:
            if shelf is None:
                raise Exception("Shelf is None")

            self.depallet_area_repo.save_kotatsu(shelf)
        except Exception as e:
            raise Exception(f"Error saving kotatsu: {e}")

    # 部品要求
    def request_parts(self, area:DepalletArea,frontage:LineFrontage):
        try:
            for inventory in frontage.inventories:
                part = inventory.part
                dest = area.get_empty_frontage()
                if dest is not None:
                    self.wcs.request_kotatsu(dest,part)
                    dest.status = 1
        except Exception as e:
            raise Exception(f"Error during request parts: {e}")

    # フローラック要求
    def request_flow_rack(self, area:DepalletArea,frontage: LineFrontage):
        try:
            dest = area.get_empty_frontage()
            if dest is not None:
                self.wcs.request_flow_rack(dest, frontage)
                flow_rack=self.depallet_area_repo.get_flow_rack(frontage)
                dest.set_shelf(flow_rack)  # フローラックを割り当てる
                dest.status = 2

        except Exception as e:
            raise Exception(f"Error during request flow rack: {e}")   

        #搬出
    def dispatch(self, source: DepalletFrontage):
        try:
            self.wcs.dispatch(source)
            if isinstance(source.shelf, Kotatsu):
                self._save_kotatsu(source.shelf)
            source.remove_shlef() 
            source.status = 0
        except Exception as e:
            raise Exception(f"Error during dispatch: {e}")

     #全搬出
    def dispatch_all(self, source: DepalletArea):
        try:
            for frontage in source.frontages.values():
                if frontage.shelf is not None:
                    self.wcs.dispatch(frontage)
        except Exception as e:
            raise Exception(f"Error during dispatch: {e}")
        
    
    # update maguchi signal 1
    def insert_target_ids(self, line_frontage_id):
        try:
            print("[DepalletService >> insert_target_ids >> line_frontage_id ]")
            self.depallet_area_repo.insert_target_ids(line_frontage_id)
        except Exception as e:
            print(f"DepalletService >> Error update maguchi by signal input: {e}")
            raise Exception(f"DepalletService >> Error update maguchi by signal input: {e}")
        
    # update maguchi signal 2
    def call_target_ids(self, line_frontage_id):
        try:
            print("[DepalletService >> call_target_ids >> line_frontage_id ]")
            self.depallet_area_repo.call_target_ids(line_frontage_id)
        except Exception as e:
            print(f"DepalletService >> Error set values to maguchi: {e}")
            raise Exception(f"DepalletService >> Error set values to maguchi: {e}")
        

    def call_AMR_return(self, line_frontage_id):
        try:
            print("[DepalletService >> call_AMR_return >> line_frontage_id ]")
            self.depallet_area_repo.call_AMR_return(line_frontage_id)
        except Exception as e:
            print(f"DepalletService >> Error set values to call_AMR_return: {e}")
            raise Exception(f"DepalletService >> Error set values to call_AMR_return: {e}")
                
    # update new depallet area
    def get_depallet_area_by_plat(self, plat_id_list: list, button_id: int):
        try:
            print(f"[DepalletService >> get_depallet_area_by_plat >> plat_id_list] : {plat_id_list}") 
            new_area = self.depallet_area_repo.get_depallet_area_by_plat(plat_id_list, button_id)
            print(f"[DepalletService >> get_depallet_area_by_plat >> new_area Result] : {new_area}") # TODO: testing
            return new_area
        except Exception as e:
            raise Exception(f"DepalletService >> Error loading depallet area: {e}")
        
    # insert kanban nuki
    def insert_kanban_nuki(self):
        try:
            print("[DepalletService >> insert_kanban_nuki >> ]")
            self.depallet_area_repo.insert_kanban_nuki()
        except Exception as e:
            print(f"DepalletService >> Error set values to insert_kanban_nuki: {e}")
            raise Exception(f"DepalletService >> Error set values to insert_kanban_nuki: {e}")
        
    # insert kanban sashi
    def insert_kanban_sashi(self):
        try:
            print("[DepalletService >> insert_kanban_sashi >> ]")
            self.depallet_area_repo.insert_kanban_sashi()
        except Exception as e:
            print(f"DepalletService >> Error set values to insert_kanban_sashi: {e}")
            raise Exception(f"DepalletService >> Error set values to insert_kanban_sashi: {e}")

if __name__ == "__main__":
  
    s = DepalletService()
