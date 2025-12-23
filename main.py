import threading 
import queue
import traceback
import time
from functools import partial
from Program.LogicOfProgram.SettingsUI import SettingsUI
# from Program.LogicOfProgram.InGameUI import InGameUI, mode_selected, mode_event
from Program.LogicOfProgram.InGameUI import InGameUI
from Program.LogicOfProgram.GenerateBackendMark import GenerateBackendMark
from Program.LogicOfProgram.UsageOfYolo import UsageOfYolo
from Program.LogicOfProgram.CalculatePxPerMapSquare import CalculatePxPerMapSquare
from Program.LogicOfProgram.ManageYoloResponse import ManageYoloResponse
from Program.LogicOfProgram.PathToPrograms import (
    settings_path,
    prediction_raw_path
)
from Program.LogicOfProgram.logger import setup_logger
from Program.LogicOfProgram.Development import development

logger = setup_logger(__name__)

current_resolution = None

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
    logger.debug(f"thread error: ")


# funckja dla callback
def when_capture_ready(number):
    """executed after callback from yolo detection (function callback)"""
    task_queue.put(UsageOfYolo)
    task_queue.put(lambda: CalculatePxPerMapSquare(current_resolution))
    task_queue.put(ManageYoloResponse)

def main():
    global current_resolution

    if(development==1):
        print("IMPORTANT !!! go to file Program/LogicOfProgram/development.py and set everything to 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.debug(f"go to file Program/LogicOfProgram/Development.py and set everything to 0 if you dont debugging")

    threading.excepthook = handle_thread_exception
    
    threading.Thread(target=worker, daemon=True, name="TaskQueueWorker").start()

    # 📏 Ustawienia rozdzielczości
    res = SettingsUI()
    if not res or res == "error":
        print("resolution not selected or error.")
        logger.debug(f"resolution not selected or error.")
        return
    current_resolution = res
    print(f"setted resolution: {res}")

    # 🎮 Uruchamiamy InGameUI (oddzielny wątek, działa do ESC/krzyżyka)
    InGameUI_thread = threading.Thread(target=InGameUI, name="InGameUIThread")
    InGameUI_thread.start()

    # mode=mode_event.wait()

    # ⚙️ Uruchamiamy backend (YOLO + callback)
    print("[DEBUG] start backend_thread...execute callback when_capture_ready")
    backend_thread = threading.Thread(
        target=GenerateBackendMark,
        args=(settings_path, prediction_raw_path, when_capture_ready),
        daemon=True,
        name="GenerateMark"
    )
    backend_thread.start()

    print("[DEBUG] all threads are active. Program works in parallel.")

    # czekamy aż użytkownik zamknie InGameUI
    InGameUI_thread.join()
    print("[INFO] InGameUI closed — closing program.")

    task_queue.put(None)
    time.sleep(0.1)
    task_queue.join()

if __name__ == "__main__":
    main()
