import threading 
import queue
import traceback
import time
from functools import partial
from Program.LogicOfProgram.SettingsUI import SettingsUI
from Program.LogicOfProgram.InGameUI import InGameUI
from Program.LogicOfProgram.GenerateBackendMark import GenerateBackendMark
from Program.LogicOfProgram.UsageOfYolo import UsageOfYolo
from Program.LogicOfProgram.CalculatePxPerMapSquare import CalculatePxPerMapSquare
from Program.LogicOfProgram.ManageYoloResponse import ManageYoloResponse
from Program.LogicOfProgram.PathToPrograms import settings_path, prediction_raw_path

# 🌐 Zmienne globalne
overlay = None
app = None
current_resolution = None

# 🔐 Flaga i blokada do wątku meters
meter_thread_running = False
meter_lock = threading.Lock()

task_queue = queue.Queue()

def worker():
    """Worker to handle queue."""
    while True:
        task = task_queue.get()
        if task is None:  # sygnał zakończenia
            task_queue.task_done()
            print("[WORKER] stopped worker thread.")
            break
        try:
            result = task()
            if result is not None:
                print(f"[WORKER OK] result: {result}")
        except Exception as e:
            print(f"[WORKER ERR] {e}")
            traceback.print_exc()
        finally:
            task_queue.task_done()


def handle_thread_exception(args):
    print("\n--- [Error in thread] ---")

    thread_name = getattr(args.thread, "name", "unknown thread")
    print(f"thread: {thread_name}")
    print(f"type: {args.exc_type.__name__}")
    print(f"mesage: {args.exc_value}")
    print(f"is thread alive: {args.thread.is_alive() if args.thread else 'none data'}")

    print("thread stack")
    traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback)

    # Lista aktywnych wątków
    enumeration = threading.enumerate()
    print(f"active thread ({len(enumeration)}):")
    for i in enumeration:
        print(f"  - {i.name} (alive={i.is_alive()})")

    # Rozmiar stosu (globalny, nie dla konkretnego wątku)
    size = threading.stack_size()
    print(f"default size of thread stack: {size if size != 0 else 'system default'}")

    print("--- end thread exception ---\n")

# funckja dla callback
def when_capture_ready(number):
    """executed after callback from yolo detection (function callback)"""
    global meter_thread_running

    print(f"[YOLO] start detection {number}")

    # 🔒 Tylko jeden wątek CalculateMetersPerPX + ManageYoloResponse na raz
    with meter_lock:
        if meter_thread_running:
            print("[DEBUG] thread meters is alive already.")
            return
        meter_thread_running = True

    def meter_thread_func():
        global meter_thread_running
        try:
            print("meter_thread_func task queue start")
            print("[DEBUG] start CalculateMetersPerPX in different thread.")
            task_queue.put(UsageOfYolo())
            task_queue.put(lambda: CalculatePxPerMapSquare(current_resolution))
            task_queue.put(ManageYoloResponse)
            print("meter_thread_func task queue end")
            task_queue.join()

        except Exception as e:
            print(f"[ERROR] error in thread calculate meters: {e}")
            traceback.print_exc()
        finally:
            # 🔄 Reset flagi po zakończeniu wątku
            with meter_lock:
                meter_thread_running = False

    meter_thread=threading.Thread(target=meter_thread_func, daemon=True, name="MeterWorker")
    meter_thread.start()



def main():
    global overlay, app, current_resolution

    threading.excepthook = handle_thread_exception
    
    threading.Thread(target=worker, daemon=True, name="TaskQueueWorker").start()

    # 📏 Ustawienia rozdzielczości
    res = SettingsUI()
    if not res or res == "error":
        print("resolution not selected or error.")
        return
    current_resolution = res
    print(f"setted resolution: {res}")

    # 🎮 Uruchamiamy InGameUI (oddzielny wątek, działa do ESC/krzyżyka)
    InGameUI_thread = threading.Thread(target=InGameUI, name="InGameUIThread")
    InGameUI_thread.start()

    # ⚙️ Uruchamiamy backend (YOLO + callback)
    print("[DEBUG] start backend_thread...execute callback when_capture_ready")
    backend_thread = threading.Thread(
        target=GenerateBackendMark,
        args=(settings_path, prediction_raw_path, when_capture_ready),
        daemon=True,
        name="GenerateMark"
    )
    backend_thread.start()


    # Pętla główna obsługi zadań
    # while not stop_threads:
    #     try:
    #         task = task_queue.get(timeout=0.5)
    #         # jeśli chcesz, możesz tu od razu wykonać task:
    #         if task is not None:
    #             task()
    #         task_queue.task_done()
    #     except queue.Empty:
    #         continue


    print("[DEBUG] all threads are active. Program works in parallel.")

    # czekamy aż użytkownik zamknie InGameUI
    InGameUI_thread.join()
    print("[INFO] InGameUI closed — closing program.")

    task_queue.put(None)
    time.sleep(0.1)
    task_queue.join()

if __name__ == "__main__":
    main()
