import threading
from Program.LogicOfProgram.SettingsUI import SettingsUI
from Program.LogicOfProgram.InGameUI import InGameUI
from Program.LogicOfProgram.GenerateBackendMark import GenerateBackendMark
from Program.LogicOfProgram.UsageOfYolo import UsageOfYolo
from Program.LogicOfProgram.CalculateMetersPerPX import CalculateMetersPerPX
from Program.LogicOfProgram.ManageYoloResponse import ManageYoloResponse
from Program.LogicOfProgram.PathToPrograms import settings_path, prediction_raw_path

# 🌐 Zmienne globalne
overlay = None
app = None
current_resolution = None

# 🔐 Flaga i blokada do wątku meters
meter_thread_running = False
meter_lock = threading.Lock()

def when_capture_ready(number):
    """Wywoływane po wykonaniu detekcji YOLO"""
    global meter_thread_running

    print(f"[YOLO] Uruchamiam detekcję dla {number}")
    UsageOfYolo()

    # 🔒 Tylko jeden wątek CalculateMetersPerPX + ManageYoloResponse na raz
    with meter_lock:
        if meter_thread_running:
            print("[DEBUG] Wątek meters już działa — pomijam uruchomienie nowego.")
            return
        meter_thread_running = True

    def meter_thread_func():
        global meter_thread_running
        try:
            print("[DEBUG] Uruchamiam CalculateMetersPerPX w osobnym wątku.")
            CalculateMetersPerPX(current_resolution)
            print("[DEBUG] Uruchamiam ManageYoloResponse po CalculateMetersPerPX.")
            ManageYoloResponse()
        except Exception as e:
            print(f"[ERROR] Błąd w wątku obliczania metrów: {e}")
        finally:
            # 🔄 Reset flagi po zakończeniu wątku
            with meter_lock:
                meter_thread_running = False

    meter_thread = threading.Thread(target=meter_thread_func, daemon=True)
    meter_thread.start()


def main():
    global overlay, app, current_resolution

    # 📏 Ustawienia rozdzielczości
    res = SettingsUI()
    if not res or res == "error":
        print("Nie wybrano rozdzielczości lub błąd.")
        return
    current_resolution = res
    print(f"Ustawiono rozdzielczość: {res}")

    # 🎮 Uruchamiamy InGameUI (oddzielny wątek, działa do ESC/krzyżyka)
    InGameUI_thread = threading.Thread(target=InGameUI)
    InGameUI_thread.start()

    # ⚙️ Uruchamiamy backend (YOLO + callback)
    print("[DEBUG] Uruchamiam backend_thread...")
    backend_thread = threading.Thread(
        target=GenerateBackendMark,
        args=(settings_path, prediction_raw_path, when_capture_ready),
        daemon=True
    )
    backend_thread.start()

    print("[DEBUG] Wszystkie wątki uruchomione. Program działa równolegle.")

    # czekamy aż użytkownik zamknie InGameUI
    InGameUI_thread.join()
    print("[INFO] InGameUI zakończone — kończę program.")


if __name__ == "__main__":
    main()
