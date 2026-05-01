import os
import sys

# Assicuriamoci che Python trovi la cartella py_functions
percorso_base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(percorso_base, "py_functions"))

# Immaginiamo che dentro py_functions tu crei un file chiamato 'motore.py'
# che conterrà la logica del loop che abbiamo visto prima.
try:
    from py_functions import motore
except ImportError:
    print("ERRORE: Assicurati di aver creato la cartella 'py_functions' e il file 'motore.py' al suo interno.")
    sys.exit(1)


def main():
    print("Caricamento risorse di gioco in corso...")

    # Qui potresti chiamare una funzione che carica i JSON dalle cartelle 'scenes', 'stats', 'npcs'
    # database_scene = motore.carica_json(os.path.join(percorso_base, "scenes"))

    print("Risorse caricate. Avvio avventura...\n")
    print("*" * 40)

    # Facciamo partire il loop principale del gioco
    motore.avvia_gioco()


if __name__ == "__main__":
    main()