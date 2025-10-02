#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime, date
import json
import os
from pathlib import Path

class BabyTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Baby Tracker")
        
        # Configuration pour plein écran
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#2c3e50')
        
        # Chemin du fichier de sauvegarde
        self.data_file = Path.home() / '.babytracker.json'
        
        # Charger les données
        self.load_data()
        
        # Vérifier si on doit réinitialiser (nouveau jour)
        self.check_new_day()
        
        # Créer l'interface
        self.create_ui()
        
        # Vérifier périodiquement pour le changement de jour
        self.check_midnight()
        
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        default_data = {
            'date': str(date.today()),
            'soins': False,
            'vitamines': False,
            'couches_jour': 0,
            'couches_total': 0
        }
        
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = default_data
        else:
            self.data = default_data
            
    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)
            
    def check_new_day(self):
        """Vérifie si c'est un nouveau jour et réinitialise si nécessaire"""
        today = str(date.today())
        if self.data['date'] != today:
            # Sauvegarder le nombre de couches du jour dans le total
            self.data['couches_total'] += self.data['couches_jour']
            # Réinitialiser pour le nouveau jour
            self.data['date'] = today
            self.data['soins'] = False
            self.data['vitamines'] = False
            self.data['couches_jour'] = 0
            self.save_data()
            
    def create_ui(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Configuration des colonnes et lignes
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=2)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Bouton SOINS
        self.btn_soins = tk.Button(
            main_frame,
            text="SOINS",
            font=('Arial', 48, 'bold'),
            fg='white',
            bg=self.get_color(self.data['soins']),
            activebackground=self.get_color(self.data['soins'], True),
            relief='flat',
            bd=0,
            command=lambda: self.toggle_task('soins')
        )
        self.btn_soins.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # Bouton VITAMINES
        self.btn_vitamines = tk.Button(
            main_frame,
            text="VITAMINES",
            font=('Arial', 48, 'bold'),
            fg='white',
            bg=self.get_color(self.data['vitamines']),
            activebackground=self.get_color(self.data['vitamines'], True),
            relief='flat',
            bd=0,
            command=lambda: self.toggle_task('vitamines')
        )
        self.btn_vitamines.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        
        # Bouton compteur de couches avec statistiques
        couches_text = f"COUCHE +1\n\nAujourd'hui: {self.data['couches_jour']}\nTotal: {self.data['couches_total'] + self.data['couches_jour']}"
        self.btn_couches = tk.Button(
            main_frame,
            text=couches_text,
            font=('Arial', 32, 'bold'),
            fg='white',
            bg='#3498db',
            activebackground='#2980b9',
            relief='flat',
            bd=0,
            command=self.increment_couches,
            justify='center'
        )
        self.btn_couches.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        
        # Bouton quitter (petit, en bas à droite)
        btn_quit = tk.Button(
            self.root,
            text="✕",
            font=('Arial', 20),
            fg='white',
            bg='#e74c3c',
            activebackground='#c0392b',
            relief='flat',
            bd=0,
            command=self.quit_app,
            width=3,
            height=1
        )
        btn_quit.place(relx=0.98, rely=0.02, anchor='ne')
        
        # Label date (en haut à gauche)
        self.date_label = tk.Label(
            self.root,
            text=datetime.now().strftime("%d/%m/%Y"),
            font=('Arial', 18),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.date_label.place(relx=0.02, rely=0.02, anchor='nw')
        
    def get_color(self, status, active=False):
        """Retourne la couleur selon le statut"""
        if status:
            return '#27ae60' if not active else '#229954'  # Vert
        else:
            return '#e74c3c' if not active else '#c0392b'  # Rouge

    def flash_button(self, button, flash_color, original_color, duration=150):
        """Anime un bouton avec un flash visuel pour feedback tactile"""
        button.config(bg=flash_color, relief='sunken')
        self.root.after(duration, lambda: button.config(bg=original_color, relief='flat'))

    def toggle_task(self, task):
        """Bascule l'état d'une tâche"""
        # Feedback visuel immédiat
        button = self.btn_soins if task == 'soins' else self.btn_vitamines
        current_color = self.get_color(self.data[task])
        flash_color = '#ffffff' if self.data[task] else '#95a5a6'
        self.flash_button(button, flash_color, self.get_color(not self.data[task]))

        self.data[task] = not self.data[task]
        self.save_data()

        # Mettre à jour la couleur du bouton
        if task == 'soins':
            self.btn_soins.config(
                activebackground=self.get_color(self.data[task], True)
            )
        else:
            self.btn_vitamines.config(
                activebackground=self.get_color(self.data[task], True)
            )
            
    def increment_couches(self):
        """Incrémente le compteur de couches"""
        # Feedback visuel immédiat avec flash blanc
        self.flash_button(self.btn_couches, '#5dade2', '#3498db')

        self.data['couches_jour'] += 1
        self.save_data()

        # Mettre à jour le texte du bouton
        couches_text = f"COUCHE +1\n\nAujourd'hui: {self.data['couches_jour']}\nTotal: {self.data['couches_total'] + self.data['couches_jour']}"
        self.btn_couches.config(text=couches_text)
        
    def check_midnight(self):
        """Vérifie périodiquement si on passe à minuit"""
        self.check_new_day()
        
        # Si on a changé de jour, mettre à jour l'interface
        if self.data['date'] == str(date.today()):
            # Mettre à jour les couleurs des boutons
            self.btn_soins.config(
                bg=self.get_color(self.data['soins']),
                activebackground=self.get_color(self.data['soins'], True)
            )
            self.btn_vitamines.config(
                bg=self.get_color(self.data['vitamines']),
                activebackground=self.get_color(self.data['vitamines'], True)
            )
            # Mettre à jour le texte du bouton couches
            couches_text = f"COUCHE +1\n\nAujourd'hui: {self.data['couches_jour']}\nTotal: {self.data['couches_total'] + self.data['couches_jour']}"
            self.btn_couches.config(text=couches_text)
            
            # Mettre à jour la date affichée
            self.date_label.config(text=datetime.now().strftime("%d/%m/%Y"))
        
        # Vérifier à nouveau dans 60 secondes
        self.root.after(60000, self.check_midnight)
        
    def quit_app(self):
        """Quitte l'application"""
        self.save_data()
        self.root.quit()
        
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BabyTracker()
    app.run()