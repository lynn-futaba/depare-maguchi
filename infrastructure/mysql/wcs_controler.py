import time

from domain.infrastructure.wcs_controler import IWcsControler
from domain.models.depallet import  DepalletFrontage
from domain.models.line import LineFrontage
from domain.models.part import Part

class WcsControler(IWcsControler):
    
    def __init__(self,db):
         self.db =db

    # 部品要求
    def request_kotatsu(self,frontage:DepalletFrontage,part:Part):
        try:
            conn =self.db.wcs_pool.get_connection()
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
    def request_flow_rack(self,frontage:DepalletFrontage,line_frontage:LineFrontage):
        try:
            conn =self.db.wcs_pool.get_connection()
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
    
    def dispatch(self,frontage:DepalletFrontage):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if frontage.shelf is None:
               raise Exception("[DepalletAreaRepository] No shelf in frontage")

            signal_id = frontage.signals["dispatch"]
            cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s", (signal_id,))  
            conn.commit()

            # 一秒後に再度リクエスト信号を0に戻す
            time.sleep(1)
            conn.start_transaction()
            cur.execute("UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id = %s", (signal_id,))  
            conn.commit()
               
        except Exception as e:
            conn.rollback()
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        
        finally:
            cur.close()
            conn.close()
        return  

if __name__ == "__main__":
    from mysql_db import MysqlDb
    from depallet_area_repository import DepalletAreaRepository
    from line_repository import LineRepository
    from domain.models.shelf import FlowRack
    db = MysqlDb()
    w_repo = WcsControler(db)
    d_repo = DepalletAreaRepository(db)
    l_repo = LineRepository(db)
    area = d_repo.get_depallet_area((1,2))
    lines = l_repo.get_lines((1, 2))
    
    f=area.get_empty_frontage()
    w_repo.request_flow_rack(f,lines[0].get_by_id(1))
    flow_rack = FlowRack("1")
    f.set_shelf(flow_rack)


    f=area.get_empty_frontage()
    
    part = lines[0].get_by_id(1).inventories[0].part
    w_repo.request_kotatsu(f,part)

    

