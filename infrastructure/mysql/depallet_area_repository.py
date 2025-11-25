from domain.models.shelf import Kotatsu ,Shelf, FlowRack
from domain.models.part import Inventory, Part ,KotatsuInventory

from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.line import LineFrontage

from domain.infrastructure.depallet_area_repository import IDepalletAreaRepository


import json
import os

#mysql実装
class DepalletAreaRepository(IDepalletAreaRepository):

    def __init__(self,db):

        self.db =db
        
        # TODO : Load config dynamically
        config_path = os.path.join(os.path.dirname(__file__), "../../config/take_count_config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            self.take_count_map = json.load(f)

    # TODO: Get take count
    def get_take_count(self, kanban_no: str) -> str:
            """Return take_count for given kanban_no from config."""
            return self.take_count_map.get(kanban_no, "-0")

        
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

            print(f"[Get_kotatsu >> parts_signals >> Result] : {parts_signals}")
      
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

    def update_maguchi_signal_input(self, line_frontage_id):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            updates = []  # Initialize empty list (values,signals)

            if line_frontage_id == 1: # Bライン, R1 => 5,4,3,2,1
                updates = [ # (values,signals)
                    (107, 8404),
                    (103, 8403),
                    (105, 8402),
                    (106, 8401),
                    (18, 8400)
                ]
            elif line_frontage_id == 2: # Bライン, R2 => 5,4,3,2,1
                updates = [
                    (102, 8404),
                    (108, 8403),
                    (101, 8402),
                    (104, 8401),
                    (21, 8400)
                ]
            elif line_frontage_id == 3: # Bライン, R3 => 5,4,3
                updates = [
                    (23, 8404),
                    (100, 8403),
                    (301, 8402)
                ]
            elif line_frontage_id == 4: # Bライン, L1 => 5,4,3,2,1
                updates = [
                    (26, 8504),
                    (206, 8503),
                    (205, 8502),
                    (203, 8501),
                    (208, 8500)
                ]
            elif line_frontage_id == 5: # Bライン, L2 => 5,4,3,2,1
                updates = [
                    (29, 8504),
                    (204, 8503),
                    (201, 8502),
                    (207, 8501),
                    (202, 8500)
                ]
            elif line_frontage_id == 6: # Bライン, L3 => 5,4,3,2,1
                updates = [
                    (300, 8502),
                    (200, 8501),
                    (31, 8500)
                ]

            if updates:  # Only execute if updates list is not empty
                cur.executemany(
                    "UPDATE `eip_signal`.word_input SET value = %s WHERE signal_id = %s",
                    updates
                )
                # print(f"[Update_maguchi_signal_input >> Updated] : {updates}")
                conn.commit()
            else:
                print(f"No updates for line_frontage_id: {line_frontage_id}")

        except Exception as e:
            conn.rollback()
            raise Exception(f"[update_maguchi_signal_input] Error: {e}")
        finally:
            cur.close()
            conn.close()
            
    def to_maguchi_set_values(self, line_frontage_id):
        try:
            conn = self.db.wcs_pool.get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            if line_frontage_id == 1: # Bライン, R1 => 5,4,3,2,1
                signal_ids = (8061, 8046, 8031, 8016, 8000)

            elif line_frontage_id == 2: # Bライン, R2 => 5,4,3,2,1
                signal_ids = (8061, 8046, 8032, 8016, 8000)

            elif line_frontage_id == 3: # Bライン, R3 => 5,4,3
                signal_ids = (8060, 8046, 8032)

            elif line_frontage_id in (4, 5): # Bライン, L1, L2 => 5,4,3,2,1
                signal_ids = (8260, 8246, 8231, 8216, 8201)

            elif line_frontage_id == 6: # Bライン, L3 => 5,4,3
                signal_ids = (8231, 8216, 8200)

            else:
                raise ValueError(f"Invalid line_frontage_id: {line_frontage_id}")

            placeholders = ','.join(['%s'] * len(signal_ids))
            sql = f"UPDATE `eip_signal`.word_input SET value = 1 WHERE signal_id IN ({placeholders})"
            cur.execute(sql, signal_ids)

            print(f"[to_maguchi_set_values >> Updated IDs]: {signal_ids}")

            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"[to_maguchi_set_values] Error: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    
    def update_depallet_area(self, plat_list: list = None):
        """
        Build update_frontages for plats 20–29 (or custom plat_list).
        Each plat key contains a list of shelf details.
        """
        conn = None
        cur = None
        try:
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            # ✅ Prepare plat filter
            if not plat_list:
                plat_list = [str(i) for i in range(20, 30)]  # Default: 20–29

            placeholders = ','.join(['%s'] * len(plat_list))

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

            cur.execute(sql, plat_list)
            rows = cur.fetchall()

            update_frontages = {}
            for row in rows:
                plat_value = row["plat"]
                if plat_value not in update_frontages:
                    update_frontages[plat_value] = []
                    update_frontages[plat_value].append({
                    "step_kanban_no": row["step_kanban_no"],
                    "load_num": row["load_num"],
                    "shelf_code": row["shelf_code"],
                    "take_count": self.take_count_map.get(row["step_kanban_no"], "-0")
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

    
    # # TODO: retrieve plat 
    # def _get_first_plat(self, cur, shelf_code):
    #     """Helper to get first plat for a shelf_code."""
    #     cell_code_sql = """
    #     SELECT cell_code FROM `futaba-chiryu-3building`.t_location_status
    #     WHERE shelf_code = %s;
    #     """
    #     cur.execute(cell_code_sql, (shelf_code,))
    #     cell_code_result = cur.fetchall()
    #     if not cell_code_result:
    #         return None

    #     first_cell_code = cell_code_result[0]["cell_code"]
    #     plat_sql = """
    #     SELECT plat FROM `futaba-chiryu-3building`.m_basis_location
    #     WHERE cell_code = %s;
    #     """
    #     cur.execute(plat_sql, (first_cell_code,))
    #     plat_result = cur.fetchall()
    #     return plat_result[0]["plat"] if plat_result else None


if __name__ == "__main__":
    from mysql_db import MysqlDb
    db = MysqlDb()
    repo = DepalletAreaRepository(db)
    area = repo.get_depallet_area((1,2,3,4)) # TODO: added 3,4
    new_area = repo.update_depallet_area((20, 21, 22, 23, 24, 25, 26, 27, 28, 29)) # TODO: added
    f = area.get_empty_frontage()
    print(f.id)
    for f in area.frontages.values():
       r = repo.get_flow_rack(f)
       print(r)
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
   

           

      

