from domain.models.line import Line, LineFrontage
from domain.models.part import Part, Inventory
from domain.models.shelf import FlowRack

from domain.infrastructure.line_repository import ILineRepository

#mysql実装
class LineRepository(ILineRepository):
    def __init__(self,db):
         self.db =db

    # def get_lines(self,line_id_list:list)->list[Line]:
    #     lines = [] # TODO: この行を追加しました
    #     try:
    #         sql =f"SELECT * FROM depal.line where line_id in {line_id_list};"
    #         conn =self.db.depal_pool.get_connection()
    #         cur = conn.cursor(dictionary=True)
    #         cur.execute(sql)
    #         result= cur.fetchall()
    #         print(f"[Line Table >>] Result: {result}")

    #         # lines = [] # TODO: 川島さんのコードをコメントアウトする
    #         for row in result:
    #             line = Line(row["line_id"],row["name"],row["process"])
    #             lines.append(line)

    #         for line in lines:
    #             sql =f"SELECT * FROM depal.line_frontage where line_id = {line.id};"
    #             cur.execute(sql)

    #             result = cur.fetchall()
    #             print(f"[Line Frontage >>] Result: {result}")

    #             for row in result:
    #                 frontage_obj = LineFrontage(row["cell_code"],row["name"], row["frontage_id"],row["car_model_id"])
    #                 line.register_frontage(frontage_obj)
        
    #             for frontage in line.frontages.values():
    #                 sql = f"SELECT * FROM depal.line_inventory inner join depal.m_product using(part_number) where frontage_id = {frontage.id};"
    #                 cur.execute(sql, (frontage.id,))
    #                 inv = cur.fetchall()
    #                 print(f"[Line Inventory >>] Result: {inv}")
    #                 inventories = []
    #                 for row in inv:
    #                     inventory = Inventory(row["inventory_id"],Part(row["part_number"],row["kanban_no"],row["name"],row["car_model_id"]), row["case_quantity"])
    #                     inventories.append(inventory)
    #                 frontage.set_inventories(inventories)

    #         cur.close()
    #         conn.close()
    #     except Exception as e:
    #         print(f"[LineRepository] Error: {e}")

    #     return lines

    def get_lines(self, line_id_list: list) -> list[Line]:
        lines = []
        conn = None
        cur = None

        try:
            # Get DB connection
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            # 1. Fetch lines
            sql = f"SELECT * FROM depal.line WHERE line_id IN ({','.join(['%s'] * len(line_id_list))})"
            cur.execute(sql, line_id_list)
            result = cur.fetchall()
            print(f"[Line Table >>] Result: {result}")

            for row in result:
                line = Line(row["line_id"], row["name"], row["process"])
                lines.append(line)

            # 2. Fetch frontages for each line
            for line in lines:
                sql = "SELECT * FROM depal.line_frontage WHERE line_id = %s"
                cur.execute(sql, (line.id,))
                frontages_result = cur.fetchall()
                print(f"[Line Frontage >>] Result: {frontages_result}")

                for row in frontages_result:
                    frontage_obj = LineFrontage(row["cell_code"], row["name"], row["frontage_id"], row["car_model_id"])
                    line.register_frontage(frontage_obj)

                # 3. Fetch inventories for each frontage
                for frontage in line.frontages.values():

                    sql = f"SELECT * FROM depal.line_inventory inner join depal.m_product using(part_number) where frontage_id = {frontage.id};"
                    cur.execute(sql, (frontage.id,))

                    
                    inv_result = cur.fetchall()
                    print(f"[Line Inventory >>] Result: {inv_result}")

                    inventories = []
                    for row in inv_result:
                        # part = Part(row["part_number"], row["kanban_no"], row["name"], row["car_model_id"])
                        part = Part(row["part_number"], row["kanban_no"], "name", row["car_model_id"])
                        inventory = Inventory(row["inventory_id"], part, row["case_quantity"])
                        inventories.append(inventory)

                    frontage.set_inventories(inventories)

        except Exception as e:
            print(f"[LineRepository] Error: {e}")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        return lines

    def  supply_parts(self,flow_rack:FlowRack):
        if flow_rack.is_empty():
            raise Exception("FlowRack is empty")
        Values = []
        for inventory in flow_rack.rack:
            if  inventory is None or inventory.is_empty():
                continue
            Values.append([inventory.id,inventory.case_quantity])
        try:
            sql = "INSERT INTO depal.parts_supply (inventory_id,case_quantity) VALUES (%s,%s);"
            conn = self.db.depal_pool.get_connection()
            cur = conn.cursor()
            cur.executemany(sql, Values)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[LineRepository] Error: {e}")
        

if __name__ == "__main__":
    repo = LineRepository()
    lines = repo.get_lines((1,2))
    for line in lines:
        print(line.name)
        for f in line.frontages.values():
            print(f.id)
            for i in f.inventories:
                print(i)
      
    # flow_rack = FlowRack(1)
    # inventory = Inventory(1, Part(1, "A", "partA"), 5)
    # flow_rack.set_inventories([inventory])
    # repo.supply_line_area(flow_rack)


