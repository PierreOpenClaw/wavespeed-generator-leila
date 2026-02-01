#!/usr/bin/env python3
"""
WaveSpeed Image Generator for Leila
Logiciel Windows avec interface graphique pour générer des images via API WaveSpeed
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import json
import time
import base64
from pathlib import Path
from datetime import datetime
import threading
import os

class WaveSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WaveSpeed Generator - Leila")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configuration
        self.config_file = Path("config.json")
        self.load_config()
        
        # Variables
        self.current_task_a = None
        self.current_task_b = None
        self.generating = False
        
        self.create_widgets()
        
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
    
    def create_widgets(self):
        """Crée l'interface graphique"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="🎨 WaveSpeed Image Generator", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        subtitle_label = ttk.Label(
            main_frame, 
            text="Pour Leila - Génération d'images Nano Banana Pro",
            font=('Helvetica', 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # === SECTION CONFIGURATION ===
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        config_frame.columnconfigure(1, weight=1)
        
        # API Key
        ttk.Label(config_frame, text="Clé API WaveSpeed:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value=self.config.get('api_key', ''))
        api_entry = ttk.Entry(config_frame, textvariable=self.api_key_var, show="*", width=50)
        api_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # LoRa Path
        ttk.Label(config_frame, text="Image LoRa:").grid(row=1, column=0, sticky=tk.W, pady=5)
        lora_frame = ttk.Frame(config_frame)
        lora_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        lora_frame.columnconfigure(0, weight=1)
        
        self.lora_var = tk.StringVar(value=self.config.get('lora_path', ''))
        lora_entry = ttk.Entry(lora_frame, textvariable=self.lora_var)
        lora_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(lora_frame, text="Parcourir", command=self.browse_lora).grid(row=0, column=1)
        
        # Output Folder
        ttk.Label(config_frame, text="Dossier de sortie:").grid(row=2, column=0, sticky=tk.W, pady=5)
        output_frame = ttk.Frame(config_frame)
        output_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar(value=self.config.get('output_folder', ''))
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Parcourir", command=self.browse_output).grid(row=0, column=1)
        
        # === SECTION PROMPTS ===
        prompts_frame = ttk.LabelFrame(main_frame, text="Prompts", padding="10")
        prompts_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        prompts_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Prompt A
        ttk.Label(prompts_frame, text="Prompt A (Image Principale):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.prompt_a = scrolledtext.ScrolledText(prompts_frame, height=4, wrap=tk.WORD)
        self.prompt_a.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Prompt B
        ttk.Label(prompts_frame, text="Prompt B (Variante - img2img):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.prompt_b = scrolledtext.ScrolledText(prompts_frame, height=4, wrap=tk.WORD)
        self.prompt_b.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Caption
        ttk.Label(prompts_frame, text="Caption (pour Threads):").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.caption = scrolledtext.ScrolledText(prompts_frame, height=3, wrap=tk.WORD)
        self.caption.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === SECTION ACTIONS ===
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.generate_btn = ttk.Button(
            actions_frame, 
            text="🚀 Générer les 2 images", 
            command=self.start_generation,
            width=30
        )
        self.generate_btn.pack()
        
        # === SECTION STATUS ===
        status_frame = ttk.LabelFrame(main_frame, text="Statut", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.status_var = tk.StringVar(value="Prêt")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, wraplength=700)
        status_label.pack(fill=tk.X)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # === SECTION HISTORIQUE ===
        history_frame = ttk.LabelFrame(main_frame, text="Derniers dossiers créés", padding="10")
        history_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.history_list = tk.Listbox(history_frame, height=5)
        self.history_list.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_list.config(yscrollcommand=scrollbar.set)
        
        # Sauvegarde auto config
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def browse_lora(self):
        """Ouvre le dialogue pour choisir l'image LoRa"""
        filename = filedialog.askopenfilename(
            title="Choisir l'image LoRa",
            filetypes=[("Images", "*.jpg *.jpeg *.png")]
        )
        if filename:
            self.lora_var.set(filename)
    
    def browse_output(self):
        """Ouvre le dialogue pour choisir le dossier de sortie"""
        folder = filedialog.askdirectory(title="Choisir le dossier de sortie")
        if folder:
            self.output_var.set(folder)
    
    def start_generation(self):
        """Démarre la génération dans un thread séparé"""
        if self.generating:
            return
        
        # Vérifications
        api_key = self.api_key_var.get().strip()
        lora_path = self.lora_var.get().strip()
        output_folder = self.output_var.get().strip()
        prompt_a = self.prompt_a.get("1.0", tk.END).strip()
        prompt_b = self.prompt_b.get("1.0", tk.END).strip()
        caption = self.caption.get("1.0", tk.END).strip()
        
        if not api_key:
            messagebox.showerror("Erreur", "Veuillez entrer votre clé API WaveSpeed")
            return
        
        if not lora_path or not Path(lora_path).exists():
            messagebox.showerror("Erreur", "Veuillez sélectionner une image LoRa valide")
            return
        
        if not prompt_a:
            messagebox.showerror("Erreur", "Veuillez entrer le Prompt A")
            return
        
        if not prompt_b:
            messagebox.showerror("Erreur", "Veuillez entrer le Prompt B")
            return
        
        # Sauvegarder config
        self.config['api_key'] = api_key
        self.config['lora_path'] = lora_path
        self.config['output_folder'] = output_folder
        self.save_config()
        
        # Démarrer la génération
        self.generating = True
        self.generate_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        thread = threading.Thread(
            target=self.generate_images,
            args=(api_key, lora_path, output_folder, prompt_a, prompt_b, caption)
        )
        thread.daemon = True
        thread.start()
    
    def generate_images(self, api_key, lora_path, output_folder, prompt_a, prompt_b, caption):
        """Génère les deux images"""
        try:
            # Créer le dossier de sortie
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = Path(output_folder) / f"{timestamp}-post"
            output_path.mkdir(parents=True, exist_ok=True)
            
            self.update_status(f"📁 Dossier créé: {output_path}")
            
            # Générer Image A
            self.update_status("🎨 Génération Image A (depuis LoRa)...")
            img_a = self.generate_single_image(api_key, lora_path, prompt_a, "A")
            
            if not img_a:
                self.update_status("❌ Échec génération Image A")
                return
            
            # Sauvegarder Image A
            img_a_path = output_path / "A.jpg"
            with open(img_a_path, 'wb') as f:
                f.write(img_a)
            self.update_status(f"✅ Image A sauvegardée ({len(img_a)} bytes)")
            
            # Générer Image B (img2img depuis A)
            self.update_status("🎨 Génération Image B (variante img2img)...")
            img_b = self.generate_variant(api_key, img_a, prompt_b)
            
            if not img_b:
                self.update_status("❌ Échec génération Image B")
                return
            
            # Sauvegarder Image B
            img_b_path = output_path / "B.jpg"
            with open(img_b_path, 'wb') as f:
                f.write(img_b)
            self.update_status(f"✅ Image B sauvegardée ({len(img_b)} bytes)")
            
            # Sauvegarder caption
            if caption:
                caption_path = output_path / "caption.txt"
                with open(caption_path, 'w', encoding='utf-8') as f:
                    f.write(caption)
                self.update_status("✅ Caption sauvegardée")
            
            # Sauvegarder prompts
            prompts_path = output_path / "prompts.txt"
            with open(prompts_path, 'w', encoding='utf-8') as f:
                f.write(f"PROMPT A (Image Principale):\n{prompt_a}\n\n")
                f.write(f"PROMPT B (Variante):\n{prompt_b}\n")
            
            # Ajouter à l'historique
            self.add_to_history(str(output_path))
            
            self.update_status(f"🎉 Post complet créé dans: {output_path}")
            messagebox.showinfo("Succès", f"Images générées avec succès!\nDossier: {output_path}")
            
        except Exception as e:
            self.update_status(f"❌ Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Une erreur est survenue:\n{str(e)}")
        finally:
            self.generating = False
            self.root.after(0, self.reset_ui)
    
    def generate_single_image(self, api_key, lora_path, prompt, name):
        """Génère une image depuis le LoRa"""
        with open(lora_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        data = {
            "prompt": prompt,
            "images": [f"data:image/jpeg;base64,{img_b64}"],
            "aspect_ratio": "9:16",
            "resolution": "2k",
            "output_format": "jpeg"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.post(
            "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit",
            json=data,
            headers=headers,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        
        result = response.json()
        task_url = result['data']['urls']['get']
        
        # Attendre le résultat
        for attempt in range(60):
            self.update_status(f"⏳ Attente {name}... ({attempt+1}/60)")
            time.sleep(2)
            
            poll_response = requests.get(
                task_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30
            )
            
            poll = poll_response.json()
            
            if poll['data']['status'] == 'completed' and poll['data']['outputs']:
                img_url = poll['data']['outputs'][0]
                img_response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
                return img_response.content
                
            elif poll['data']['status'] == 'failed':
                raise Exception("La génération a échoué")
        
        raise Exception("Timeout - la génération prend trop de temps")
    
    def generate_variant(self, api_key, base_image_data, prompt):
        """Génère une variante img2img"""
        img_b64 = base64.b64encode(base_image_data).decode('utf-8')
        
        data = {
            "prompt": prompt,
            "images": [f"data:image/jpeg;base64,{img_b64}"],
            "aspect_ratio": "9:16",
            "resolution": "2k",
            "output_format": "jpeg"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.post(
            "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit",
            json=data,
            headers=headers,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        
        result = response.json()
        task_url = result['data']['urls']['get']
        
        # Attendre le résultat
        for attempt in range(60):
            self.update_status(f"⏳ Attente variante... ({attempt+1}/60)")
            time.sleep(2)
            
            poll_response = requests.get(
                task_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30
            )
            
            poll = poll_response.json()
            
            if poll['data']['status'] == 'completed' and poll['data']['outputs']:
                img_url = poll['data']['outputs'][0]
                img_response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
                return img_response.content
                
            elif poll['data']['status'] == 'failed':
                raise Exception("La génération a échoué")
        
        raise Exception("Timeout - la génération prend trop de temps")
    
    def update_status(self, message):
        """Met à jour le statut (thread-safe)"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def add_to_history(self, folder_path):
        """Ajoute un dossier à l'historique"""
        self.root.after(0, lambda: self.history_list.insert(0, folder_path))
    
    def reset_ui(self):
        """Réinitialise l'interface"""
        self.generate_btn.config(state=tk.NORMAL)
        self.progress.stop()
    
    def on_closing(self):
        """Appelé à la fermeture"""
        if self.generating:
            if not messagebox.askyesno("Confirmer", "Une génération est en cours. Voulez-vous vraiment quitter?"):
                return
        self.save_config()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = WaveSpeedApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
