from pynput import mouse

# plik do zapisu pozycji
filename = "test.txt"

def on_click(x, y, button, pressed):
    if pressed:  # tylko przy naciśnięciu przycisku
        print(f"Kliknięcie wykryte: x={x}, y={y}")
        with open(filename, "a") as f:
            f.write(f"{x},{y}\n")

# nasłuchiwanie myszy
with mouse.Listener(on_click=on_click) as listener:
    print("Nasłuchiwanie kliknięć myszy. Zapisuje do test.txt")
    listener.join()
