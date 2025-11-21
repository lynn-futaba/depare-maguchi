import time
import threading
import asyncio

from flask import Flask, render_template, request, jsonify, abort, flash

from application.depallet_app import DepalletApplication


class DepalletWebServer:
    def __init__(self,depallet_app):
        self._depallet_app =depallet_app
        self.app = Flask(__name__)
        self.setup_routes()
        self.server_thread = None
        self.app.secret_key = 'secret_key'

    def start(self, host='0.0.0.0', port=5000):
          
            if self.server_thread is not None and self.server_thread.is_alive():
                print("Web server is already running")
                return self
        
            def run_server():
                self.app.run(host=host, port=port, debug=False, threaded=True, use_reloader=False)
        
            self.server_thread = threading.Thread(target=run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            print(f"Web server started at http://{host}:{port}")
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

        @app.route("/header")
        def header():
            return render_template('depallet/header.html')

        @app.route("/maguchi")
        def maguchi_page():
            return render_template('depallet/maguchi.html')

        @app.route("/flow_rack")
        def flow_rack_page():
            return render_template('depallet/flowrack.html') 

        @app.route("/depallet", methods=["GET"])
        def depallet():
            try:
                return render_template(['./depallet/depallet.html'])
            except Exception as e:
                return abort(400, 'Invalid request')

        @app.route("/update_product_info",methods=["GET"])
        def update_product_info():
            try:
                self._depallet_app.update_line_data()
                l,  r =self._depallet_app.get_product_infos_json()
                line_area_json =self._depallet_app.get_lines_json()
                return jsonify([l,r,line_area_json])
            except Exception as e:
                return str(e), 500

        @app.route("/line_frontage_click", methods=["POST"])
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

        @app.route("/update_depallet_area")
        def update_depallet_area():
            try:
                depallet_area =self._depallet_app.get_depallet_area_json()
                return jsonify(depallet_area)
            except Exception as e:
                return abort(400, str(e))

        @app.route("/update_flow_rack")
        def update_flow_rack():
            try:
               flow_rack =self._depallet_app.get_flow_rack_json()
               return jsonify(flow_rack)
            except Exception as e:
                return abort(400, str(e))
    
        @app.route("/to_flow_rack", methods=["POST"])
        def to_flow_rack():
            try:
                frontage_id = request.json.get('frontage_id')
                part_id = request.json.get('part_id')
                # print(f"[to_flow_rack >> frontage_id] : {frontage_id}")
                # print(f"[to_flow_rack >> part_id] : {part_id}")
                self._depallet_app.fetch_part(int(frontage_id), str(part_id))
                # self._depallet_app.fetch_part(int(frontage_id), int(part_id)) # TODO: testing
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/to_kotatsu", methods=["POST"])
        def to_kotatsu():
            try:
                frontage_id = request.json.get('frontage_id')
                part_id = request.json.get('part_id')
                # print(f"[to_kotatsu >> frontage_id] : {frontage_id}")
                # print(f"[to_kotatsu >> part_id] : {part_id}")
                self._depallet_app.return_part(int(frontage_id), str(part_id))
                # self._depallet_app.return_part(int(frontage_id), int(part_id)) # TODO: modified
                return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))

        @app.route("/return_kotatsu", methods=["POST"])
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

        @app.route("/complete", methods=["POST"])
        def complate():
            try:
               loop = asyncio.new_event_loop()
               asyncio.set_event_loop(loop)
               loop.run_in_executor(None, self._depallet_app.complate)
               return jsonify({"status": "success"})
            except Exception as e:
                return abort(400, str(e))
                            
        @app.route("/to_maguchi_signal_input", methods=["POST"])
        def to_maguchi_signal_input():
            try:
                line_frontage_id = request.json.get('line_frontage_id')
                print(f"[to_maguchi_signal_input >> line_frontage_id] : {line_frontage_id}")
                self._depallet_app.update_maguchi_signal_input(line_frontage_id)
                return jsonify({"status": "success"})
            except Exception as e:
                print(f"[to_maguchi_signal_input >> error] : {e}")
                return abort(400, str(e))
            
        
        @app.route("/to_maguchi_set_values", methods=["POST"])
        def to_maguchi_set_values():
            try:
                line_frontage_id = request.json.get('line_frontage_id')
                print(f"[to_maguchi_set_values >> line_frontage_id] : {line_frontage_id}")
                self._depallet_app.to_maguchi_set_values(line_frontage_id)
                return jsonify({"status": "success"})
            except Exception as e:
                print(f"[to_maguchi_set_values >> error] : {e}")
                return abort(400, str(e))


if __name__ == "__main__":
    depallet_app = None # TODO
    try:
        depallet_app= DepalletApplication()
        print(depallet_app)
        depallet_app.start()
        web_server = DepalletWebServer(depallet_app)
        web_server.start(host='0.0.0.0', port=5000)
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt as e:
        print(f"Shutting down...:{e}")
    finally:
        if depallet_app:
            depallet_app.stop()

        