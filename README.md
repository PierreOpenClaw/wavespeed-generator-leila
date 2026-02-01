# WaveSpeed Generator pour Leila

Générateur d'images simple avec interface graphique.

## 🚀 Utilisation SIMPLE (sans .exe)

### 1. Installer Python
- Télécharger : https://python.org/downloads
- Cocher "Add Python to PATH" pendant l'installation

### 2. Télécharger ce dossier
- Télécharger le ZIP depuis GitHub
- Extraire dans un dossier

### 3. Installer les dépendances
Ouvrir un terminal (cmd) dans le dossier :
```
pip install requests
```

### 4. Lancer le logiciel
```
python main.py
```

## 📝 Configuration

Créer un fichier `config.json` :
```json
{
  "api_key": "TA_CLE_API_WAVESPEED",
  "lora_path": "C:/chemin/vers/ton/image_lora.jpg",
  "output_folder": "C:/Users/TonNom/Images"
}
```

## 🎯 Fonctionnement

1. Lancer : `python main.py`
2. Entrer la clé API
3. Choisir l'image LoRa
4. Coller Prompt A (image principale)
5. Coller Prompt B (variante)
6. Coller la caption
7. Cliquer "Générer"
8. Les images apparaissent dans le dossier de sortie

## 📁 Structure créée

```
Images/
├── 2026-02-01_22-30-00-post/
│   ├── A.jpg
│   ├── B.jpg
│   ├── caption.txt
│   └── prompts.txt
└── ...
```

## ❓ Problèmes ?

- **"python n'est pas reconnu"** → Réinstaller Python avec "Add to PATH"
- **"Module requests introuvable"** → Lancer `pip install requests`

## 🔑 Clé API WaveSpeed

1. Aller sur https://wavespeed.ai
2. Créer compte
3. Paramètres → API Keys
4. Copier la clé

---

**Pas besoin de créer d'.exe, tu lances juste `python main.py` !** 🎉
