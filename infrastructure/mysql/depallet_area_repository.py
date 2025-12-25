from domain.models.shelf import Kotatsu, Shelf, FlowRack
from domain.models.part import Inventory, Part, KotatsuInventory

from domain.models.shelf import Kotatsu, Shelf, FlowRack
from domain.models.part import Inventory, Part, KotatsuInventory

from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.line import LineFrontage

from domain.infrastructure.depallet_area_repository import IDepalletAreaRepository
from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS, LOG_FOLDER, LOG_FILE  # ログ用


from typing import Optional
from config.config_loader import AppConfig

import json
import os
import time
import logging
import threading

# ログ出力開始
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

#mysql実装
class DepalletAreaRepository(IDepalletAreaRepository):

    def __init__(self, db, app_config: Optional[AppConfig] = None):

        self.db = db
        self._listener_thread = None
        self._listener_lock = threading.Lock()

        # Load app_config.json once (allow DI for tests)
        self.cfg = app_config or AppConfig()

    
    #--- Replaced functions using the unified loader
    def get_take_count(self, kanban_no: str) -> str:
        return self.cfg.get_take_count(kanban_no)

    def get_flowrack_no(self, kanban_no: str) -> str:
        return self.cfg.get_flowrack_no(kanban_no)

    def get_maguchi_no(self, plat: int) -> str:
        return self.cfg.get_maguchi_no(plat)

    # If you previously needed shelf_codes groups:
    def get_shelf_codes_L3_R3(self) -> list[str]:
        return self.cfg.get_shelf_codes_group("L3_R3")

    def get_shelf_codes_R1_R2_L1_L2(self) -> list[str]:
        return self.cfg.get_shelf_codes_group("R1_R2_L1_L2")

    # If you need flowrack_no -> shelf_code mapping:
    def get_shelf_code_by_flowrack_no(self, flowrack_no: str) -> str:
        return self.cfg.get_shelf_code_by_flowrack_no(flowrack_no)

    def get_depallet_area(self, line_id_list:list)->DepalletArea:
        area = DepalletArea("A")
        conn = None
        cur = None

        try:
            # Get DB connection
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            # 1. Fetch depallet_frontage
            sql =f"SELECT frontage_id, name, priority, cell_code FROM depal.depallet_frontage"\
                      +" join depal.line_depallet_frontage using (frontage_id)"\
                    + " where depal.line_depallet_frontage.line_id in " + str(tuple(line_id_list)) \
                     + " group by frontage_id, name, priority, cell_code"
            cur.execute(sql)
            result = cur.fetchall()
            # print(f"[DepalletFrontage >> Query Result] : {result}") 

            for row in result:
                frontege = DepalletFrontage(str(row["cell_code"]), row["frontage_id"], row["name"], row["priority"])     
                area.register_frontage(frontege)

            # 2. Fetch signal for each frontage
            for frontage in area.frontages.values():
                # print(f"[After Area Registration >> Frontage >> ID] : {frontage.id}")
                sql = f"SELECT * FROM depal.signal WHERE frontage_id={frontage.id};"
                cur.execute(sql)
                signal_result = cur.fetchall()
                # print(f"[Signal >> Query Result] : {signal_result}")

                signals = {}
                for row in signal_result:
                    signals[row["tag"]] = int(row["signal_id"])

                frontage.signals = signals
                # print(f"[Signal >> frontage.signals] : {frontage.signals}")
                shelf = self.get_shelf(frontage)
                if shelf is not None:
                    # print("[frontage.signals >> shelf is not None]")
                    frontage.set_shelf(shelf)
        except Exception as e:
            print(f"[DepalletAreaRepository >> get_depallet_area >> エラー] : {e}")
                
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        return area
    
    def is_frontage_ready(self, frontage:DepalletFrontage)->bool:
        value = None
        try:
            conn = self.db.eip_signal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            signal_id = frontage.signals["ready"]
            sql = f"SELECT * FROM `eip_signal`.word_output WHERE signal_id={signal_id};"
            cur.execute(sql)
            result = cur.fetchall()
            # print(f"[is_frontage_ready >> eip_signal >> Query Result] : {result}") #TODO: testing

            for row in result:
                if row["value"] == 1:
                   value = True
                else:
                   value = False
        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        return value

    def get_shelf(self, frontage: DepalletFrontage) -> Shelf:
        try:
            # print(f"[Get_shelf >> frontage] : {frontage}")

            if self.is_frontage_ready(frontage) == False:
                # print(f"[Get_shelf >> is_frontage_ready] : {self.is_frontage_ready(frontage)}")
                return None
            
            kotatsu = self.get_kotatsu(frontage)
            if kotatsu is not None:
                # print(f"[Get_shelf >> get_kotatsu] : {kotatsu is not None}")
                return kotatsu
            
            flow_rack = self.get_flow_rack(frontage)
            # print(f"[Get_shelf >> flow_rack] : {flow_rack}")
            if flow_rack is not None:
                return flow_rack
            
        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        return None
        
    def get_kotatsu(self, frontage: DepalletFrontage) -> Kotatsu:
        try:
            conn = self.db.eip_signal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            parts_tag_list = [ "part1_no", "part2_no", "part3_no", "part4_no", "part5_no", "part6_no", "part1_count", "part2_count",
                          "part3_count", "part4_count", "part5_count", "part6_count" ]

            parts_signals = [frontage.signals[k] for k in parts_tag_list if k in frontage.signals]
            parts_signals = tuple(parts_signals)

            # print(f"[Get_kotatsu >> parts_signals >> Result] : {parts_signals}")
      
            sql = f"SELECT * FROM `eip_signal`.word_output WHERE signal_id IN {parts_signals} ORDER BY signal_id;"
            cur.execute(sql)
            result = cur.fetchall()
            # print(f"[Get_kotatsu >> eip_signal >> Query Result] : {result}")

            inventory_list = []
            
            for i,(no, count) in enumerate(zip(result[::2], result[1::2]),start=1):
                if no["value"] == 0:
                    continue
                # とりあえず背番号のみの部品として扱う
                inventory = KotatsuInventory(0, Part(str(no["value"]),str(no["value"]),str(no["value"]),0), int(count["value"]), 
                                             frontage.signals[f"fetch{i}"],frontage.signals[f"fetch{i}_count"],frontage.signals[f"part{i}_no"],frontage.signals[f"part{i}_count"])
                inventory_list.append(inventory)
                # print(f"[Get_kotatsu >> Inventory_list >> Result] : {result}")
          
            if len(inventory_list) == 0:
                return None
            kotatsu = Kotatsu('kotatsu', inventory_list)
            return kotatsu
        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        

    def get_flow_rack(self, frontage:LineFrontage)->FlowRack:
        try:
          
            sql =f"SELECT * FROM depal.line_inventory "\
            + "INNER JOIN depal.rack_position as r USING(inventory_id) "\
            + "INNER JOIN depal.m_product USING(part_number) "\
            + f"RIGHT JOIN depal.position as p on r.rack_position_id = p.rack_position_id and frontage_id ={frontage.id} "\
            + "ORDER BY p.rack_position_id"

            conn =self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)
    
            cur.execute(sql)
            result= cur.fetchall()
            inventory_list = []
            
            for row in result:
                if row["part_number"] is None:
                    inventory = None
                else:
                    inventory = Inventory(row["inventory_id"], 
                                          Part(str(row["part_number"]),str(row["kanban_no"]),str(row["part_number"]),int(row["car_model_id"])), 
                                          0)
                inventory_list.append(inventory)
          
            cur.close()
            conn.close()

            flow_rack = FlowRack('flow_rack')
            flow_rack.set_inventories(inventory_list)
        except Exception as e:
           raise Exception(f"[DepalletAreaRepository] Error: {e}")
        return  flow_rack

    def save_kotatsu(self, shelf: Kotatsu):
      
        try:
            conn =self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if shelf is None:
                print("No shelf")
                return 
            if not isinstance(shelf, Kotatsu):
                print("Shelf is not Kotatsu")
                return

            for inventory in shelf.inventories:
                diff_count = inventory.initial_quantity - inventory.case_quantity
                
                if diff_count == 0:
                    continue

                cur.execute("UPDATE `eip_signal`.word_input SET value = %s WHERE signal_id = %s",(diff_count,inventory.fetch_count_signal_id))
                cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s",(inventory.fetch_signal_id,))
                
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        finally:
            cur.close()
            conn.close()
        return  
   
    # TODO➞リン: AMR発進
    def call_AMR_return(self, line_frontage_id):

        # --- MOCK MODE START ---
        # logging.info(f"MOCK: Received call for ID {line_frontage_id}")
        # time.sleep(3) # This makes the spinner spin for 3 seconds
        # return {"status": "success", "message": "Mock response"}
        # --- MOCK MODE END ---

        # Mapping for signal IDs
        signal_map = {
            "hashiru_ichi": { # ①一a # 呼び出し信号をリセット / デパレ間口()実TP の 呼出
                # Bライン
                1: (8061, 8046, 8031, 8016, 8000), # R1 間口 5,4,3,2,1 => button_id 1
                2: (8061, 8046, 8031, 8016, 8000), # R2 間口 5,4,3,2,1 => button_id 2
                3: (8060, 8046, 8031),             # R3 間口 5,4,3 => button_id 3
                4: (8260, 8246, 8231, 8216, 8201), # L1 間口 5,4,3,2,1 => button_id 4
                5: (8260, 8246, 8231, 8216, 8201), # L2 間口 5,4,3,2,1 => button_id 5
                6: (8231, 8216, 8200),             # L3 間口 3,2,1 => button_id 6
                # Aライン
                7: (8061, 8046, 8031, 8016, 8000), # R1 間口 5,4,3,2,1 => button_id 7
                8: (8061, 8046, 8031, 8016, 8000), # R2 間口 5,4,3,2,1 => button_id 8
                9: (8060, 8046, 8031),             # R3 間口 5,4,3 => button_id 9
                10:(8260, 8246, 8231, 8216, 8201), # L1 間口 5,4,3,2,1 => button_id 10
                11:(8260, 8246, 8231, 8216, 8201), # L2 間口 5,4,3,2,1 => button_id 11
                12:(8231, 8216, 8200),             # L3 間口 3,2,1 => button_id 12
            },
            "ni_herasu": {  # ②ニ: 搬送対象の取出し信号 / 間口()部品1取出し数量
                # Bライン
                1: (8063, 8048, 8033, 8018, 8003), # R1 間口 5,4,3,2 => button_id 1
                2: (8063, 8048, 8033, 8018, 8003), # R2 間口 5,4,3,2 => button_id 2
                3: (8048, 8033, 8018),             # R3 間口 5,4,3 => button_id 3
                4: (8263, 8248, 8233, 8218, 8203), # L1 間口 5,4,3,2,1 => button_id 4
                5: (8263, 8248, 8233, 8218, 8203), # L2 間口 5,4,3,2,1 => button_id 5
                6: (8233, 8218, 8203),             # L3 間口 3,2,1 => button_id 6
                # Aライン
                7: (8063, 8048, 8033, 8018, 8003), # R1 間口 5,4,3,2 => button_id 7
                8: (8063, 8048, 8033, 8018, 8003), # R2 間口 5,4,3,2 => button_id 8
                9: (8048, 8033, 8018),             # R3 間口 5,4,3 => button_id 9
                10:(8263, 8248, 8233, 8218, 8203), # L1 間口 5,4,3,2,1 => button_id 10
                11:(8263, 8248, 8233, 8218, 8203), # L2 間口 5,4,3,2,1 => button_id 11
                12:(8233, 8218, 8203),             # L3 間口 3,2,1 => button_id 12
            },
            "kaeru_ichi": { # ①一b # 搬送対象idをリセット / デパレ間口()実TP の 呼出
                # Bライン
                1: (8404, 8403, 8402, 8401, 8400), # R1 間口 5,4,3,2 => button_id 1
                2: (8404, 8403, 8402, 8401, 8400), # R2 間口 5,4,3,2 => button_id 2
                3: (8404, 8403, 8402),             # R3 間口 5,4,3 => button_id 3
                4: (8504, 8503, 8502, 8501, 8500), # L1 間口 4,3,2,1 => button_id 4
                5: (8504, 8503, 8502, 8501, 8500), # L2 間口 4,3,2,1 => button_id 5
                6: (8502, 8501, 8500),             # L3 間口 3,2,1 => button_id 6
                # Aライン
                7: (8404, 8403, 8402, 8401, 8400), # R1 間口 5,4,3,2,1 => button_id 7
                8: (8404, 8403, 8402, 8401, 8400), # R2 間口 5,4,3,2,1 => button_id 8 
                9: (8404, 8403, 8402),             # R3 間口 5,4,3 => button_id 9
                10:(8504, 8503, 8502, 8501, 8500), # L1 間口 5,4,3,2,1 => button_id 10 
                11:(8504, 8503, 8502, 8501, 8500), # L2 間口 5,4,3,2,1 => button_id 11 
                12:(8502, 8501, 8500),             # L3 間口 3,2,1 => button_id 12
            },
            "hashiru_ni": { # ③三 # 搬送指示 間口からストアに搬送 / デパレ間口()発進
                # Bライン
                1: (8062, 8047, 8032, 8017, 8002), # R1 間口 5,4,3,2,1 => button_id 1
                2: (8062, 8047, 8032, 8017, 8002), # R2 間口 5,4,3,2,1 => button_id 2
                3: (8062, 8047, 8032),             # R3 間口 5,4,3 => button_id 3
                4: (8262, 8247, 8232, 8217, 8202), # L1 間口 5,4,3,2,1 => button_id 4
                5: (8262, 8247, 8232, 8217, 8202), # L2 間口 5,4,3,2,1 => button_id 5
                6: (8232, 8217, 8202),             # L3 間口 3,2,1 => button_id 6
                # Aライン
                7: (8062, 8047, 8032, 8017, 8002), # R1 間口 5,4,3,2,1 => button_id 7
                8: (8062, 8047, 8032, 8017, 8002), # R2 間口 5,4,3,2,1 => button_id 8
                9: (8062, 8047, 8032),             # R3 間口 5,4,3 => button_id 9
                10:(8262, 8247, 8232, 8217, 8202), # L1 間口 4,3,2,1 => button_id 10
                11:(8262, 8247, 8232, 8217, 8202), # L2 間口 4,3,2,1 => button_id 11
                12:(8232, 8217, 8202),             # L3 間口 3,2,1 => button_id 12
            },
        }

        if line_frontage_id not in range(1, 13):
            raise ValueError(f"Invalid 供給間口ID: {line_frontage_id}")
       
        try:
            conn = self.db.wcs_pool.get_connection()
            cur = conn.cursor()

            # Pre-fetch IDs
            ids_1a = signal_map["hashiru_ichi"].get(line_frontage_id, [])
            ids_2 = signal_map["ni_herasu"].get(line_frontage_id, [])
            ids_1b = signal_map["kaeru_ichi"].get(line_frontage_id, [])
            ids_3 = signal_map["hashiru_ni"].get(line_frontage_id, [])

            # --- EXECUTION SEQUENCE START ---

            # STEP 1: SET ①一a to OFF (value 0)
            if ids_1a:
                placeholders1 = ','.join(['%s'] * len(ids_1a))
                cur.execute(f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id IN ({placeholders1})", ids_1a)
                conn.commit() # Ensure PLC sees Step 1a reset before next step
                logging.info(f"SET ①一a to OFF for 供給間口ID: {line_frontage_id}")

            # STEP 2: SET ②ニ to ON (value 1)
            if ids_2:
                placeholders4 = ','.join(['%s'] * len(ids_2))
                cur.execute(f"UPDATE eip_signal.word_input SET value = 1 WHERE signal_id IN ({placeholders4})", ids_2)
                conn.commit() 
                logging.info(f"SET ②ニ to ON for 供給間口ID: {line_frontage_id}")
                time.sleep(1) # Handshake delay

            # STEP 3: SET ①一b to OFF (value 0)
            if ids_1b:
                placeholders1b = ','.join(['%s'] * len(ids_1b))
                cur.execute(f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id IN ({placeholders1b})", ids_1b)
                conn.commit()
                logging.info(f"SET ①一b to OFF for 供給間口ID: {line_frontage_id}")
                time.sleep(1)

            # STEP 4: SET ③三 to ON (value 1)
            if ids_3:
                placeholders3 = ','.join(['%s'] * len(ids_3))
                cur.execute(f"UPDATE eip_signal.word_input SET value = 1 WHERE signal_id IN ({placeholders3})", ids_3)
                conn.commit()
                logging.info(f"SET ③三 to ON for 供給間口ID: {line_frontage_id}")
                time.sleep(1)

            # STEP 5: FINAL RESET - Set ②ニ and ③三 to OFF (value 0)
            # Resetting these ensures the system is ready for the next call.
            if ids_2 and ids_3:
                # Reset ②ニ
                cur.execute(f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id IN ({','.join(['%s']*len(ids_2))})", ids_2)
                # Reset ③三
                cur.execute(f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id IN ({','.join(['%s']*len(ids_3))})", ids_3)
                conn.commit()
                logging.info(f"SET ②ニ and ③三 to OFF for 供給間口ID: {line_frontage_id}")
                
            logging.info(f"All steps completed successfully for ID: {line_frontage_id}")

        except Exception as e:
            if conn: conn.rollback()
            logging.error(f"Error in call_AMR_return: {e}")
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()

    # TODO➞リン: AMRフローラック発進
    def call_AMR_flowrack_only(self, line_frontage_id):

        # --- MOCK MODE START ---
        # logging.info(f"MOCK: Received call for ID {line_frontage_id}")
        # time.sleep(3) # This makes the spinner spin for 3 seconds
        # return {"status": "success", "message": "Flowrack Mock response"}
        # --- MOCK MODE END ---

        signal_map = {
            "hashiru_ni": {
                1: 8002, # R1 間口 1 => button_id 1
                2: 8002, # R2 間口 1 => button_id 2
                3: 8062, # R3 間口 5 => button_id 3
                4: 8262, # L1 間口 5=> button_id 4
                5: 8262, # L2 間口 5=> button_id 5
                6: 8202, # L3 間口 1 => button_id 6
                # Aライン
                7: 8002, # R1 間口 5=> button_id 7
                8: 8002, # R2 間口 5=> button_id 8
                9: 8062, # R3 間口 5=> button_id 9
                10:8262, # L1 間口 4,3,2,1 => button_id 10
                11:8262, # L2 間口 4,3,2,1 => button_id 11
                12:8202, # L3 間口 1 => button_id 12
            },
        }

        if line_frontage_id not in range(1, 13):
            raise ValueError(f"Invalid 供給間口ID: {line_frontage_id}")
        
        conn = None
        cur = None
        try:
            conn = self.db.wcs_pool.get_connection()
            cur = conn.cursor()

            # Ensure ids_3 is a list
            raw_val = signal_map["hashiru_ni"].get(line_frontage_id)
            ids_3 = [raw_val] if raw_val is not None else []

            if ids_3:
                placeholders = ','.join(['%s'] * len(ids_3))
                
                # Pulse ON
                sql_on = f"UPDATE eip_signal.word_input SET value = 1 WHERE signal_id IN ({placeholders})"
                cur.execute(sql_on, ids_3)
                conn.commit()
                logging.info(f"[DepalletAreaRepository >> call_AMR_flowrack_only()] SET ON for ID: {line_frontage_id}")

                time.sleep(5)

                # Pulse OFF
                sql_off = f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id IN ({placeholders})"
                cur.execute(sql_off, ids_3)
                conn.commit()
                logging.info(f"[DepalletAreaRepository >> call_AMR_flowrack_only()] SET OFF for ID: {line_frontage_id}")
                
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"[DepalletAreaRepository >> call_AMR_flowrack_only() >> エラー]: {e}")
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()


    def get_depallet_area_by_plat(self, plat_id_list: list):
        """
        Build update_frontages for plats 29-20 (or custom plat_id_list).
        Each plat key contains a list of shelf details.
        """
        conn = None
        cur = None
        
        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            placeholders = ','.join(['%s'] * len(plat_id_list))

            sql = f"""
            SELECT 
                mb.plat,
                ts.step_kanban_no,
                ts.load_num,
                ts.shelf_code
            FROM `futaba-chiryu-3building`.t_shelf_status AS ts
            INNER JOIN `futaba-chiryu-3building`.t_location_status AS tl
                ON ts.shelf_code = tl.shelf_code
            INNER JOIN `futaba-chiryu-3building`.m_basis_location AS mb
                ON tl.cell_code = mb.cell_code
            WHERE mb.plat IN ({placeholders});
            """

            cur.execute(sql, plat_id_list)
            result = cur.fetchall()


            # ✅ Build response
            update_frontages = {}
            for row in result:
                plat_value = row["plat"]
                if plat_value not in update_frontages:
                    update_frontages[plat_value] = []

                    # # These getters now automatically fetch fresh data if the JSON file was changed
                    update_frontages[plat_value].append({
                    "step_kanban_no": row["step_kanban_no"],
                    "load_num": row["load_num"],
                    "shelf_code": row["shelf_code"],
                    "take_count": self.cfg.get_take_count(row["step_kanban_no"]),
                    "flow_rack_no": self.cfg.get_flowrack_no(row["step_kanban_no"]),
                    "maguchi_no": self.cfg.get_maguchi_no(plat_value) 
                })
                    
            logging.info(f"[DepalletAreaRepository >> get_depallet_area_by_plat() >> update_frontages] : {update_frontages}")
            return update_frontages

        except Exception as e:
            logging.error(f"[DepalletAreaRepository >> get_depallet_area_by_plat() >> エラー ] : {e}")
            return {}

        finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

    # TODO➞リン: かんばん抜きの発進を呼び出し
    def insert_kanban_nuki(self):
        # Starts signal 9030 (start) and monitors to reset 9030 (reset)
        self._start_signal_and_listener(
            start_signal_id=9030,
            reset_signal_id=9030,
            log_prefix="Kanban Nuki (Signal 9030)"
        )

    # TODO➞リン: かんばん差しの発進を呼び出し
    def insert_kanban_sashi(self):
        # Starts signal 9031 (start) and monitors to reset 9031 (reset)
        self._start_signal_and_listener(
            start_signal_id=9031,
            reset_signal_id=9031,
            log_prefix="Kanban Sashi (Signal 9031)"
        )

    def _start_signal_and_listener(self, start_signal_id: int, reset_signal_id: int, log_prefix: str):
        """
        Unified function to set the starting signal and begin the listener thread.
        """
        conn = None
        cur = None
        try:
            conn = self.db.wcs_pool.get_connection()
            cur = conn.cursor()
            logging.info(f"{log_prefix}: Setting signal_id {start_signal_id} value to 1...")
            cur.execute(f"UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = {start_signal_id}")
            conn.commit()
        except Exception as e:
            logging.error(f"Error in {log_prefix} initial setup: {e}")
        finally:
            if cur: cur.close()
            if conn: conn.close()
            
        # Start the listener thread to monitor for the reset condition
        # Note: We must pass the necessary parameters to the thread target function
        with self._listener_lock:
            if self._listener_thread is None or not self._listener_thread.is_alive():
                logging.info(f"{log_prefix}: Starting background listener for signal reset condition...")
                print(f"{log_prefix}: Starting background listener for signal reset condition...")
                self._listener_thread = threading.Thread(
                    target=self._wait_and_reset_signal,
                    args=(reset_signal_id, log_prefix), # Pass parameters to the target function
                    daemon=True
                )
                self._listener_thread.start()
            else:
                logging.info(f"{log_prefix}: Background listener already running. Not starting another.")
                print(f"{log_prefix}: Starting background listener for signal reset condition...")

    def _wait_and_reset_signal(self, reset_signal_id: int, log_prefix: str, check_interval_sec=1.0): 
        """
        Unified polling function. Polls the database condition every second 
        and resets the specified signal_id to 0 when met.
        """
        
        # Using logging instead of print for thread safety and better handling
        logging.info(f"Background listener started for {log_prefix}. Polling Interval: {check_interval_sec} seconds.")
        print(f"Background listener started for {log_prefix}. Polling Interval: {check_interval_sec} seconds.")
        
        sql_check = """
            SELECT 1
            FROM `futaba-chiryu-3building`.t_location_status AS t1
            WHERE 
                t1.cell_code = 30550017 AND 
                t1.using_flag = 0 AND 
                (t1.shelf_code IS NULL OR t1.shelf_code = '')
        """
        
        while True:
            conn = None
            cur = None
            try:
                # 1. Acquire connection for THIS check
                conn = self.db.wcs_pool.get_connection()
                cur = conn.cursor()

                # 2. Execute the check query
                cur.execute(sql_check)
                rows = cur.fetchall()
                
                # 3. If condition met (using_flag is 0), update the signal and exit
                if rows:
                    logging.info(f"{log_prefix}: Query matched rows (using_flag = 0) -> resetting signal_id {reset_signal_id} to 0.")
                    print(f"{log_prefix}: Query matched rows (using_flag = 0) -> resetting signal_id {reset_signal_id} to 0.")
                    cur.execute(f"UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = {reset_signal_id}")
                    conn.commit()
                    logging.info(f"{log_prefix}: Reset signal_id {reset_signal_id} completed. Exiting listener.")
                    print(f"{log_prefix}: Reset signal_id {reset_signal_id} completed. Exiting listener.")
                    break # <-- Exit the loop
                    
            except Exception as e:
                # Handle connection or execution errors, log, and continue the loop
                logging.error(f"{log_prefix} Database Error: {e}. Retrying soon.")
                print(f"{log_prefix} Database Error: {e}. Retrying soon.")
                try:
                    if conn:
                        conn.rollback()
                except Exception:
                    pass
                    
            finally:
                # 4. Close resources
                if cur: cur.close()
                if conn: conn.close()
                
            # 5. Wait for the next check
            time.sleep(check_interval_sec)
            
        logging.info(f"Background listener thread finished for {log_prefix}.")

    # TODO➞リン: かんばん呼び出しの発進を呼び出し
    def insert_kanban_yobi_dashi(self):
        conn = None
        cur = None
        try:
            conn = self.db.wcs_pool.get_connection()
            cur = conn.cursor()

            # Pulse ON
            sql_on = f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id = 4501"
            cur.execute(sql_on)
            conn.commit()
            logging.info(f"[DepalletAreaRepository >> insert_kanban_yobi_dashi()] SET ON (value 1) for ID")

            time.sleep(5)

            # Pulse OFF
            sql_off = f"UPDATE eip_signal.word_input SET value = 1 WHERE signal_id = 4501"
            cur.execute(sql_off)
            conn.commit()
            logging.info(f"[DepalletAreaRepository >> insert_kanban_yobi_dashi()] SET OFF (value 0) for ID")

        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"[DepalletAreaRepository >> insert_kanban_yobi_dashi() >> エラー]: {e}")
            raise e
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

if __name__ == "__main__":
    from mysql_db import MysqlDb
    db = MysqlDb()
    repo = DepalletAreaRepository(db)
    area = repo.get_depallet_area((1,2,3,4)) # TODO➞リン: added 3,4
    new_area = repo.get_depallet_area_by_plat((20, 21, 22, 23, 24, 25, 26, 27, 28, 29)) # TODO➞リン: added
    # TODO➞リン: comment out
    # f = area.get_empty_frontage()
    # print(f.id)
    # for f in area.frontages.values():
    #    r = repo.get_flow_rack(f)
    #    print(r)
       # #print(f.signals)
       # TODO➞リン: comment open until last line
        #    status = repo.is_frontage_ready(f)
        #    print(f"[ DepalletAreaRepository >> __main__ >> status ]: {status}")
        #    k = repo.get_kotatsu(f)
        #    if k is None:
        #        continue
        #    f.set_shelf(k)
        #    for inv in f.shelf.inventories:
        #        print(f"Part No: {inv.part.kanban_id}, Count: {inv.case_quantity}")
        #        inv.remove(2)

        #    repo.save_kotatsu(f)

   

           

      

