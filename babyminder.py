#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime, date
import json
import os
from pathlib import Path
import random
from PIL import Image, ImageTk

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
            
    def create_rounded_button(self, parent, text, row, column, bg_color, command, font_size=48, columnspan=1):
        """Crée un bouton avec coins arrondis en utilisant Canvas"""
        # Conteneur pour le bouton
        container = tk.Frame(parent, bg='#2c3e50')
        container.grid(row=row, column=column, columnspan=columnspan, sticky='nsew', padx=10, pady=10)

        # Canvas pour dessiner le bouton arrondi
        canvas = tk.Canvas(container, bg='#2c3e50', highlightthickness=0)
        canvas.pack(expand=True, fill='both')

        # Stocker les références pour les mises à jour
        button_data = {
            'canvas': canvas,
            'text': text,
            'bg_color': bg_color,
            'font_size': font_size,
            'command': command,
            'rect_id': None,
            'text_id': None
        }

        # Dessiner le bouton après que le canvas soit configuré
        canvas.bind('<Configure>', lambda e: self.draw_rounded_button(button_data))

        # Gestion des événements de clic
        canvas.bind('<Button-1>', lambda e: command())

        return button_data

    def draw_rounded_button(self, button_data):
        """Dessine un rectangle arrondi sur le canvas"""
        canvas = button_data['canvas']
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width < 2 or height < 2:
            return

        # Nettoyer le canvas
        canvas.delete('all')

        # Rayon des coins arrondis (proportionnel à la taille)
        radius = min(40, width // 8, height // 8)

        bg_color = button_data['bg_color']

        # Ombre portée (effet de profondeur)
        shadow_offset = 6
        shadow_color = '#1a252f'
        self.create_rounded_rect(canvas, shadow_offset, shadow_offset,
                                 width - shadow_offset, height - shadow_offset,
                                 radius, fill=shadow_color, outline='')

        # Rectangle principal arrondi
        rect_id = self.create_rounded_rect(canvas, 0, 0, width - shadow_offset*2,
                                           height - shadow_offset*2, radius,
                                           fill=bg_color, outline='')

        # Reflet supérieur (effet brillant)
        highlight_color = self.lighten_color(bg_color, 0.2)
        self.create_rounded_rect(canvas, 0, 0, width - shadow_offset*2,
                                height // 3, radius, fill=highlight_color,
                                outline='', top_only=True)

        # Texte au centre
        text_id = canvas.create_text(
            (width - shadow_offset*2) // 2,
            (height - shadow_offset*2) // 2,
            text=button_data['text'],
            font=('Arial', button_data['font_size'], 'bold'),
            fill='white',
            justify='center'
        )

        button_data['rect_id'] = rect_id
        button_data['text_id'] = text_id

    def create_rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Crée un rectangle aux coins arrondis sur un canvas"""
        top_only = kwargs.pop('top_only', False)

        points = []

        # Coin supérieur gauche
        points.extend([x1 + radius, y1])

        # Coin supérieur droit
        points.extend([x2 - radius, y1])
        points.extend([x2, y1])
        points.extend([x2, y1 + radius])

        if top_only:
            # Si seulement le haut arrondi, fermer avec une ligne droite en bas
            points.extend([x2, y2])
            points.extend([x1, y2])
            points.extend([x1, y1 + radius])
        else:
            # Coin inférieur droit
            points.extend([x2, y2 - radius])
            points.extend([x2, y2])
            points.extend([x2 - radius, y2])

            # Coin inférieur gauche
            points.extend([x1 + radius, y2])
            points.extend([x1, y2])
            points.extend([x1, y2 - radius])

        # Retour au début
        points.extend([x1, y1 + radius])
        points.extend([x1, y1])

        return canvas.create_polygon(points, smooth=True, **kwargs)

    def lighten_color(self, hex_color, factor):
        """Éclaircit une couleur hexadécimale"""
        # Convertir hex en RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Éclaircir
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))

        return f'#{r:02x}{g:02x}{b:02x}'

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

        # Bouton SOINS avec effet arrondi
        self.btn_soins = self.create_rounded_button(
            main_frame,
            "SOINS",
            row=0, column=0,
            bg_color=self.get_color(self.data['soins']),
            command=lambda: self.toggle_task('soins'),
            font_size=48
        )

        # Bouton VITAMINES avec effet arrondi
        self.btn_vitamines = self.create_rounded_button(
            main_frame,
            "VITAMINES",
            row=0, column=1,
            bg_color=self.get_color(self.data['vitamines']),
            command=lambda: self.toggle_task('vitamines'),
            font_size=48
        )

        # Bouton compteur de couches avec statistiques
        couches_text = f"COUCHE +1\n\nAujourd'hui: {self.data['couches_jour']}\nTotal: {self.data['couches_total'] + self.data['couches_jour']}"
        self.btn_couches = self.create_rounded_button(
            main_frame,
            couches_text,
            row=1, column=0,
            columnspan=2,
            bg_color='#3498db',
            command=self.increment_couches,
            font_size=32
        )

        # Bouton quitter (petit, en bas à droite, gardé simple et rond)
        btn_quit_container = tk.Frame(self.root, bg='#2c3e50')
        btn_quit_container.place(relx=0.98, rely=0.02, anchor='ne', width=60, height=60)

        btn_quit_canvas = tk.Canvas(btn_quit_container, bg='#2c3e50', highlightthickness=0)
        btn_quit_canvas.pack(expand=True, fill='both')

        def draw_quit_button(event=None):
            btn_quit_canvas.delete('all')
            # Cercle avec ombre
            btn_quit_canvas.create_oval(5, 5, 55, 55, fill='#1a252f', outline='')
            btn_quit_canvas.create_oval(0, 0, 50, 50, fill='#e74c3c', outline='')
            btn_quit_canvas.create_oval(0, 0, 50, 15, fill='#ec7063', outline='')
            btn_quit_canvas.create_text(25, 25, text='✕', font=('Arial', 24, 'bold'), fill='white')

        btn_quit_canvas.bind('<Configure>', draw_quit_button)
        btn_quit_canvas.bind('<Button-1>', lambda e: self.quit_app())
        draw_quit_button()
        
        # Label date (en haut à gauche)
        self.date_label = tk.Label(
            self.root,
            text=datetime.now().strftime("%d/%m/%Y"),
            font=('Arial', 18),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.date_label.place(relx=0.02, rely=0.02, anchor='nw')

        # Charger l'image poop
        self.poop_image_path = Path(__file__).parent / 'Poop Emoji.png'
        self.poop_base_image = Image.open(self.poop_image_path)

        # Toplevel transparent pour les emojis
        self.poop_window = tk.Toplevel(self.root)
        self.poop_window.withdraw()  # Cacher temporairement
        self.poop_window.overrideredirect(True)
        self.poop_window.attributes('-transparentcolor', '#2c3e50')
        self.poop_window.attributes('-topmost', True)
        self.poop_window.config(bg='#2c3e50')

        # Liste pour garder trace des labels emoji et leurs images
        self.poop_labels = []
        self.poop_images = []  # Garder références pour éviter garbage collection

        # Dessiner les emojis initiaux après que la fenêtre soit prête
        self.root.after(100, self.setup_poop_window)
        
    def setup_poop_window(self):
        """Configure la fenêtre transparente pour les emojis"""
        # Positionner la fenêtre au-dessus de la fenêtre principale
        self.root.update_idletasks()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        self.poop_window.geometry(f"{width}x{height}+{x}+{y}")
        self.poop_window.deiconify()

        # Dessiner les emojis
        self.update_poop_emojis()

    def update_poop_emojis(self):
        """Met à jour les emojis poop avec des images"""
        # Détruire tous les labels existants
        for label in self.poop_labels:
            label.destroy()
        self.poop_labels.clear()
        self.poop_images.clear()

        # Obtenir les dimensions de la fenêtre
        self.root.update_idletasks()
        width = self.poop_window.winfo_width() if self.poop_window.winfo_width() > 1 else self.root.winfo_width()
        height = self.poop_window.winfo_height() if self.poop_window.winfo_height() > 1 else self.root.winfo_height()

        # Créer un label pour chaque couche du jour
        for _ in range(self.data['couches_jour']):
            # Position aléatoire (en pourcentage)
            # Zones évitées: centre où se trouvent les boutons (0.2-0.8 horizontal, 0.2-0.8 vertical)
            # Privilégier les coins et bords
            if random.random() < 0.5:
                # Coins gauche ou droit
                x = random.uniform(0.02, 0.15) if random.random() < 0.5 else random.uniform(0.85, 0.98)
                y = random.uniform(0.1, 0.9)
            else:
                # Bords haut ou bas
                x = random.uniform(0.15, 0.85)
                y = random.uniform(0.02, 0.12) if random.random() < 0.5 else random.uniform(0.88, 0.98)

            # Taille aléatoire (40-70 pixels - plus petit pour être moins intrusif)
            size = random.randint(40, 70)

            # Angle aléatoire (-30 à +30 degrés)
            angle = random.randint(-30, 30)

            # Redimensionner et faire pivoter l'image
            resized = self.poop_base_image.resize((size, size), Image.Resampling.LANCZOS)
            rotated = resized.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)

            # Convertir pour tkinter
            photo = ImageTk.PhotoImage(rotated)
            self.poop_images.append(photo)  # Garder référence

            # Créer le label avec l'image dans la fenêtre transparente
            label = tk.Label(
                self.poop_window,
                image=photo,
                bg='#2c3e50',
                borderwidth=0,
                highlightthickness=0
            )
            label.place(relx=x, rely=y, anchor='center')

            self.poop_labels.append(label)

    def get_color(self, status, active=False):
        """Retourne la couleur selon le statut"""
        if status:
            return '#27ae60' if not active else '#229954'  # Vert
        else:
            return '#e74c3c' if not active else '#c0392b'  # Rouge

    def flash_button(self, button_data, flash_color, final_color, duration=150):
        """Anime un bouton avec un flash visuel pour feedback tactile"""
        original_color = button_data['bg_color']
        button_data['bg_color'] = flash_color
        self.draw_rounded_button(button_data)

        def restore_color():
            button_data['bg_color'] = final_color
            self.draw_rounded_button(button_data)

        self.root.after(duration, restore_color)

    def toggle_task(self, task):
        """Bascule l'état d'une tâche"""
        # Feedback visuel immédiat
        button_data = self.btn_soins if task == 'soins' else self.btn_vitamines
        flash_color = '#ffffff' if self.data[task] else '#95a5a6'
        self.flash_button(button_data, flash_color, self.get_color(not self.data[task]))

        self.data[task] = not self.data[task]
        self.save_data()
            
    def increment_couches(self):
        """Incrémente le compteur de couches"""
        # Feedback visuel immédiat avec flash blanc
        self.flash_button(self.btn_couches, '#5dade2', '#3498db')

        self.data['couches_jour'] += 1
        self.save_data()

        # Mettre à jour le texte du bouton
        couches_text = f"COUCHE +1\n\nAujourd'hui: {self.data['couches_jour']}\nTotal: {self.data['couches_total'] + self.data['couches_jour']}"
        self.btn_couches['text'] = couches_text
        self.draw_rounded_button(self.btn_couches)

        # Mettre à jour les emojis poop
        self.update_poop_emojis()
        
    def check_midnight(self):
        """Vérifie périodiquement si on passe à minuit"""
        self.check_new_day()

        # Si on a changé de jour, mettre à jour l'interface
        if self.data['date'] == str(date.today()):
            # Mettre à jour les couleurs des boutons
            self.btn_soins['bg_color'] = self.get_color(self.data['soins'])
            self.draw_rounded_button(self.btn_soins)

            self.btn_vitamines['bg_color'] = self.get_color(self.data['vitamines'])
            self.draw_rounded_button(self.btn_vitamines)

            # Mettre à jour le texte du bouton couches
            couches_text = f"COUCHE +1\n\nAujourd'hui: {self.data['couches_jour']}\nTotal: {self.data['couches_total'] + self.data['couches_jour']}"
            self.btn_couches['text'] = couches_text
            self.draw_rounded_button(self.btn_couches)

            # Mettre à jour la date affichée
            self.date_label.config(text=datetime.now().strftime("%d/%m/%Y"))

            # Mettre à jour les emojis poop (sera vide si nouveau jour)
            self.update_poop_emojis()

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