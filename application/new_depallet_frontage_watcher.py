from time import sleep
import logging
import threading

from domain.models.depallet import DepalletFrontage
from domain.services.depallet_service import DepalletService
from common.setup_logger import setup_log  # ログ用
from config.config import BACKUP_DAYS  # ログ用

# ログ出力開始
LOG_FOLDER = "../log"
LOG_FILE = "debug_logging.log"
setup_log(LOG_FOLDER, LOG_FILE, BACKUP_DAYS)


class NewDepalletFrontegeWatcher():

    def __init__(self, depallet_frontage: DepalletFrontage, service:DepalletService, callback = None):

        self.new_frontage = depallet_frontage
        self.depallet_service =  service
        self.interval = 1.0  # ポーリング間隔（秒）
        self.callback = callback
        self._stop_event = threading.Event()
        self._last_value = False

    def _poll(self):
        while not self._stop_event.is_set():
            try:
                current_value = self.depallet_service.is_frontage_ready(self.frontage)

                if current_value != self._last_value:
                    # self.depallet_service.set_kotatsu(self.frontage)
                    self._last_value = current_value
                    #  print(f"[Watcher] _last_value: {self._last_value}") # TODO➞リン: added print
                    logging.info(f"DepalletFrontegeWatcher >> _poll() >> self._last_value] : {self._last_value}")
            except Exception as e:
                logging.error(f"[DepalletFrontegeWatcher >> _poll() >> Watcher エラー] : {e}")
            sleep(self.interval)

    def start(self):
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()

    def stop(self):
        logging.info("[DepalletFrontegeWatcher >> stop() >> Watcher] Stopping watcher...")
        self._stop_event.set()
        self._thread.join()


class NewWatcherManager:
    def __init__(self):
        self.watchers = []

    def add_watcher(self, watcher: NewDepalletFrontegeWatcher):
        self.watchers.append(watcher)

    def start_all(self):
        logging.info("[DepalletFrontegeWatcher >> start_all() >> Manager] Starting all watchers...")
        for w in self.watchers:
            w.start()

    def stop_all(self):
        logging.info("[DepalletFrontegeWatcher >> start_all() >> Manager] Stopping all watchers...")
        for w in self.watchers:
            w.stop()


if __name__ == "__main__":

    from infrastructure.mysql.mysql_db import MysqlDb
    from infrastructure.mysql.depallet_area_repository import DepalletAreaRepository
    from infrastructure.mysql.wcs_controler import WcsControler
    db = MysqlDb()
    repo = DepalletAreaRepository(db)
    w_repo = WcsControler(db)
    area = repo.get_depallet_area_by_plat([20, 21, 22, 23, 24, 25, 26, 27, 28, 29])  
    f = area.get_by_id(1)
    service = DepalletService(repo, w_repo)
    w = NewDepalletFrontegeWatcher(f, service)
    w.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        w.stop()
        logging.info("[DepalletFrontegeWatcher >> __main__ >> Stopped by user]")