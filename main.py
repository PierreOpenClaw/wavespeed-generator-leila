# main_modern.py - Interface Moderne CustomTkinter pour Leila
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import json
import time
import base64
import threading
from pathlib import Path
from datetime import datetime
import os

# Configuration du thème Dark/Gothique
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ModernWaveSpeedApp:
    def __init__(self):
        # Fenêtre principale
        self.window = ctk.CTk()
        self.window.title("WaveSpeed Generator - Leila")
        self.window.geometry("1400x900")
        self.window.minsize(1200, 700)
        
        # Configuration
        self.config_file = Path("config.json")
        self.load_config()
        
        # Variables
        self.current_images = []
        self.selected_image = None
        self.generating = False
        self.thumbnail_cache = {}
        
        # Couleurs du thème Dark/Gothique
        self.colors = {
            "bg_primary": "#1a1a1a",      # Noir profond
            "bg_secondary": "#242424",     # Gris très foncé
            "bg_tertiary": "#2d2d2d",      # Gris foncé
            "accent": "#8b5cf6",           # Violet gothique
            "accent_hover": "#7c3aed",     # Violet foncé
            "text_primary": "#ffffff",     # Blanc
            "text_secondary": "#a1a1aa",   # Gris clair
            "border": "#3f3f46",           # Bordure
            "success": "#10b981",          # Vert succès
            "error": "#ef4444",            # Rouge erreur
        }
        
        self.setup_ui()
        
    def load_config(self):
        """Charge la configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "api_key": "",
                "lora_path": "",
                "output_folder": str(Path.home() / "WaveSpeed_Images")
            }
    
    def save_config(self):
        """Sauvegarde la configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        """Configure l'interface utilisateur moderne"""
        # Frame principal avec padding
        self.main_frame = ctk.CTkFrame(self.window, fg_color=self.colors["bg_primary"])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Layout en 3 colonnes : Sidebar (25%) | Preview (45%) | Gallery (30%)
        self.main_frame.grid_columnconfigure(0, weight=0, minsize=350)  # Sidebar
        self.main_frame.grid_columnconfigure(1, weight=1)               # Preview
        self.main_frame.grid_columnconfigure(2, weight=0, minsize=400)  # Gallery
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # === SIDEBAR (Gauche) ===
        self.create_sidebar()
        
        # === PREVIEW (Centre) ===
        self.create_preview_panel()
        
        # === GALLERY (Droite) ===
        self.create_gallery_panel()
        
        # === STATUS BAR (Bas) ===
        self.create_status_bar()
        
    def create_sidebar(self):
        """Crée la barre latérale avec les contrôles"""
        sidebar = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        sidebar.grid_rowconfigure(3, weight=1)
        
        # Titre
        title = ctk.CTkLabel(
            sidebar,
            text="⚡ WaveSpeed",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(
            sidebar,
            text="Generator for Leila",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(pady=(0, 20))
        
        # Section Configuration
        config_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        config_frame.pack(fill="x", padx=15, pady=10)
        
        # API Key
        ctk.CTkLabel(config_frame, text="🔑 Clé API", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        self.api_entry = ctk.CTkEntry(
            config_frame,
            placeholder_text="Votre clé API WaveSpeed",
            show="•",
            height=35,
            corner_radius=8
        )
        self.api_entry.pack(fill="x", pady=(0, 10))
        self.api_entry.insert(0, self.config.get("api_key", ""))
        
        # LoRa Path
        ctk.CTkLabel(config_frame, text="🖼️ Image LoRa", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        lora_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        lora_frame.pack(fill="x", pady=(0, 10))
        lora_frame.grid_columnconfigure(0, weight=1)
        
        self.lora_entry = ctk.CTkEntry(
            lora_frame,
            placeholder_text="Chemin vers image LoRa",
            height=35,
            corner_radius=8
        )
        self.lora_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.lora_entry.insert(0, self.config.get("lora_path", ""))
        
        ctk.CTkButton(
            lora_frame,
            text="📁",
            width=40,
            height=35,
            corner_radius=8,
            command=self.browse_lora
        ).grid(row=0, column=1)
        
        # Section Prompts
        prompts_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        prompts_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(prompts_frame, text="✏️ Prompt A (Principal)", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        self.prompt_a = ctk.CTkTextbox(
            prompts_frame,
            height=80,
            corner_radius=10,
            border_width=1,
            border_color=self.colors["border"]
        )
        self.prompt_a.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(prompts_frame, text="🎨 Prompt B (Variante)", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        self.prompt_b = ctk.CTkTextbox(
            prompts_frame,
            height=80,
            corner_radius=10,
            border_width=1,
            border_color=self.colors["border"]
        )
        self.prompt_b.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(prompts_frame, text="💬 Caption", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        self.caption = ctk.CTkTextbox(
            prompts_frame,
            height=60,
            corner_radius=10,
            border_width=1,
            border_color=self.colors["border"]
        )
        self.caption.pack(fill="x", pady=(0, 10))
        
        # Bouton Générer
        self.generate_btn = ctk.CTkButton(
            sidebar,
            text="🚀 Générer les 2 images",
            height=45,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.start_generation
        )
        self.generate_btn.pack(fill="x", padx=15, pady=20)
        
        # Info
        info = ctk.CTkLabel(
            sidebar,
            text="💡 Format: 9:16 | 2K Quality",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_secondary"]
        )
        info.pack(pady=(10, 20))
        
    def create_preview_panel(self):
        """Crée le panneau de prévisualisation centrale"""
        preview_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(preview_frame, fg_color="transparent", height=50)
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header,
            text="👁️ Prévisualisation",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        self.image_label = ctk.CTkLabel(header, text="", font=ctk.CTkFont(size=12))
        self.image_label.grid(row=0, column=1, sticky="e")
        
        # Zone d'image
        self.preview_container = ctk.CTkFrame(
            preview_frame,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=10
        )
        self.preview_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        self.preview_image = ctk.CTkLabel(
            self.preview_container,
            text="📷 Aucune image sélectionnée",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        )
        self.preview_image.pack(expand=True)
        
        # Boutons d'action
        actions = ctk.CTkFrame(preview_frame, fg_color="transparent", height=50)
        actions.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        actions.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkButton(
            actions,
            text="📂 Ouvrir dossier",
            height=35,
            corner_radius=8,
            command=self.open_output_folder
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            actions,
            text="📋 Copier prompt",
            height=35,
            corner_radius=8,
            command=self.copy_prompt
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(
            actions,
            text="🗑️ Supprimer",
            height=35,
            corner_radius=8,
            fg_color=self.colors["error"],
            hover_color="#dc2626",
            command=self.delete_selected
        ).grid(row=0, column=2, padx=5)
        
    def create_gallery_panel(self):
        """Crée le panneau de galerie à droite"""
        gallery_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )
        gallery_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        gallery_frame.grid_rowconfigure(1, weight=1)
        gallery_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(gallery_frame, fg_color="transparent", height=50)
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        ctk.CTkLabel(
            header,
            text="🖼️ Galerie",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        self.gallery_count = ctk.CTkLabel(
            header,
            text="0 images",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.gallery_count.pack(side="right")
        
        # Scrollable frame pour les thumbnails
        self.gallery_scroll = ctk.CTkScrollableFrame(
            gallery_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.gallery_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Charger les images existantes
        self.refresh_gallery()
        
    def create_status_bar(self):
        """Crée la barre de statut en bas"""
        status_frame = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["bg_secondary"],
            height=35,
            corner_radius=0
        )
        status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✅ Prêt",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_secondary"]
        )
        self.status_label.pack(side="left", padx=20)
        
        self.progress = ctk.CTkProgressBar(
            status_frame,
            width=200,
            height=6,
            corner_radius=3,
            mode="indeterminate"
        )
        self.progress.pack(side="right", padx=20)
        self.progress.stop()
        self.progress.set(0)
        
    def browse_lora(self):
        """Ouvre le dialogue pour choisir l'image LoRa"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Choisir l'image LoRa",
            filetypes=[("Images", "*.jpg *.jpeg *.png")]
        )
        if filename:
            self.lora_entry.delete(0, "end")
            self.lora_entry.insert(0, filename)
    
    def start_generation(self):
        """Démarre la génération"""
        if self.generating:
            return
        
        # Récupérer les valeurs
        api_key = self.api_entry.get().strip()
        lora_path = self.lora_entry.get().strip()
        prompt_a = self.prompt_a.get("1.0", "end").strip()
        prompt_b = self.prompt_b.get("1.0", "end").strip()
        caption = self.caption.get("1.0", "end").strip()
        
        # Vérifications
        if not api_key:
            self.show_error("Veuillez entrer votre clé API")
            return
        if not lora_path or not Path(lora_path).exists():
            self.show_error("Veuillez sélectionner une image LoRa valide")
            return
        if not prompt_a:
            self.show_error("Veuillez entrer le Prompt A")
            return
        if not prompt_b:
            self.show_error("Veuillez entrer le Prompt B")
            return
        
        # Sauvegarder config
        self.config["api_key"] = api_key
        self.config["lora_path"] = lora_path
        self.save_config()
        
        # Démarrer génération
        self.generating = True
        self.generate_btn.configure(state="disabled", text="⏳ Génération en cours...")
        self.progress.start()
        self.update_status("🎨 Génération en cours...")
        
        thread = threading.Thread(
            target=self.generate_images,
            args=(api_key, lora_path, prompt_a, prompt_b, caption)
        )
        thread.daemon = True
        thread.start()
    
    def generate_images(self, api_key, lora_path, prompt_a, prompt_b, caption):
        """Génère les images en arrière-plan"""
        try:
            # Créer dossier de sortie
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = Path(self.config.get("output_folder", Path.home() / "WaveSpeed_Images"))
            output_path = output_path / f"{timestamp}-post"
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Générer Image A
            self.update_status("🎨 Génération Image A...")
            img_a = self.generate_single_image(api_key, lora_path, prompt_a)
            
            if img_a:
                img_a_path = output_path / "A.jpg"
                with open(img_a_path, 'wb') as f:
                    f.write(img_a)
                self.update_status(f"✅ Image A générée")
                
                # Générer Image B
                self.update_status("🎨 Génération Image B (variante)...")
                img_b = self.generate_variant(api_key, img_a, prompt_b)
                
                if img_b:
                    img_b_path = output_path / "B.jpg"
                    with open(img_b_path, 'wb') as f:
                        f.write(img_b)
                    self.update_status(f"✅ Image B générée")
                    
                    # Sauvegarder caption et prompts
                    if caption:
                        with open(output_path / "caption.txt", 'w', encoding='utf-8') as f:
                            f.write(caption)
                    
                    with open(output_path / "prompts.txt", 'w', encoding='utf-8') as f:
                        f.write(f"PROMPT A:\n{prompt_a}\n\nPROMPT B:\n{prompt_b}")
                    
                    self.update_status(f"🎉 Post créé dans: {output_path}")
                    self.window.after(0, self.refresh_gallery)
                    self.window.after(0, lambda: self.show_success(f"Images générées!\nDossier: {output_path}"))
                else:
                    self.update_status("⚠️ Image B échouée")
            else:
                self.update_status("❌ Image A échouée")
                
        except Exception as e:
            self.update_status(f"❌ Erreur: {str(e)}")
            self.window.after(0, lambda: self.show_error(str(e)))
        finally:
            self.generating = False
            self.window.after(0, self.reset_ui)
    
    def generate_single_image(self, api_key, lora_path, prompt):
        """Génère une image unique"""
        with open(lora_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        data = {
            "prompt": prompt,
            "images": [f"data:image/jpeg;base64,{img_b64}"],
            "aspect_ratio": "9:16",
            "resolution": "2k",
            "output_format": "jpeg"
        }
        
        response = requests.post(
            "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit",
            json=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        
        result = response.json()
        task_url = result['data']['urls']['get']
        
        # Attendre résultat
        for attempt in range(60):
            time.sleep(2)
            poll = requests.get(task_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30).json()
            
            if poll['data']['status'] == 'completed' and poll['data']['outputs']:
                img_url = poll['data']['outputs'][0]
                return requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60).content
            elif poll['data']['status'] == 'failed':
                raise Exception("Génération échouée")
        
        raise Exception("Timeout")
    
    def generate_variant(self, api_key, base_image, prompt):
        """Génère une variante img2img"""
        img_b64 = base64.b64encode(base_image).decode('utf-8')
        
        data = {
            "prompt": prompt,
            "images": [f"data:image/jpeg;base64,{img_b64}"],
            "aspect_ratio": "9:16",
            "resolution": "2k",
            "output_format": "jpeg"
        }
        
        response = requests.post(
            "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit",
            json=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        
        result = response.json()
        task_url = result['data']['urls']['get']
        
        for attempt in range(60):
            time.sleep(2)
            poll = requests.get(task_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30).json()
            
            if poll['data']['status'] == 'completed' and poll['data']['outputs']:
                img_url = poll['data']['outputs'][0]
                return requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60).content
            elif poll['data']['status'] == 'failed':
                raise Exception("Génération échouée")
        
        raise Exception("Timeout")
    
    def refresh_gallery(self):
        """Rafraîchit la galerie avec les images existantes"""
        # Vider la galerie
        for widget in self.gallery_scroll.winfo_children():
            widget.destroy()
        
        # Chercher les images
        output_folder = Path(self.config.get("output_folder", Path.home() / "WaveSpeed_Images"))
        image_folders = sorted(output_folder.glob("*-post"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        self.current_images = []
        
        for folder in image_folders[:20]:  # Limiter à 20 derniers
            for img_file in ["A.jpg", "B.jpg"]:
                img_path = folder / img_file
                if img_path.exists():
                    self.current_images.append({
                        "path": img_path,
                        "folder": folder.name,
                        "type": img_file.replace(".jpg", "")
                    })
        
        # Mettre à jour compteur
        self.gallery_count.configure(text=f"{len(self.current_images)} images")
        
        # Créer les thumbnails
        for i, img_info in enumerate(self.current_images):
            self.create_thumbnail(img_info, i)
    
    def create_thumbnail(self, img_info, index):
        """Crée une miniature cliquable"""
        try:
            # Charger et redimensionner l'image
            img = Image.open(img_info["path"])
            img.thumbnail((150, 200))
            
            # Convertir pour CTk
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 200))
            
            # Frame conteneur
            container = ctk.CTkFrame(self.gallery_scroll, fg_color="transparent")
            container.pack(fill="x", pady=5)
            
            # Label image
            btn = ctk.CTkButton(
                container,
                image=ctk_img,
                text="",
                width=150,
                height=200,
                corner_radius=10,
                fg_color=self.colors["bg_tertiary"],
                hover_color=self.colors["accent"],
                command=lambda p=img_info: self.select_image(p)
            )
            btn.pack()
            
            # Label info
            info = ctk.CTkLabel(
                container,
                text=f"{img_info['folder'][:15]}... ({img_info['type']})",
                font=ctk.CTkFont(size=9),
                text_color=self.colors["text_secondary"]
            )
            info.pack()
            
        except Exception as e:
            print(f"Erreur thumbnail: {e}")
    
    def select_image(self, img_info):
        """Sélectionne une image pour la prévisualisation"""
        self.selected_image = img_info
        
        try:
            # Charger l'image en grand
            img = Image.open(img_info["path"])
            
            # Redimensionner pour le preview (max 800x600)
            img.thumbnail((800, 600))
            
            # Convertir
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            
            # Afficher
            self.preview_image.configure(image=ctk_img, text="")
            self.image_label.configure(text=f"{img_info['folder']} - {img_info['type']}")
            
            # Garder référence
            self.preview_image.image = ctk_img
            
        except Exception as e:
            print(f"Erreur preview: {e}")
    
    def open_output_folder(self):
        """Ouvre le dossier de sortie"""
        output_folder = self.config.get("output_folder", Path.home() / "WaveSpeed_Images")
        os.startfile(output_folder)
    
    def copy_prompt(self):
        """Copie le prompt dans le presse-papier"""
        if self.selected_image:
            try:
                folder = self.selected_image["path"].parent
                with open(folder / "prompts.txt", 'r') as f:
                    content = f.read()
                self.window.clipboard_clear()
                self.window.clipboard_append(content)
                self.update_status("📋 Prompt copié!")
            except:
                pass
    
    def delete_selected(self):
        """Supprime l'image sélectionnée"""
        if self.selected_image:
            from tkinter import messagebox
            if messagebox.askyesno("Confirmer", "Supprimer cette image ?"):
                try:
                    self.selected_image["path"].unlink()
                    self.refresh_gallery()
                    self.preview_image.configure(image="", text="📷 Aucune image sélectionnée")
                    self.update_status("🗑️ Image supprimée")
                except Exception as e:
                    self.show_error(str(e))
    
    def update_status(self, message):
        """Met à jour le statut"""
        self.status_label.configure(text=message)
    
    def reset_ui(self):
        """Réinitialise l'interface"""
        self.generate_btn.configure(state="normal", text="🚀 Générer les 2 images")
        self.progress.stop()
        self.progress.set(0)
    
    def show_error(self, message):
        """Affiche une erreur"""
        from tkinter import messagebox
        messagebox.showerror("Erreur", message)
    
    def show_success(self, message):
        """Affiche un succès"""
        from tkinter import messagebox
        messagebox.showinfo("Succès", message)
    
    def run(self):
        """Lance l'application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernWaveSpeedApp()
    app.run()
