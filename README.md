# WaveSpeed Image Generator for Leila

Logiciel Windows pour générer des images via l'API WaveSpeed (Nano Banana Pro) avec organisation automatique des fichiers.

## 🎯 Fonctionnalités

- ✅ Interface graphique simple (Windows)
- ✅ Génération d'images A et B (variante img2img)
- ✅ Organisation automatique : 1 dossier = 2 images + caption
- ✅ Pas de perte de qualité (2K, 9:16)
- ✅ Historique des générations
- ✅ Export .exe autonome

## 📁 Structure des dossiers générés

```
MesImages/
├── 2026-02-01_14-30-00-post1/
│   ├── A.jpg (image principale)
│   ├── B.jpg (variante)
│   └── caption.txt
├── 2026-02-01_14-35-22-post2/
│   ├── A.jpg
│   ├── B.jpg
│   └── caption.txt
└── ...
```

## 🚀 Installation

### Option 1 : Utiliser l'exécutable (.exe)
1. Télécharger `WaveSpeedGenerator.exe` dans les Releases
2. Double-cliquer pour lancer
3. Entrer votre clé API WaveSpeed
4. Commencer à générer !

### Option 2 : Depuis le code source
```bash
# Cloner le repo
git clone https://github.com/PierreOpenClaw/wavespeed-generator.git
cd wavespeed-generator

# Installer les dépendances
pip install -r requirements.txt

# Lancer
python main.py
```

## 📦 Créer l'exécutable (.exe)

```bash
# Installer PyInstaller
pip install pyinstaller

# Créer l'exécutable
pyinstaller --onefile --windowed --icon=icon.ico main.py

# L'exécutable sera dans dist/WaveSpeedGenerator.exe
```

## ⚙️ Configuration

Créer un fichier `config.json` :
```json
{
  "api_key": "votre_clé_api_wavespeed",
  "lora_path": "chemin/vers/image_lora.jpg",
  "output_folder": "chemin/vers/dossier_sortie"
}
```

## 📝 Utilisation

1. **Lancer le logiciel**
2. **Entrer le Prompt A** (image principale)
3. **Entrer le Prompt B** (variante - changements mineurs)
4. **Entrer la Caption** (texte pour Threads)
5. **Cliquer "Générer les 2 images"**
6. **Attendre** (2-3 minutes)
7. **Récupérer** les images dans le dossier créé

## 🔑 Obtenir une clé API WaveSpeed

1. Aller sur https://wavespeed.ai
2. Créer un compte
3. Générer une clé API dans les paramètres
4. Copier-coller dans le logiciel

## 📞 Support

Problèmes ? Questions ? Ouvrir une issue sur GitHub.

---

**Développé pour Leila 💜**
