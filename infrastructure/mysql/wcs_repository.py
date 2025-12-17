import time

from domain.infrastructure.wcs_repository import IWCSRepository
from domain.models.depallet import DepalletFrontage
from domain.models.line import LineFrontage
from domain.models.part import Part

from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS  # ログ用
import logging

# ログ出力開始
LOG_FOLDER = "../log"
LOG_FILE = "debug_logging.log"
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

class WCSRepository(IWCSRepository):

    def __init__(self, db):
        self.db = db

    # 部品要求
    def request_kotatsu(self, frontage: DepalletFrontage, part: Part):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if frontage.shelf is not None:
                raise Exception("[DepalletAreaRepository] Shelf already exists")

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
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
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
                raise Exception("[DepalletAreaRepository] Shelf already exists")

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
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
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
                raise Exception("[DepalletAreaRepository] No shelf in frontage")

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
            raise Exception(f"[DepalletAreaRepository] Error: {e}")

        finally:
            cur.close()
            conn.close()
        return

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
    
    def dispallet(self, depallet_area):
        logging.info("[WCSRepository >> dispallet] Function called")

        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            logging.info(f"[WCSRepository >> dispallet] Incoming depallet_area: {depallet_area}")

            # Mapping table for signal_id
            signal_map = {
                "20": 8405, "21": 8411, "22": 8417, "23": 8423, "24": 8429,
                "25": 8505, "26": 8511, "27": 8517, "28": 8523, "29": 8529
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







if __name__ == "__main__":
    from mysql_db import MysqlDb
    from depallet_area_repository import DepalletAreaRepository
    from line_repository import LineRepository
    from domain.models.shelf import FlowRack
    db = MysqlDb()
    w_repo = WCSRepository(db)
    d_repo = DepalletAreaRepository(db)
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
