from time import sleep
import threading

from domain.models.depallet import DepalletFrontage
from domain.services.depallet_service import DepalletService


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
                    #  print(f"[Watcher] _last_value: {self._last_value}") # TODO: added print
            except Exception as e:
                print(f"[Watcher] Error: {e}")
            sleep(self.interval)

    def start(self):
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()

    def stop(self):
        print(f"[Watcher] Stopping watcher...")
        self._stop_event.set()
        self._thread.join()


class NewWatcherManager:
    def __init__(self):
        self.watchers = []

    def add_watcher(self, watcher: NewDepalletFrontegeWatcher):
        self.watchers.append(watcher)

    def start_all(self):
        print("[Manager] Starting all watchers...")
        for w in self.watchers:
            w.start()

    def stop_all(self):
        print("[Manager] Stopping all watchers...")
        for w in self.watchers:
            w.stop()


if __name__ == "__main__":

    from infrastructure.mysql.mysql_db import MysqlDb
    from infrastructure.mysql.depallet_area_repository import DepalletAreaRepository
    from infrastructure.mysql.wcs_controler import WcsControler
    db = MysqlDb()
    repo = DepalletAreaRepository(db)
    w_repo = WcsControler(db)
    area = repo.get_depallet_area_by_plat([1,2,3,4])  
    f = area.get_by_id(1)
    service = DepalletService(repo, w_repo)
    w = NewDepalletFrontegeWatcher(f, service)
    w.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        w.stop()
        print("Stopped by user")