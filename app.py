import os
import json
import time
import logging
import threading
import asyncio

from flask import Flask, render_template, request, jsonify, abort
from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS  # ログ用
from application.depallet_app import DepalletApplication

# ログ出力開始
LOG_FOLDER = "../log"
LOG_FILE = "app.py_logging.log"
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "./config/take_count_config.json")

class DepalletWebServer:
    def __init__(self, depallet_app):
        self._depallet_app = depallet_app
        self.app = Flask(__name__, static_folder='static')
        self.setup_routes()
        self.server_thread = None
        self.app.secret_key = 'secret_key'

    def start(self, host='0.0.0.0', port=5000):
          
            if self.server_thread is not None and self.server_thread.is_alive():
                logging.info("Web server is already running")
                return self
        
            def run_server():
                self.app.run(host=host, port=port, debug=False, threaded=True, use_reloader=False)
        
            self.server_thread = threading.Thread(target=run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            logging.info(f"Web server started at http://{host}:{port}")
            return self

    def setup_routes(self):
        """ルート設定"""
        app = self.app

        @app.route("/", methods=["GET"])
        def index():
             return render_template('index.html')

        @app.route("/return_index")
        def returns():
            return render_template('index.html')

        # @app.route("/maguchi")
        # def maguchi_page():
        #     return render_template('depallet/maguchi.html')

        # @app.route("/flow_rack")
        # def flow_rack_page():
        #     return render_template('depallet/flowrack.html') 

        @app.route("/depallet", methods=["GET"])
        def depallet():
            try:
                id_value = request.args.get("id")
                name_value = request.args.get("name")
                logging.info("[app.py >> depallet() >> 成功]")
                return render_template('depallet-maguchi.html', id = id_value, name = name_value)
            except Exception as e:
                logging.info(f"[app.py >> depallet() >> エラー] : {e}")
                return abort(400, 'Invalid request')
            
        @app.route("/a_line_depallet_maguchi", methods=["GET"])
        def a_line_depallet_maguchi():
            try:
                id_value = request.args.get("id")
                name_value = request.args.get("name")
                logging.info("[app.py >> a_line_depallet_maguchi() >> 成功]")
                return render_template('a-line-depallet-maguchi.html', id = id_value, name = name_value)
            except Exception as e:
                logging.info(f"[app.py >> a_line_depallet_maguchi() >> エラー] : {e}")
                return abort(400, 'Invalid request')

        @app.route("/api/get_product_infos",methods=["GET"])
        def get_product_infos():
            try:
                self._depallet_app.update_line_data()
                a_product_r, a_product_l, b_product_r, b_product_l = self._depallet_app.get_product_infos_json() # TODO➞リン: l,r to product_r, product_l
                line_area_json = self._depallet_app.get_lines_json()
                return [a_product_r, a_product_l, b_product_r, b_product_l, line_area_json] # TODO➞リン: l,r to product_r, product_l
            except Exception as e:
                return str(e), 500
            
        @app.route("/api/insert_kanban_nuki", methods=["GET"])
        def insert_kanban_nuki():
            try:
                logging.info("[app.py >> insert_kanban_nuki() >> 成功]")
                self._depallet_app.insert_kanban_nuki()
                return jsonify({"status": "success"})
            except Exception as e:
                logging.info(f"[app.py >> insert_kanban_nuki() >> エラー] : {e}")
                return abort(400, str(e))
        
        @app.route("/api/insert_kanban_sashi", methods=["GET"])
        def insert_kanban_sashi():
            try:
                logging.info("[app.py >> insert_kanban_sashi() >> 成功]")
                self._depallet_app.insert_kanban_sashi()
                return jsonify({"status": "success"})
            except Exception as e:
                logging.info(f"[app.py >> insert_kanban_sashi() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/line_frontage_click", methods=["POST"])
        def line_frontage_click():
            #クリックしたら部品とフローラックを呼ぶ
            id = request.json.get('frontage_id')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_in_executor(None, self._depallet_app.depallet_start, id)
                return jsonify({"status": "success"})

            except Exception as e:
                return abort(400, 'Invalid request')
            
        @app.route("/api/insert_target_ids", methods=["POST"])
        def insert_target_ids():
            try:
                line_frontage_id = request.json.get('line_frontage_id')
                logging.info("[app.py >> [insert_target_ids() >> 成功]")
                self._depallet_app.insert_target_ids(line_frontage_id)
                return jsonify({"status": "success"})
            except Exception as e:
                logging.error(f"[app.py >> insert_target_ids() >> エラー] : {e}")
                return abort(400, str(e))
            
        
        @app.route("/api/call_target_ids", methods=["POST"])
        def call_target_ids():
            try:
                line_frontage_id = request.json.get('line_frontage_id')
                logging.info("[app.py >> call_target_ids() >> 成功]")
                self._depallet_app.call_target_ids(line_frontage_id)
                return jsonify({"status": "success"})
            except Exception as e:
                logging.error(f"[app.py >> call_target_ids() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/get_depallet_area") # TODO➞リン: changed 
        def get_depallet_area():
            try:
                depallet_area = self._depallet_app.get_depallet_area_json()
                logging.info(f"[app.py >> get_depallet_area_by_plat() >> depallet_area] : {depallet_area}")
                return jsonify(depallet_area)
            except Exception as e:
                logging.error(f"[app.py >> get_depallet_area() >> エラー] : {e}")
                return abort(400, str(e))

        @app.route("/api/update_flow_rack")
        def update_flow_rack():
            try:
               flow_rack =self._depallet_app.get_flow_rack_json()
               return jsonify(flow_rack)
            except Exception as e:
                return abort(400, str(e))
    
        @app.route("/api/to_flow_rack", methods=["POST"])
        def to_flow_rack():
            try:
                frontage_id = request.json.get('frontage_id')
                part_id = request.json.get('part_id')
                self._depallet_app.fetch_part(int(frontage_id), str(part_id))
                # self._depallet_app.fetch_part(int(frontage_id), int(part_id)) # TODO➞リン: testing
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/to_kotatsu", methods=["POST"])
        def to_kotatsu():
            try:
                frontage_id = request.json.get('frontage_id')
                part_id = request.json.get('part_id')
                self._depallet_app.return_part(int(frontage_id), str(part_id))
                # self._depallet_app.return_part(int(frontage_id), int(part_id)) # TODO➞リン: modified
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/return_kotatsu", methods=["POST"])
        def return_kotatsu():
            try:
               frontage = request.json.get('frontage_id')
               loop = asyncio.new_event_loop()
               asyncio.set_event_loop(loop)
               loop.run_in_executor(
                   None, self._depallet_app.return_kotatsu, int(frontage))
             
               return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/api/complete", methods=["POST"])
        def complete():
            try:
               loop = asyncio.new_event_loop()
               asyncio.set_event_loop(loop)
               loop.run_in_executor(None, self._depallet_app.complete)
               return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))
                            
        @app.route("/api/get_depallet_area_by_plat", methods=["POST"]) # TODO➞リン: added 
        def get_depallet_area_by_plat():
            try:
                button_id = request.json.get("button_id") 
                new_depallet_area = self._depallet_app.get_depallet_area_by_plat_json(button_id)
                logging.info(f"[app.py >> get_depallet_area_by_plat() >> new_depallet_area] : {new_depallet_area}")
                return new_depallet_area
            except Exception as e:
                logging.error(f"[app.py >> get_depallet_area_by_plat() >> エラー] : {e}")
                return abort(400, str(e))
            
        @app.route('/api/update_take_count', methods=['POST'])
        def update_take_count():
            kanban_no = request.json.get('kanban_no')
            new_take_count = str(request.json.get('new_take_count'))

            try:
                with file_lock:
                    # Load config
                    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    # Check if key exists
                    if kanban_no not in config:
                        return jsonify({
                            "status": "error",
                            "message": f"Kanban No '{kanban_no}' not found in config"
                        }), 404

                    # Update value
                    config[kanban_no] = new_take_count

                    # Save back
                    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=4)

                return jsonify({"status": "success", "updated": {kanban_no: new_take_count}})
            except Exception as e:
                logging.error(f"[app.py >> update_take_count() >> エラー] : {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        
        @app.route("/api/call_AMR_return", methods=["POST"])
        def call_AMR_return():
            try:
                button_id = request.json.get('button_id') 
                self._depallet_app.call_AMR_return(button_id) 
                logging.info(f"[app.py >> call_AMR_return() >> success]")
                return jsonify({"status": "success", "message": "call AMR return successfully"})
            except Exception as e:
                logging.error(f"[app.py >> call_AMR_return() >> エラー] : {e}")
                return abort(400, str(e))
    
        file_lock = threading.Lock()

if __name__ == "__main__":
    depallet_app = None # TODO➞リン
    try:
        depallet_app = DepalletApplication()
        logging.info(f"[app.py >> DepalletApplication >> __main__] : {depallet_app}")
        depallet_app.start()
        web_server = DepalletWebServer(depallet_app)
        web_server.start(host='0.0.0.0', port=5000)
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt as e:
        logging.error(f"app.py >> Shutting down...:{e}")
    finally:
        if depallet_app:
            depallet_app.stop()

        