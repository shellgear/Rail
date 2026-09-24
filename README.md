# Hermes Girl Avatar 🎮

Un avatar interattivo in stile pixel-art anni '90 che vive sul tuo desktop e si integra con Hermes Agent.

## ✨ Caratteristiche

- **Avatar sempre visibile**: finestra sempre in primo piano (always-on-top)
- **Screen capture automatico**: cattura lo schermo ogni N secondi (configurabile 5-60s)
- **Invio diretto a Hermes**: screenshot inviati via API per analisi (nessun salvataggio su disco)
- **Chat window**: piccola finestra stile "blocco note" che si apre al click
- **Suggerimenti Hermes**: l'avatar mostra i consigli di Hermes in tempo reale
- **Animazioni pixel art**: stile fighting game anni '90 (ispirato a Metaslug)
  - Idle, Speak, Think, Alert animations
- **System tray**: minimizza nell'area di notifica invece di chiudere

## 🚀 Installazione Rapida

### Prerequisiti

- **Python 3.10+** (verifica con `python3 --version`)
- **pip** (di solito incluso con Python)
- **Linux** (Ubuntu/Debian/Fedora) - X11 o Wayland

### Passo 1: Clona il repo

```bash
# Usa la chiave SSH configurata per shellgear
git clone git@github-shellgear:shellgear/Rail.git
cd Rail
```

### Passo 2: Crea e attiva virtual environment

```bash
# Crea virtual environment
python3 -m venv venv

# Attiva virtual environment
source venv/bin/activate

# Verifica che sia attivo (dovresti vedere (venv) nel prompt)
which python
```

### Passo 3: Installa dipendenze

```bash
# Installa tutte le dipendenze
pip install -r requirements.txt

# Verifica l'installazione
python -c "import PyQt6; print('PyQt6 OK')"
python -c "from PIL import Image; print('Pillow OK')"
```

### Passo 4: Configura Hermes API (opzionale ma consigliato)

Modifica `config.yaml` per puntare al tuo endpoint Hermes:

```yaml
api:
  endpoint: "http://localhost:8000/v1/chat/completions"  # Default Hermes locale
  model: "qwen3.5-122b"  # Modello Hermes
  timeout: 10
```

**Se non hai Hermes locale configurato**, l'app funzionerà comunque ma con risposte simulate.

### Passo 5: Avvia l'applicazione

```bash
# Avvia l'avatar
python -m hermes_avatar.main
```

L'applicazione apparirà nell'angolo in alto a destra dello schermo e si minimizzerà nell'area di notifica.

## ⚙️ Configurazione

Modifica `config.yaml` per personalizzare:

```yaml
# Intervallo screenshot (5-60 secondi)
screen_capture:
  interval_seconds: 30  # Default: 30s
  enabled: true

# Posizione avatar
avatar:
  width: 200
  height: 200
  position: "top-right"  # top-left, top-right, bottom-left, bottom-right
  always_on_top: true
  transparent_background: false

# Endpoint API Hermes
api:
  endpoint: "http://localhost:8000/v1/chat/completions"
  model: "qwen3.5-122b"
  timeout: 10
  format: "base64"

# Chat window
chat_window:
  width: 400
  height: 300
  position: "below_avatar"
  auto_open_on_message: true
```

## 🎮 Uso

### Interazione con l'avatar

- **Click sinistro**: Apre la chat window per inviare messaggi a Hermes
- **Click destro**: Apre il menu contestuale (Mostra, Chat, Toggle Screen Capture, Esci)
- **Minimizza**: L'avatar va nell'area di notifica (system tray)
- **Click sull'icona tray**: Apre il menu contestuale

### Screen capture automatico

- Cattura lo schermo ogni `interval_seconds` (configurabile)
- Invia screenshot a Hermes via API (nessun file salvato su disco)
- Hermes analizza e risponde con suggerimenti
- La chat window si apre automaticamente per mostrare le risposte

### Disattivare screen capture

- Dal menu tray: "Toggle Screen Capture"
- O in `config.yaml`: `screen_capture.enabled: false`

## 📁 Struttura del progetto

```
Rail/
├── config.yaml              # Configurazione
├── requirements.txt         # Dipendenze Python
├── README.md               # Questa guida
├── .gitignore
└── hermes_avatar/
    ├── __init__.py
    ├── main.py             # Applicazione principale PyQt6
    ├── screen_capture.py   # Screenshot in memoria → API Hermes
    ├── chat_window.py      # Finestra chat stile blocco note
    ├── sprite_animator.py  # Animazioni pixel art (placeholder)
    └── api_client.py       # (TODO: Integrazione API completa)
└── assets/
    └── hermes_girl/        # Placeholder per sprite sheets
        └── .gitkeep
```

## 🎨 Asset Pixel Art (TODO)

Gli sprite vanno posizionati in `assets/hermes_girl/{state}/{frame}.png`:

- **idle/**: 4 frame (animazione di riposo)
- **speak/**: 6 frame (quando Hermes parla)
- **think/**: 3 frame (quando sta pensando)
- **alert/**: 4 frame (quando c'è un avviso)

**Formato consigliato**: PNG 64x64 pixel, con trasparenza.

**Stile**: Pixel art anni '90, ispirato a Metaslug/fighting game classici.

## 🛠️ Sviluppo

### Ambiente di sviluppo

```bash
# Installa dipendenze di sviluppo (se aggiunte)
pip install -r requirements.txt

# Esegui test (se aggiunti)
python -m pytest  # TODO: Aggiungi test

# Lint (opzionale)
pip install flake8 black
flake8 hermes_avatar/
black hermes_avatar/
```

### Test locali

```bash
# Verifica configurazione
python -c "from hermes_avatar.screen_capture import ScreenCapture; c = ScreenCapture(); print('Config:', c.config.get('screen_capture'))"

# Test screen capture (se X11 disponibile)
python -c "from hermes_avatar.screen_capture import ScreenCapture; sc = ScreenCapture(); data = sc.capture_screenshot(); print(f'Screenshot size: {len(data)} bytes')"

# Avvia applicazione
python -m hermes_avatar.main
```

## 🐛 Risoluzione problemi

### PyQt6 non trovato

```bash
pip install PyQt6
# Oppure con venv attivo:
source venv/bin/activate
pip install PyQt6
```

### Screen capture non funziona

- Assicurati di essere su **Linux** con **X11** o **Wayland**
- Se usi Wayland, potresti aver bisogno di permessi aggiuntivi
- Prova a installare `python3-pyqt6` via apt: `sudo apt install python3-pyqt6`

### API Hermes non risponde

- Verifica che Hermes sia in esecuzione su `localhost:8000`
- Controlla `config.yaml` per l'endpoint corretto
- Se Hermes non è configurato, l'app mostrerà risposte simulate

### Finestra non appare

- Controlla che il virtual environment sia attivo
- Verifica che PyQt6 sia installato: `python -c "import PyQt6; print('OK')"`
- Prova ad avviare con output dettagliato: `python -m hermes_avatar.main 2>&1 | head -50`

## 📝 Roadmap

- [x] Struttura progetto
- [x] Screen capture in memoria
- [x] Chat window
- [x] Sprite animator (placeholder)
- [x] Integrazione base PyQt6
- [x] System tray integration
- [ ] Sprite sheets pixel art completi (stile Metaslug)
- [ ] Integrazione API Hermes completa
- [ ] Tasto scorciatoia per screenshot manuale
- [ ] Notifiche desktop
- [ ] Supporto multi-monitor
- [ ] Tema personalizzabile
- [ ] Test automatizzati
- [ ] Documentazione API

## 📄 Licenza

MIT License

---

**Developed by Simo** per l'ecosistema Hermes 🚀

Repo: `https://github.com/shellgear/Rail`
