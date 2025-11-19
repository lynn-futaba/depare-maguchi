from domain.models.shelf import Kotatsu ,Shelf, FlowRack
from domain.models.part import Inventory, Part ,KotatsuInventory

from domain.models.depallet import DepalletArea, DepalletFrontage
from domain.models.line import LineFrontage

from domain.infrastructure.depallet_area_repository import IDepalletAreaRepository

#mysql実装
class DepalletAreaRepository(IDepalletAreaRepository):
    def __init__(self,db):
         self.db =db
        
    def get_depallet_area(self,line_id_list:list)->DepalletArea:
        try:

            sql =f"SELECT frontage_id,name,priority,cell_code FROM depal.depallet_frontage"\
                      +" join depal.line_depallet_frontage using (frontage_id)"\
                    + " where line_id in " + str(tuple(line_id_list)) \
                     + " group by frontage_id,name,priority,cell_code"
            print(f"SQL Query Result >> DepalletAreaRepository -> get_depallet_area :{sql}")


            conn =self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)
    
            cur.execute(sql)
            result= cur.fetchall()

            area = DepalletArea("A")
            for row in   result:
                frontege = DepalletFrontage(str(row["cell_code"]),row["frontage_id"],row["name"],row["priority"])     
                area.register_frontage(frontege)

            cur.close()
            conn.close()
            for frontage in area.frontages.values():
                sql =f"SELECT * FROM depal.signal WHERE frontage_id={frontage.id};"
                conn =self.db.depal_pool.get_connection()
                cur = conn.cursor(dictionary=True)
                cur.execute(sql)
                result= cur.fetchall()
                signals = {}
                for row in result:

                    signals[row["tag"]] = int(row["signal_id"])

                frontage.signals = signals
                
                cur.close()
                conn.close()
                shelf= self.get_shelf(frontage)
                if shelf is not None:
                    frontage.set_shelf(shelf)
        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        return area

    # TODO
    # def get_depallet_area(self, line_id_list: list) -> DepalletArea:
    #     try:
    #         if not line_id_list:
    #             raise Exception("line_id_list is empty")
    #         # Build SQL safely - note: str(tuple(...)) works only if len >1, else needs special handling
    #         if len(line_id_list) == 1:
    #             in_clause = f"({line_id_list[0]})"
    #         else:
    #             in_clause = str(tuple(line_id_list))
    #         sql = (
    #             "SELECT frontage_id, name, priority, cell_code FROM depal.depallet_frontage "
    #             "JOIN depal.line_depallet_frontage USING (frontage_id) "
    #             f"WHERE line_id IN {in_clause} "
    #             "GROUP BY frontage_id, name, priority, cell_code"
    #         )
    #         conn = self.db.get_connection('depal')
    #         cur = conn.cursor(dictionary=True)
    #         cur.execute(sql)
    #         result = cur.fetchall()
    #         area = DepalletArea("A")
    #         for row in result:
    #             frontage = DepalletFrontage(
    #                 str(row["cell_code"]),
    #                 row["frontage_id"],
    #                 row["name"],
    #                 row["priority"],
    #             )
    #             area.register_frontage(frontage)
    #         # Prepare signal query once, use parameterized queries inside loop
    #         signal_sql = "SELECT * FROM depal.signal WHERE frontage_id = %s;"
    #         for frontage in area.frontages.values():
    #             cur.execute(signal_sql, (frontage.id,))
    #             signals = {row["tag"]: int(row["signal_id"]) for row in cur.fetchall()}
    #             frontage.signals = signals
    #             shelf = self.get_shelf(frontage)
    #             if shelf is not None:
    #                 frontage.set_shelf(shelf)
    #         cur.close()
    #         conn.close()
    #     except Exception as e:
    #         raise Exception(f"[DepalletAreaRepository] Error: {e}")
    #     return area

    def is_frontage_ready(self, frontage:DepalletFrontage)->bool:
        try:
            signal_id = frontage.signals["ready"]
            sql =f"SELECT * FROM `eip_signal`.word_output WHERE signal_id={signal_id};"
            conn =self.db.eip_signal_pool.get_connection()
            cur = conn.cursor(dictionary=True)
    
            cur.execute(sql)
            result= cur.fetchall()
            value = None
            for row in   result:

                if row["value"] == 1:
                   value = True
                else:
                    value = False
          
            cur.close()
            conn.close()

        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        return value

    def get_shelf(self, frontage: DepalletFrontage) -> Shelf:
        try:
            if self.is_frontage_ready(frontage)==False:
                return None
            kotatsu = self.get_kotatsu(frontage)
            if kotatsu is not None:
                return kotatsu
            flow_rack = self.get_flow_rack(frontage)
            if flow_rack is not None:
                return flow_rack
        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        return None
        
    def get_kotatsu(self, frontage: DepalletFrontage) -> Kotatsu:
        parts_tag_list = ["part1_no", "part2_no", "part3_no", "part4_no", "part5_no", "part6_no","part1_count", "part2_count",
                          "part3_count", "part4_count", "part5_count", "part6_count"]
        try:

            parts_signals = [frontage.signals[k] for k in parts_tag_list if k in frontage.signals]
            parts_signals = tuple( parts_signals)
      
            sql =f"SELECT * FROM `eip_signal`.word_output WHERE signal_id IN {parts_signals} ORDER BY signal_id;"
            conn =self.db.eip_signal_pool.get_connection()
            cur = conn.cursor(dictionary=True)
    
            cur.execute(sql)
            result= cur.fetchall()
            inventory_list = []
            
            for i,( no, count) in enumerate(zip(result[::2], result[1::2]),start=1):
                if no["value"]==0:
                    continue
                # とりあえず背番号のみの部品として扱う
                inventory = KotatsuInventory(0, Part(str(no["value"]),str(no["value"]),str(no["value"]),0), int(count["value"]), 
                                             frontage.signals[f"fetch{i}"],frontage.signals[f"fetch{i}_count"],frontage.signals[f"part{i}_no"],frontage.signals[f"part{i}_count"])
                inventory_list.append(inventory)
          
            cur.close()
            conn.close()
            
            if len(inventory_list) ==0:
                return None
            kotatsu = Kotatsu('kotatsu', inventory_list)
        except Exception as e:
            raise Exception(f"[DepalletAreaRepository] Error: {e}")
        return  kotatsu

    def get_flow_rack(self,frontage:LineFrontage)->FlowRack:
        try:
          
            sql =f"SELECT * FROM depal.line_inventory "\
            + "INNER JOIN depal.rack_position as r USING(inventory_id) "\
            + "INNER JOIN depal.m_product USING(part_number) "\
            + f"RIGHT JOIN depal.position as p on r.rack_position_id = p.rack_position_id  and frontage_id ={frontage.id} "\
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

if __name__ == "__main__":
    from mysql_db import MysqlDb
    db = MysqlDb()
    repo = DepalletAreaRepository(db)
    area = repo.get_depallet_area((1,2))
    f=area.get_empty_frontage()
    print(f.id)
    for f in area.frontages.values():
       r=repo.get_flow_rack(f)
       print(r)
       # #print(f.signals)
       # status = repo. is_frontage_ready(f)
       # # print(status)
       # k=repo.get_kotatsu(f)
       
       # if k is None:
       #     continue
       # f.set_shelf(k)
       # for inv in f.shelf.inventories:
       #     print(f"Part No: {inv.part.kanban_id}, Count: {inv.case_quantity}")
       #     inv.remove(2)

       # repo.save_kotatsu(f)
   

           

      

