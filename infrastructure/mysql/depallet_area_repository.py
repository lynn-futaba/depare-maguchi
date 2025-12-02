from domain.models.shelf import Kotatsu ,Shelf, FlowRack
from domain.models.part import Inventory, Part ,KotatsuInventory

from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.line import LineFrontage

from domain.infrastructure.depallet_area_repository import IDepalletAreaRepository


import json
import os
import time

#mysql実装
class DepalletAreaRepository(IDepalletAreaRepository):

    def __init__(self,db):

        self.db = db
        
        # TODO : Load take_count config dynamically
        TAKE_COUNT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/take_count_config.json")
        with open(TAKE_COUNT_CONFIG_PATH, "r", encoding="utf-8") as f:
            self.take_count_map = json.load(f)

        # TODO : Load flowrack_no config dynamically
        FLOWRACK_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/flowrack_no_config.json")
        with open(FLOWRACK_CONFIG_PATH, "r", encoding="utf-8") as f:
            self.flowrack_no_map = json.load(f)

        # TODO : Load maguchi_no_map config dynamically
        MAGUCHI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/maguchi_no_config.json")
        with open(MAGUCHI_CONFIG_PATH, "r", encoding="utf-8") as f:
            self.maguchi_no_map = json.load(f)

        
        # TODO : Load shelf_code config
        SHELF_FLOWRACKS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/shelf_code_flowracks_config.json")
        with open(SHELF_FLOWRACKS_CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config_shelf_codes_flowracks = json.load(f).get("shelf_codes", [])


    # TODO: Get take_count
    def get_take_count(self, kanban_no: str) -> str:
            """Return take_count for given kanban_no from config."""
            return self.take_count_map.get(kanban_no, "-0")
    
    # TODO: Get flowrack_no
    def get_flowrack_no(self, kanban_no: str) -> str:
            """Return flowrack_no for given kanban_no from config."""
            return self.flowrack_no_map.get(kanban_no, "")
    
    # TODO: Get flowrack_no
    def get_maguchi_no(self, plat: int) -> int:
            """Return maguchi_no for given plat from config."""
            return self.maguchi_no_map.get(plat, "")

        
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
            print(f"[DepalletAreaRepository >> Error] : {e}")
                
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
    
    # TODO: 間口に搬送対象idを入力
    def insert_target_ids(self, line_frontage_id):
        conn = None
        cur = None
        try:
            print(f"[DepalletAreaRepository >> insert_target_ids] Starting flowrack update for line_frontage_id={line_frontage_id}")

            # Mapping for creates
            creates_map = {
                # Bライン, 間口 5,4,3,2,1
                1: [(107, 8404), (103, 8403), (105, 8402), (106, 8401), (18, 8400)],  # R1 => button_id 1
                2: [(102, 8404), (108, 8403), (101, 8402), (104, 8401), (21, 8400)],  # R2 => button_id 2
                3: [(23, 8404), (100, 8403), (301, 8402)],                            # R3 => button_id 3
                4: [(26, 8504), (206, 8503), (205, 8502), (203, 8501), (208, 8500)],  # L1 => button_id 4
                5: [(29, 8504), (204, 8503), (201, 8502), (207, 8501), (202, 8500)],  # L2 => button_id 5
                6: [(300, 8502), (200, 8501), (31, 8500)],                            # L3 => button_id 6
                # Aライン, 間口 5,4,3,2,1
                7: [(107, 8404), (103, 8403), (105, 8402), (106, 8401), (2, 8400)],  # R1 => button_id 7
                8: [(102, 8404), (108, 8403), (101, 8402), (104, 8401), (5, 8400)],  # R2 => button_id 8
                9: [(7, 8404), (100, 8403), (301, 8402)],                            # R3 => button_id 9
                10: [(10, 8504), (206, 8503), (205, 8502), (203, 8501), (208, 8500)],  # L1 => button_id 10
                11: [(13, 8504), (204, 8503), (201, 8502), (207, 8501), (202, 8500)],  # L2 => button_id 11
                12: [(300, 8502), (200, 8501), (15, 8500)],                            # L3 => button_id 12
            }

            kanban_map = {1: 2001, 2: 2002, 3: 2003, 4: 2004, 5: 2005, 6: 2006, 7: 1001, 8: 1002, 9: 1003, 10: 1004, 11: 1005, 12: 1006} # Bライン (button_id 1～6 R1,R2,R3,L1,L2,L3), # Aライン (button_id 7～12 R1,R2,R3,L1,L2,L3)

            creates = creates_map.get(line_frontage_id)
            step_kanban_no = kanban_map.get(line_frontage_id)


            if not creates:
                print("No mappings found for given line_frontage_id.")
                return

            # Connect for flowrack update
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor(dictionary=True)

            
            # ✅ Fetch shelf status for specific shelf_codes
            # shelf_codes = ('K30143', 'K30148', 'K30149', 'K30150')
            shelf_codes =  self.config_shelf_codes_flowracks
            print(f"[DepalletAreaRepository >> self.config_shelf_codes_flowracks] {shelf_codes}.")
            sql = f"""
                SELECT shelf_code, kotatsu_status, update_datetime, step_kanban_no
                FROM `futaba-chiryu-3building`.t_shelf_status
                WHERE shelf_code IN ({','.join(['%s'] * len(shelf_codes))})
            """
            cur.execute(sql, shelf_codes)
            result = cur.fetchall()

            # Filter EMPTY rows and sort by earliest update_datetime
            empty_rows = [row for row in result if row["kotatsu_status"] == "EMPTY"]
            empty_rows.sort(key=lambda r: r["update_datetime"])

            print(f"[DepalletAreaRepository >> insert_target_ids] Found {len(empty_rows)} EMPTY shelves.")

            if not empty_rows:
                print("[DepalletAreaRepository >> insert_target_ids] No EMPTY shelves found for given shelf_codes.")
                conn.rollback()
                return

            # ✅ Update t_shelf_status with new step_kanban_no for the first EMPTY shelf
            update_sql = """
                UPDATE `futaba-chiryu-3building`.t_shelf_status
                SET step_kanban_no = %s
                WHERE shelf_code = %s
            """
            cur.execute(update_sql, (step_kanban_no, empty_rows[0]["shelf_code"]))
            print(f"[DepalletAreaRepository >> insert_target_ids] Updated t_shelf_status: shelf_code={empty_rows[0]['shelf_code']} -> step_kanban_no={step_kanban_no}")

            # ✅ Update signals once
            cur.executemany(
                "UPDATE `eip_signal`.word_input SET value = %s WHERE signal_id = %s",
                creates
            )
            conn.commit()
            print(f"[DepalletAreaRepository >> insert_target_ids] Signal updates completed for line_frontage_id={line_frontage_id}")


        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"[DepalletAreaRepository >> insert_target_ids] Error: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # TODO: 間口に搬送対象を呼び出す
    def call_target_ids(self, line_frontage_id):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if line_frontage_id in (1, 7): # ( Bライン=> R1 button_id 1, Aライン=> R1 button_id 7)
                signal_ids = (8061, 8046, 8031, 8016, 8000) # ( Bライン/ Aライン, R1 => 5,4,3,2,1)

            elif line_frontage_id in (2, 8): # ( Bライン=> R2 button_id 2, Aライン=> R2 button_id 8)
                signal_ids = (8061, 8046, 8032, 8016, 8000) # ( Bライン/ Aライン, R2 => 5,4,3,2,1)

            elif line_frontage_id in (3, 9): # ( Bライン=> R3 button_id 3, Aライン=> R3 button_id 9)
                signal_ids = (8060, 8046, 8032) # ( Bライン/ Aライン, R3 => 5,4,3)

            elif line_frontage_id in (4, 10): # ( Bライン=> L1 button_id 4, Aライン=> L1 button_id 10)
                signal_ids = (8260, 8246, 8231, 8216, 8201) # ( Bライン/ Aライン, L1 => 5,4,3,2,1)

            elif line_frontage_id in (5, 11): # ( Bライン=> L2 button_id 5, Aライン=> L2 button_id 11)
                signal_ids = (8260, 8246, 8231, 8216, 8201) # ( Bライン/ Aライン, L2 => 5,4,3,2,1)

            elif line_frontage_id in (6, 12): # ( Bライン=> L3 button_id 6, Aライン=> L3 button_id 12)
                signal_ids = (8231, 8216, 8200) # ( Bライン/ Aライン, L3 => 5,4,3)

            else:
                raise ValueError(f"Invalid line_frontage_id: {line_frontage_id}")

            placeholders = ','.join(['%s'] * len(signal_ids))
            sql = f"UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id IN ({placeholders})"
            cur.execute(sql, signal_ids)

            print(f"[DepalletAreaRepository >> call_target_ids >> Updated IDs]: {signal_ids}")

            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"[DepalletAreaRepository >> call_target_ids] Error: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    
    # TODO: call AMR return
    def call_AMR_return(self, line_frontage_id):
        # Mapping for signal IDs
        signal_map = {
            "hashiru_ichi": {  # 呼び出し信号をリセット
                # Bライン, 間口 5,4,3,2,1
                1: (8061, 8046, 8031, 8016, 8000), # R1 => button_id 1
                2: (8061, 8046, 8032, 8016, 8000), # R2 => button_id 2
                3: (8060, 8046, 8032),             # R3 => button_id 3
                4: (8260, 8246, 8231, 8216, 8201), # L1 => button_id 4
                5: (8260, 8246, 8231, 8216, 8201), # L2 => button_id 5
                6: (8231, 8216, 8200),             # L3 => button_id 6
                # Aライン, 間口 5,4,3,2,1
                7: (8061, 8046, 8031, 8016, 8000), # R1 => button_id 7
                8: (8061, 8046, 8032, 8016, 8000), # R2 => button_id 8
                9: (8060, 8046, 8032),             # R3 => button_id 9
                10: (8260, 8246, 8231, 8216, 8201),# L1 => button_id 10
                11: (8260, 8246, 8231, 8216, 8201),# L2 => button_id 11
                12: (8231, 8216, 8200),            # L3 => button_id 12
            },
            "hashiru_ni": {  # 搬送指示 間口からストアに搬送
                # Bライン, 間口 5,4,3,2,1
                1: (8062, 8047, 8032, 8017, 8002), # R1 => button_id 1
                2: (8062, 8047, 8032, 8017, 8002), # R2 => button_id 2
                3: (8062, 8047, 8032),             # R3 => button_id 3
                4: (8262, 8247, 8232, 8217, 8202), # L1 => button_id 4
                5: (8262, 8247, 8232, 8217, 8202), # L2 => button_id 5
                6: (8232, 8217, 8202),             # L3 => button_id 6
                # Aライン, 間口 5,4,3,2,1
                7: (8062, 8047, 8032, 8017, 8002), # R1 => button_id 7
                8: (8062, 8047, 8032, 8017, 8002), # R2 => button_id 8
                9: (8062, 8047, 8032),             # R3 => button_id 9
                10: (8262, 8247, 8232, 8217, 8202),# L1 => button_id 10
                11: (8262, 8247, 8232, 8217, 8202),# L2 => button_id 11
                12: (8232, 8217, 8202),            # L3 => button_id 12
            },
            "kaeru_ichi": {  # 搬送対象idをリセット
                # Bライン, 間口 5,4,3,2,1
                1: (8404, 8403, 8402, 8401, 8400), # R1 => button_id 1
                2: (8404, 8403, 8402, 8401, 8400), # R2 => button_id 2
                3: (8404, 8403, 8402),             # R3 => button_id 3
                4: (8504, 8503, 8502, 8501, 8500), # L1 => button_id 4
                5: (8504, 8503, 8502, 8501, 8500), # L2 => button_id 5
                6: (8502, 8501, 8500),             # L3 => button_id 6
                # Aライン, 間口 5,4,3,2,1
                7: (8404, 8403, 8402, 8401, 8400), # R1 => button_id 7
                8: (8404, 8403, 8402, 8401, 8400), # R2 => button_id 8
                9: (8404, 8403, 8402),             # R3 => button_id 9
                10: (8504, 8503, 8502, 8501, 8500),# L1 => button_id 10
                11: (8504, 8503, 8502, 8501, 8500),# L2 => button_id 11
                12: (8502, 8501, 8500),            # L3 => button_id 12
            },
            # "kaeru_ni": {  # 搬送指示リセット
            #     # Bライン, 間口 5,4,3,2,1
            #     1: (8062, 8047, 8032, 8017, 8002), # R1 => button_id 1
            #     2: (8062, 8047, 8032, 8017, 8002), # R2 => button_id 2
            #     3: (8062, 8047, 8032),             # R3 => button_id 3
            #     4: (8262, 8247, 8232, 8217, 8202), # L1 => button_id 4
            #     5: (8262, 8247, 8232, 8217, 8202), # L2 => button_id 5
            #     6: (8232, 8217, 8202),             # L3 => button_id 6
            #     # Aライン, 間口 5,4,3,2,1
            #     7: (8062, 8047, 8032, 8017, 8002), # R1 => button_id 7
            #     8: (8062, 8047, 8032, 8017, 8002), # R2 => button_id 8
            #     9: (8062, 8047, 8032),             # R3 => button_id 9
            #     10: (8262, 8247, 8232, 8217, 8202),# L1 => button_id 10
            #     11: (8262, 8247, 8232, 8217, 8202),# L2 => button_id 11
            #     12: (8232, 8217, 8202),            # L3 => button_id 12
            # }
        }

        if line_frontage_id not in range(1, 13):
            raise ValueError(f"Invalid line_frontage_id: {line_frontage_id}")
       
        
        
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            # Collect IDs
            ids_step1 = signal_map.get("hashiru_ichi", {}).get(line_frontage_id, [])
            ids_step2 = signal_map.get("hashiru_ni", {}).get(line_frontage_id, [])
            ids_step3 = signal_map.get("kaeru_ichi", {}).get(line_frontage_id, [])

            all_ids = [*ids_step1, *ids_step2, *ids_step3]

            if not all_ids:
                print("⚠ No signal IDs found for update.")
                return

            # Build CASE dynamically
            conditions = []
            params = []
            if ids_step1:
                conditions.append(f"WHEN signal_id IN ({','.join(['%s']*len(ids_step1))}) THEN 0")
                params.extend(ids_step1)
            if ids_step3:
                conditions.append(f"WHEN signal_id IN ({','.join(['%s']*len(ids_step3))}) THEN 0")
                params.extend(ids_step3)
            if ids_step2:
                conditions.append(f"WHEN signal_id IN ({','.join(['%s']*len(ids_step2))}) THEN 1")
                params.extend(ids_step2)

            placeholders_all = ','.join(['%s'] * len(all_ids))
            params.extend(all_ids)

            sql = f"""
            UPDATE eip_signal.word_input
            SET value = CASE {' '.join(conditions)} END
            WHERE signal_id IN ({placeholders_all})
            """

            # Execute combined update
            cur.execute(sql, params)
            print(f"✅ Combined update executed (rows changed: {cur.rowcount})")

            conn.commit()

            # Wait before checking Step 2
            time.sleep(10)

            # Check Step 2 signals
            if ids_step2:
                placeholders2 = ','.join(['%s'] * len(ids_step2))
                cur.execute(f"SELECT COUNT(*) FROM eip_signal.word_input WHERE signal_id IN ({placeholders2}) AND value = 1", ids_step2)
                count = cur.fetchone()[0]
                print(f"✅ Step 2 active signals: {count}")

                # Reset Step 2 to 0
                cur.execute(f"UPDATE eip_signal.word_input SET value = 0 WHERE signal_id IN ({placeholders2})", ids_step2)
                print("✅ Step 2 reset to 0")

                conn.commit()

            print(f"✅ Transaction committed for line_frontage_id={line_frontage_id}")



        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[DepalletAreaRepository >> call_AMR_return] ❌ Error: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    
    def get_depallet_area_by_plat(self, plat_id_list: list = None, button_id: int = 0):
        """
        Build update_frontages for plats 20–29 (or custom plat_id_list).
        Each plat key contains a list of shelf details.
        """
        conn = None
        cur = None
        
        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            # plat_id_list (20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
            # ✅ Apply button logic
            selected_ids = []
            if button_id in (1, 2, 3, 7, 8, 9):  # R1, R2, R3
                selected_ids = plat_id_list[:5]  # First half
            elif button_id in (4, 5, 6, 10, 11, 12):  # L1, L2, L3
                selected_ids = plat_id_list[5:]  # Second half

            # ✅ Merge and remove duplicates
            if selected_ids:
                plat_id_list = list(set(plat_id_list + selected_ids))

            if not plat_id_list:
                print("⚠ No plat IDs after button logic.")
                return {}  # Avoid duplicates

            # ✅ Prepare SQL placeholders
        
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
            rows = cur.fetchall()

            # ✅ Build response
            update_frontages = {}
            for row in rows:
                plat_value = row["plat"]
                if plat_value not in update_frontages:
                    update_frontages[plat_value] = []
                update_frontages[plat_value].append({
                    "step_kanban_no": row["step_kanban_no"],
                    "load_num": row["load_num"],
                    "shelf_code": row["shelf_code"],
                    "take_count": self.take_count_map.get(row["step_kanban_no"], "0"),
                    "flow_rack_no": self.flowrack_no_map.get(row["step_kanban_no"], "0"),
                    "maguchi_no": self.maguchi_no_map.get(row["plat"], "0")
                })

            return update_frontages

        except Exception as e:
            print(f"[DepalletAreaRepository >> Error] : {e}")
            return {}

        finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

    # TODO: かんばん抜きの発信を呼び出し
    def insert_kanban_nuki(self):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            # Step 1: Update value to 1
            sql_first = "UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = 9030"
            cur.execute(sql_first)
            print("[DepalletAreaRepository >> insert_kanban_nuki >> Updated signal_id: 9030 to 1]")

            # Step 2: Check using_flag
            sql_check = """
                SELECT s.using_flag
                FROM t_shelf_status s
                JOIN t_location_status l ON s.shelf_code = l.shelf_code
                WHERE l.cell_code = 30550017
            """
            cur.execute(sql_check)
            result = cur.fetchone()

            # Step 3: If using_flag = 0, update value back to 0
            if result and result[0] == 0:
                sql_update = "UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = 9030"
                cur.execute(sql_update)
                print("[DepalletAreaRepository >> insert_kanban_nuki >> Updated signal_id: 9030 to 0]")

                conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"[DepalletAreaRepository >> insert_kanban_nuki Error]: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # TODO: かんばん差しの発信を呼び出し
    def insert_kanban_sashi(self):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            # Step 1: Update value to 1
            sql_first = "UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = 9031"
            cur.execute(sql_first)
            print("[DepalletAreaRepository >> insert_kanban_nuki >> Updated signal_id: 9031 to 1]")

            # Step 2: Check using_flag
            sql_check = """
                SELECT s.using_flag
                FROM t_shelf_status s
                JOIN t_location_status l ON s.shelf_code = l.shelf_code
                WHERE l.cell_code = 30550017
            """
            cur.execute(sql_check)
            result = cur.fetchone()

            # Step 3: If using_flag = 0, update value back to 0
            if result and result[0] == 0:
                sql_update = "UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = 9031"
                cur.execute(sql_update)
                print("[DepalletAreaRepository >> insert_kanban_nuki >> Updated signal_id: 9031 to 0]")

                conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"[DepalletAreaRepository >> insert_kanban_sashi Error]: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


if __name__ == "__main__":
    from mysql_db import MysqlDb
    db = MysqlDb()
    repo = DepalletAreaRepository(db)
    area = repo.get_depallet_area((1,2,3,4)) # TODO: added 3,4
    new_area = repo.get_depallet_area_by_plat((20, 21, 22, 23, 24, 25, 26, 27, 28, 29)) # TODO: added
    # TODO: comment out
    # f = area.get_empty_frontage()
    # print(f.id)
    # for f in area.frontages.values():
    #    r = repo.get_flow_rack(f)
    #    print(r)
       # #print(f.signals)
       # TODO: comment open until last line
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
   

           

      

