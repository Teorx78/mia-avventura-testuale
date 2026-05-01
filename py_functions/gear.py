import json
import os
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(folder_name, file_name):
    """Carica un file JSON e restituisce un dizionario."""
    file_path = os.path.join(BASE_DIR, folder_name, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Errore caricamento {file_name}: {e}")
        return None


class GameEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("La mia Avventura Testuale")
        self.root.geometry("650x500")  # Larghezza x Altezza della finestra

        # 1. Caricamento Dati
        self.game_state = load_json("stats", "player_stats.json") or {"reputation": 0, "morale": 100}
        self.scenes_db = load_json("scenes", "story.json")

        if not self.scenes_db:
            messagebox.showerror("Errore Critico", "File delle scene non trovato o non valido.")
            self.root.destroy()
            return

        # 2. Setup dell'Interfaccia Grafica (UI)
        # Etichetta in alto per le statistiche
        self.stats_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.stats_label.pack(pady=10)

        # Area di testo centrale per la storia
        self.story_text = tk.Text(root, height=12, width=60, font=("Comfortaa", 14), wrap=tk.WORD, bg="#f4f4f4")
        self.story_text.pack(pady=10, padx=20)

        # Contenitore per i pulsanti delle scelte in basso
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        # 3. Avvio della prima scena
        self.load_scene("castle_exterior")

    def load_scene(self, scene_id):
        """Carica a schermo i testi e i bottoni di una specifica scena."""
        scene = self.scenes_db.get(scene_id)
        if not scene:
            self.story_text.insert(tk.END, f"\n[ERRORE: Scena '{scene_id}' mancante!]")
            return

        # Aggiorniamo la barra delle statistiche
        stats_str = f"Reputazione: {self.game_state.get('reputation', 0)}  |  Morale: {self.game_state.get('morale', 100)}"
        self.stats_label.config(text=stats_str)

        # Aggiorniamo il testo della storia
        self.story_text.config(state=tk.NORMAL)  # Sblocchiamo l'area di testo
        self.story_text.delete(1.0, tk.END)  # Cancelliamo il testo della scena precedente
        self.story_text.insert(tk.END, scene.get("text", ""))  # Inseriamo il nuovo testo
        self.story_text.config(state=tk.DISABLED)  # Blocchiamo l'area di testo (sola lettura)

        # Distruggiamo i vecchi bottoni
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Creiamo i nuovi bottoni basati sulle scelte
        choices = scene.get("choices", [])

        if not choices:
            # Se l'array choices è vuoto, il gioco è finito
            btn = tk.Button(self.buttons_frame, text="Esci dal gioco", font=("Helvetica", 11), width=40,
                            command=self.root.destroy)
            btn.pack(pady=5)
        else:
            for choice in choices:
                # Creiamo un bottone per ogni scelta.
                # Nota: usiamo lambda per "congelare" i dati della scelta e passarli alla funzione solo al click
                btn = tk.Button(
                    self.buttons_frame,
                    text=choice.get("text", ""),
                    font=("Helvetica", 11),
                    width=40,
                    command=lambda c=choice: self.make_choice(c)
                )
                btn.pack(pady=5)

    def make_choice(self, choice_data):
        """Viene chiamata quando il giocatore clicca un bottone."""
        # Applichiamo gli effetti alle statistiche
        effects = choice_data.get("effects", {})
        for stat, value in effects.items():
            if stat in self.game_state:
                self.game_state[stat] += value
            else:
                self.game_state[stat] = value

        # Leggiamo l'ID della prossima scena e la carichiamo
        next_scene_id = choice_data.get("next_scene")
        self.load_scene(next_scene_id)