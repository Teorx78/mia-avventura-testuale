import os
import sys
import tkinter as tk  # Importiamo la libreria per le finestre

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "py_functions"))

try:
    from py_functions import gear
except ImportError:
    print("ERRORE: Assicurati che py_functions/gear.py esista.")
    sys.exit(1)


def main():
    # Creiamo la finestra principale del sistema operativo
    root = tk.Tk()

    # Inizializziamo il nostro motore di gioco passando la finestra
    app = gear.GameEngine(root)

    # Questo comando dice alla finestra di rimanere aperta e ascoltare i click
    root.mainloop()


if __name__ == "__main__":
    main()