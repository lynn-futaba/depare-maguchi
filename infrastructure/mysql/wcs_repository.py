import time
import logging

from typing import Optional

from domain.models.part import Part
from domain.models.line import LineFrontage
from domain.models.depallet import DepalletFrontage
from domain.infrastructure.wcs_repository import IWCSRepository

from common.setup_logger import setup_log  # ログ用
from config.config_loader import AppConfig
from config.config import BACKUP_DAYS, LOG_FOLDER, LOG_FILE   # ログ用


# ログ出力開始
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

class WCSRepository(IWCSRepository):

    def __init__(self, db, app_config: Optional[AppConfig] = None):
        self.db = db

        # Load app_config.json once (allow DI for tests)
        self.cfg = app_config or AppConfig()


    # 部品要求
    def request_kotatsu(self, frontage: DepalletFrontage, part: Part):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if frontage.shelf is not None:
                raise Exception("[WCSRepository] Shelf already exists")
            signal_id = frontage.signals["model_id"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = %s WHERE signal_id = %s", (part.car_model_id, signal_id))
            signal_id = frontage.signals["kotatsu_request"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s", (signal_id,))  
            conn.commit()

            # 一秒後に再度リクエスト信号を0に戻す
            time.sleep(1)
            conn.start_transaction()
            cur.execute("UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = %s", ( signal_id,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"[WCSRepository] Error: {e}")
        finally:
            cur.close()
            conn.close()
        return

    # フローラック要求
    def request_flow_rack(self, frontage: DepalletFrontage, line_frontage: LineFrontage):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if frontage.shelf is not None:
                raise Exception("[WCSRepository] Shelf already exists")

            signal_id = frontage.signals["model_id"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = %s WHERE signal_id = %s", (line_frontage.car_model_id, signal_id))
            signal_id = frontage.signals["flow_rack_request"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s", (signal_id,))  
            conn.commit()

            # 一秒後に再度リクエスト信号を0に戻す
            time.sleep(1)
            conn.start_transaction()
            cur.execute("UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = %s", (signal_id,))  
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"[WCSRepository] Error: {e}")
        finally:
            cur.close()
            conn.close()
        return

    # 搬出
    def dispatch(self, frontage: DepalletFrontage):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if frontage.shelf is None:
                raise Exception("[WCSRepository] No shelf in frontage")

            # add sugiura ###################################################
            signal_fetch1 = frontage.signals["fetch1"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s", (signal_fetch1,))
            conn.commit()

            time.sleep(1)
            signal_id = frontage.signals["dispatch"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s", (signal_id,))
            conn.commit()

            # 一秒後に再度リクエスト信号を0に戻す
            time.sleep(1)
            conn.start_transaction()
            cur.execute("UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = %s", (signal_id,))
            cur.execute("UPDATE `eip_signal`.word_input SET value = 0 WHERE signal_id = %s", (signal_fetch1,))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"[WCSRepository] Error: {e}")

        finally:
            cur.close()
            conn.close()
        return
    
    # TODO➞リン: 間口に搬送対象idを入力、部品を呼ぶためAMR信号にIDsをまずは入力します。
    def insert_target_ids(self, button_id):
        # --- MOCK MODE START ---
        # logging.info(f"MOCK: Insert target IDS >> Received call for ID {button_id}")
        # time.sleep(3) # This makes the spinner spin for 3 seconds
        # return {"status": "success", "message": "Insert target IDS Mock response"}
        # --- MOCK MODE END ---
        """
        Updates the signal_id in word_input table of eip_signal database based on the mapping in app_config.json.
        """
        conn = None
        cur = None
        try:
            # Fetch mapping from the config loader internally checks if the JSON file was updated
            # 1. This now returns the LIST of tuples/lists directly
            creates_raw = self.cfg.get_insert_target_ids_by_button(button_id)
    
            # Convert list of lists to list of tuples manually
            creates = [tuple(x) for x in creates_raw]
            
            logging.info(f"[WCSRepository >> insert_target_ids() >> 部品を呼ぶためAMR信号に入力したIDs.]: {creates}")

            if not creates:
                logging.info(f"[WCSRepository >> insert_target_ids() >> No found 部品を呼ぶためAMR信号に入力したIDs.]: {creates}")
                return

            kanban_map = {
                # Bライン (button_id 1～6 R1,R2,R3,L1,L2,L3)
                1: 2001, 2: 2002, 3: 2003, 
                4: 2004, 5: 2005, 6: 2006, 
                # Aライン (button_id 7～12 R1,R2,R3,L1,L2,L3)
                # 7: 1001, 8: 1002, 9: 1003, 
                # 10: 1004, 11: 1005, 12: 1006
            } 

            step_kanban_no = kanban_map.get(button_id)

            # Connect for flowrack update
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor(dictionary=True)

            # ✅ Fetch shelf status for specific shelf_codes
            if button_id in (3, 6, 9, 12): # Bライン➞R3,L3  / Aライン➞R3,L3  
                group_key = "L3_R3"
            else: # Bライン➞R1,R2,L1,L2  / Aライン➞R1,R2,L1,L2
                group_key = "R1_R2_L1_L2"

            # Fetch from config loader
            shelf_codes = self.cfg.get_shelf_codes_group(group_key)

            # Logging the result
            logging.info(f"[WCSRepository >> insert_target_ids()] Group: {group_key}, Codes: {shelf_codes}")

            if not shelf_codes:
                return []

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
            logging.info(f"[WCSRepository >> insert_target_ids() >> Found {len(empty_rows)} EMPTY shelves.]")

            if not empty_rows:
                logging.error("[WCSRepository >> insert_target_ids() >> No EMPTY shelves found for given shelf_codes.]")
                conn.rollback()
                return

            # ✅ Update t_shelf_status with new step_kanban_no for the first EMPTY shelf
            update_sql = """
                UPDATE `futaba-chiryu-3building`.t_shelf_status
                SET step_kanban_no = %s
                WHERE shelf_code = %s
            """
            cur.execute(update_sql, (step_kanban_no, empty_rows[0]["shelf_code"]))
            logging.info(f"[WCSRepository >> insert_target_ids() >> Updated t_shelf_status]: shelf_code={empty_rows[0]['shelf_code']} -> step_kanban_no={step_kanban_no}")

            # ✅ Execute the update
            cur.executemany(
                "UPDATE `eip_signal`.word_input SET value = %s WHERE signal_id = %s",
                creates
            )
            conn.commit()
            logging.info(f"[WCSRepository >> insert_target_ids() >> Signal updates completed for button_id] : {button_id}")


        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"[WCSRepository >> insert_target_ids() >> エラー]: {e}")
            raise Exception(f"[WCSRepository >> insert_target_ids() >> エラー]: {e}")
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # TODO➞リン: 間口に搬送対象を呼び出す、IDsをAMR信号に入れした後で部品を呼び出し
    def call_target_ids(self, button_id):
        # --- MOCK MODE START ---
        # logging.info(f"MOCK: Call target ids >> Received call for ID {button_id}")
        # time.sleep(3) # This makes the spinner spin for 3 seconds
        # return { "status": "success", "message": "Call target IDS Mock response",  "processing_status": "completed", "updated_count": 5 }
        # --- MOCK MODE END ---
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if button_id in (1, 7): # ( Bライン=> R1 button_id 1, Aライン=> R1 button_id 7)
                signal_ids = (8061, 8046, 8031, 8016, 8000) # ( Bライン/ Aライン, R1 => 5,4,3,2,1)

            elif button_id in (2, 8): # ( Bライン=> R2 button_id 2, Aライン=> R2 button_id 8)
                signal_ids = (8061, 8046, 8031, 8016, 8000) # ( Bライン/ Aライン, R2 => 5,4,3,2,1)

            elif button_id in (3, 9): # ( Bライン=> R3 button_id 3, Aライン=> R3 button_id 9)
                signal_ids = (8060, 8046, 8031) # ( Bライン/ Aライン, R3 => 5,4,3)

            elif button_id in (4, 10): # ( Bライン=> L1 button_id 4, Aライン=> L1 button_id 10)
                signal_ids = (8260, 8246, 8231, 8216, 8201) # ( Bライン/ Aライン, L1 => 5,4,3,2,1)

            elif button_id in (5, 11): # ( Bライン=> L2 button_id 5, Aライン=> L2 button_id 11)
                signal_ids = (8260, 8246, 8231, 8216, 8201) # ( Bライン/ Aライン, L2 => 5,4,3,2,1)

            elif button_id in (6, 12): # ( Bライン=> L3 button_id 6, Aライン=> L3 button_id 12)
                signal_ids = (8231, 8216, 8200) # ( Bライン/ Aライン, L3 => 3,2,1)

            else:
                logging.error(f"[WCSRepository >> call_target_ids() >> Invalid button_id]: {button_id}")
                raise ValueError(f"[WCSRepository >> call_target_ids() >> Invalid button_id]: {button_id}")

            placeholders = ','.join(['%s'] * len(signal_ids))
            sql = f"UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id IN ({placeholders})"
            cur.execute(sql, signal_ids)

            logging.info(f"[WCSRepository >> call_target_ids() >> Updated IDs]: {signal_ids}")

            conn.commit()
        
            return {
                "status": "success", 
                "processing_status": "completed",
                "updated_count": cur.rowcount
            }

            # --- STEP 3: Polling for ANY using_flag == 1 ---
            # TODO: リン. May be supported later by 平野さん
            # check_sql = "SELECT COUNT(*) FROM `futaba-chiryu-3building`.t_location_status WHERE using_flag = 1"
            
            # max_wait = 45  # Seconds to wait for AMR
            # success = False
            
            # for _ in range(max_wait):
            #     cur.execute(check_sql)
            #     result = cur.fetchone()
                
            #     # If at least one row has using_flag = 1
            #     if result and result[0] > 0:
            #         success = True
            #         break
                
            #     time.sleep(1)
            #     conn.ping(reconnect=True) 

            # if success:
            #     logging.info(f"[WCSRepository >> call_target_ids() >> using_flag = 1 detected]: {result}")
            #     return {"status": "success", "processing_status": "completed"}
            # else:
            #     # If no flag was seen after 45 seconds, we timeout
            #     return {"status": "timeout", "message": "No AMR activity >> using_flag = 1 detected"}
        
        except Exception as e:
            if conn:
                conn.rollback()
                logging.error(f"[WCSRepository >> call_target_ids() >> エラー]: {button_id}")
            raise Exception(f"[WCSRepository >> call_target_ids() >> エラー]: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # デパレ箱数登録
    def dispallet(self, depallet_area):
        logging.info("[WCSRepository >> dispallet] Function called")

        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            logging.info(f"[WCSRepository >> dispallet] Incoming depallet_area: {depallet_area}")

            # Mapping table for signal_id
            signal_map = {
                "20": 8405, 
                "21": 8411, 
                "22": 8417, 
                "23": 8423, 
                "24": 8429,
                "25": 8505, 
                "26": 8511, 
                "27": 8517, 
                "28": 8523, 
                "29": 8529
            }

            for area_key, area_value in depallet_area.items():

                if area_key not in signal_map:
                    logging.warning(f"[WCSRepository >> dispallet] Unknown depallet area: {area_key}, skipping")
                    continue

                signal_id = signal_map[area_key]

                # Validate structure
                if not isinstance(area_value, list) or len(area_value) == 0:
                    logging.error(f"[WCSRepository >>dispallet] Invalid data format for area {area_key}: {area_value}")
                    continue

                data = area_value[0]
                # RECOMMENDED: Use the config loader directly for the most up-to-date value
                kanban_no = area_value[0].get("kanban_no") 
                num_str = self.cfg.get_take_count(kanban_no) # This triggers reload_if_changed()

                if "take_count" not in data:
                    logging.error(f"[WCSRepository >> dispallet] Missing take_count for area {area_key}: {data}")
                    continue

                try:
                    num = abs(int(data["take_count"]))
                except Exception:
                    logging.error(f"[WCSRepository >> dispallet] Invalid take_count value for area {area_key}: {data['take_count']}")
                    continue

                logging.info(f"[WCSRepository >> dispallet] Updating signal_id={signal_id} with value={num}")

                # Execute update
                result = cur.execute(
                    """
                    UPDATE eip_signal.word_input
                    SET value = %s
                    WHERE signal_id = %s
                    """,
                    (num, signal_id)
                )

                # Log update result
                if result == 0:
                    logging.warning(f"[WCSRepository >> dispallet] UPDATE executed but NO ROW matched signal_id={signal_id}")
                else:
                    logging.info(f"[WCSRepository >> dispallet] UPDATE SUCCESS: {result} row(s) updated for signal_id={signal_id}")

                # Optional: verify DB value
                cur.execute("SELECT value FROM eip_signal.word_input WHERE signal_id=%s", (signal_id,))
                row = cur.fetchone()
                logging.info(f"[dispallet] DB value after update for {signal_id}: {row}")

            logging.info("[dispallet] Committing transaction...")
            conn.commit()
            logging.info("[dispallet] Commit successful")

        except Exception as e:
            logging.error(f"[dispallet] ERROR: {e}", exc_info=True)
            conn.rollback()
            raise Exception(f"[dispallet] Transaction rolled back due to error: {e}")

        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

        logging.info("[dispallet] Function completed")
        return
    
    # TODO➞リン: get_empty_kotatsu_status
    def get_empty_kotatsu_status(self):
        conn = None
        cur = None
        try:
            conn = self.db.wcs_pool.get_connection()
            # Use dictionary=True so we can access columns by name
            cur = conn.cursor(dictionary=True) 

            # SQL Logic:
            # 1. Join t_shelf_status with t_location_status to confirm existence.
            # 2. Join m_product to get the supplier name.
            # 3. Filter for 'EMPTY' status and 'K' prefix.
            # 4. Group by supplier and sort by the OLDEST (MIN) update time.
            filter_sql = """
                SELECT mp.supplier_name
                FROM `futaba-chiryu-3building`.t_shelf_status AS ts
                INNER JOIN `futaba-chiryu-3building`.t_location_status AS tl
                    ON ts.shelf_code = tl.shelf_code
                INNER JOIN `futaba-chiryu-3building`.m_product AS mp 
                    ON ts.step_kanban_no = mp.kanban_no
                WHERE ts.kotatsu_status = %s 
                AND ts.shelf_code LIKE 'K%%'
                ORDER BY ts.update_datetime ASC
            """

            cur.execute(filter_sql, ("EMPTY",))
            results = cur.fetchall()

            if not results:
                logging.info("[WCSRepository >> get_empty_kotatsu_status() >> No EMPTY K-shelves found.]")
                return [] # Return empty list if no data

            # Create a clean list of strings: ["Supplier A", "Supplier B"]
            supplier_list = [row["supplier_name"] for row in results]
            
            logging.info(f"[WCSRepository >> get_empty_kotatsu_status() >> Found {len(supplier_list)} suppliers in order.]")
            return supplier_list

        except Exception as e:
            logging.error(f"[WCSRepository >> get_empty_kotatsu_status() >> エラー]: {e}")
            raise Exception(f"[WCSRepository >> get_empty_kotatsu_status() >> エラー]: {e}")
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # TODO➞リン: check_kotatsu_fill_or_not
    def check_kotatsu_fill_or_not(self):
        conn = None
        cur = None
        try:
            conn = self.db.wcs_pool.get_connection()
            cur = conn.cursor(dictionary=True) 

            # 1. Join tables immediately to get all valid status records
            sql = """
                SELECT ts.kotatsu_status, ts.step_kanban_no
                FROM `futaba-chiryu-3building`.t_shelf_status AS ts
                INNER JOIN `futaba-chiryu-3building`.t_location_status AS tl
                    ON ts.shelf_code = tl.shelf_code
                INNER JOIN `futaba-chiryu-3building`.m_product AS mp 
                    ON ts.step_kanban_no = mp.kanban_no
                WHERE ts.kotatsu_status = %s
                ORDER BY ts.update_datetime ASC
            """
            cur.execute(sql, ("FILL",))
            results = cur.fetchall()

            # MOCK: START
            # results = [
            #     {'kotatsu_status': 'NO_FILL', 'step_kanban_no': 'サ607'},
            #     {'kotatsu_status': 'NO_FILL', 'step_kanban_no': '3202'}, 
            #     {'kotatsu_status': 'NO_FILL', 'step_kanban_no': 'オ070'}, 
            #     {'kotatsu_status': 'NO_FILL', 'step_kanban_no': 'T704'}, 
            #     # {'kotatsu_status': 'FILL', 'step_kanban_no': '5121'},
            #     # {'kotatsu_status': 'FILL', 'step_kanban_no': 'サ607'}, 
            #     # {'kotatsu_status': 'FILL', 'step_kanban_no': '5140'},
            #     # {'kotatsu_status': 'FILL', 'step_kanban_no': 'T621'} 
            # ];
            # MOCK: END

            # 2. Logic Handling:
            # Check if ANY of the retrieved records have the status "FILL"
            has_fill = any(row["kotatsu_status"] == "FILL" for row in results)

            if has_fill:
                # If "FILL" exists in the results, return an empty list
                logging.info(f"[WCSRepository] 'FILL' status found in joined records. Returning empty list: {results}")
                return []
            else:
                # If "FILL" does NOT exist, return the list of kanban numbers
                logging.info("[WCSRepository] No 'FILL' status found. Returning kanban list.")
                return [row["step_kanban_no"] for row in results]

        except Exception as e:
            logging.error(f"[WCSRepository >> check_kotatsu_fill_or_not() >> Error]: {e}")
            raise e
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

# add sugiura ###################################################
    # デパレ箱数登録
    # def dispallet(self, depallet_area):
    #     try:
    #         conn = self.db.wcs_pool.get_connection()
    #         conn.start_transaction()
    #         cur = conn.cursor()

    #         logging.info(f"[WCSRepository >> dispallet() >> depallet_area]: {depallet_area}")

    #         for i in depallet_area:
    #             id = None
    #             data = None
    #             if i == "20":
    #                 id = 8405
    #                 data = depallet_area[i][0]
    #             elif i == "21":
    #                 id = 8411
    #                 data = depallet_area[i][0]
    #             elif i == "22":
    #                 id = 8417
    #                 data = depallet_area[i][0]
    #             elif i == "23":
    #                 id = 8423
    #                 data = depallet_area[i][0]
    #             elif i == "24":
    #                 id = 8429
    #                 data = depallet_area[i][0]
    #             elif i == "25":
    #                 id = 8505
    #                 data = depallet_area[i][0]
    #             elif i == "26":
    #                 id = 8511
    #                 data = depallet_area[i][0]
    #             elif i == "27":
    #                 id = 8517
    #                 data = depallet_area[i][0]
    #             elif i == "28":
    #                 id = 8523
    #                 data = depallet_area[i][0]
    #             elif i == "29":
    #                 id = 8529
    #                 data = depallet_area[i][0]

                

    #             num = abs(int(data["take_count"]))
    #             result = cur.execute("""
    #                         UPDATE `eip_signal`.word_input
    #                         SET value = %s
    #                         WHERE signal_id = %s
    #                         """, (num, id,))
                
    #             logging.info(f"[WCSRepository >> dispallet() >> Query result]: {result}")

    #         conn.commit()

    #     except Exception as e:
    #         conn.rollback()
    #         raise Exception(f"[WCSRepository >> dispallet() >> Error] : {e}")

    #     finally:
    #         cur.close()
    #         conn.close()
    #     return


if __name__ == "__main__":
    from mysql_db import MysqlDb
    from depallet_area_repository import WCSRepository
    from line_repository import LineRepository
    from domain.models.shelf import FlowRack
    db = MysqlDb()
    w_repo = WCSRepository(db)
    d_repo = WCSRepository(db)
    l_repo = LineRepository(db)
    area = d_repo.get_depallet_area((1,2))
    lines = l_repo.get_lines((1, 2, 3, 4))
    f=area.get_empty_frontage()
    w_repo.request_flow_rack(f,lines[0].get_by_id(1))
    flow_rack = FlowRack("1")
    f.set_shelf(flow_rack)
    f=area.get_empty_frontage()
    part = lines[0].get_by_id(1).inventories[0].part
    w_repo.request_kotatsu(f,part)

