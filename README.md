# 🎨 WaveSpeed Generator - Modern UI for Leila

Interface moderne et élégante pour générer des images avec WaveSpeed.

## ✨ Caractéristiques

- 🌙 **Thème Dark/Gothique** - Interface sombre et stylée
- 🖼️ **Prévisualisation** - Visualisation des images en grand format
- 🎴 **Galerie thumbnails** - Toutes tes images organisées
- 📁 **Organisation auto** - Dossiers datés avec A.jpg + B.jpg + caption.txt
- ⚡ **Génération rapide** - Images 2K, format 9:16
- 💾 **Historique** - Accès rapide aux générations précédentes

## 🚀 Installation

### 1. Installer Python
https://python.org/downloads
→ Cocher "Add Python to PATH"

### 2. Installer les dépendances
```bash
pip install customtkinter pillow requests
```

### 3. Lancer l'application
```bash
python main_modern.py
```

## 📝 Configuration

Créer un fichier `config.json` :
```json
{
  "api_key": "votre_clé_api_wavespeed",
  "lora_path": "C:/chemin/vers/votre_image_lora.jpg",
  "output_folder": "C:/Users/VotreNom/Images"
}
```

## 🎨 Interface

```
┌─────────────────┬───────────────────┬─────────────────┐
│   ⚡ CONFIG     │    👁️ PREVIEW     │    🖼️ GALLERY   │
│                 │                   │                 │
│  🔑 API Key     │                   │  ┌───────────┐  │
│  🖼️ LoRa       │    [IMAGE A]      │  │ Thumb 1   │  │
│                 │                   │  └───────────┘  │
│  ✏️ Prompt A    │                   │  ┌───────────┐  │
│  🎨 Prompt B    │                   │  │ Thumb 2   │  │
│  💬 Caption     │                   │  └───────────┘  │
│                 │                   │                 │
│  🚀 Générer     │  📂 📋 🗑️         │                 │
│                 │                   │                 │
└─────────────────┴───────────────────┴─────────────────┘
```

## 📁 Structure créée

```
Images/
├── 2026-02-01_22-30-00-post/
│   ├── A.jpg          (Image principale)
│   ├── B.jpg          (Variante)
│   ├── caption.txt    (Pour Threads)
│   └── prompts.txt    (Backup)
└── ...
```

## 🎯 Utilisation

1. **Lancer** : `python main_modern.py`
2. **Configurer** : Entrer clé API et chemin LoRa
3. **Prompts** : Coller Prompt A (principal) et B (variante)
4. **Caption** : Texte pour Threads
5. **Générer** : Cliquer le bouton violet
6. **Visualiser** : Les images apparaissent dans la galerie
7. **Sélectionner** : Cliquer une thumbnail pour voir en grand

## 🎨 Thème

- **Dark mode** - Noir profond (#1a1a1a)
- **Accent violet** - Style gothique (#8b5cf6)
- **Coins arrondis** - Design moderne
- **Ombres subtiles** - Profondeur

## 🔑 Obtenir clé API

1. https://wavespeed.ai
2. Créer compte
3. Paramètres → API Keys
4. Copier la clé

---

**Design moderne pour Leila 💜**
