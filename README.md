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

## 🚀 Installazione

```bash
# Clona il repo
git clone git@github-shellgear:shellgear/rail.git
cd rail

# Crea e attiva virtual environment
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python -m hermes_avatar.main
```

## ⚙️ Configurazione

Modifica `config.yaml` per personalizzare:

```yaml
# Intervallo screenshot (5-60 secondi)
screen_capture:
  interval_seconds: 30

# Posizione avatar
avatar:
  position: "top-right"  # top-left, top-right, bottom-left, bottom-right
  width: 200
  height: 200

# Endpoint API Hermes
api:
  endpoint: "http://localhost:8000/v1/chat/completions"
  model: "qwen3.5-122b"
```

## 📁 Struttura del progetto

```
rail/
├── config.yaml              # Configurazione
├── requirements.txt         # Dipendenze Python
├── hermes_avatar/
│   ├── __init__.py
│   ├── main.py             # Applicazione principale
│   ├── screen_capture.py   # Modulo screenshot in memoria
│   ├── chat_window.py      # Finestra chat
│   ├── sprite_animator.py  # Sistema animazioni
│   └── api_client.py       # Comunicazione Hermes (TODO)
└── assets/
    └── hermes_girl/        # Sprite sheets (da creare)
        ├── idle/
        ├── speak/
        ├── think/
        └── alert/
```

## 🎨 Asset Pixel Art

Gli sprite vanno posizionati in `assets/hermes_girl/{state}/{frame}.png`:

- **idle/**: 4 frame (animazione di riposo)
- **speak/**: 6 frame (quando Hermes parla)
- **think/**: 3 frame (quando sta pensando)
- **alert/**: 4 frame (quando c'è un avviso)

Formato consigliato: 64x64 pixel, PNG con trasparenza.

## 🔧 Sviluppo

### Prerequisiti

- Python 3.10+
- PyQt6
- Pillow (PIL)
- PyGame (opzionale, per alternative screen capture)

### Test locali

```bash
# Avvia in modalità sviluppo
python -m hermes_avatar.main

# Verifica configurazione
python -c "from hermes_avatar.screen_capture import ScreenCapture; print(ScreenCapture().config)"
```

## 🛠️ Roadmap

- [x] Struttura progetto
- [x] Screen capture in memoria
- [x] Chat window
- [x] Sprite animator (placeholder)
- [x] Integrazione base PyQt6
- [ ] Sprite sheets pixel art completi
- [ ] Integrazione API Hermes completa
- [ ] Tasto scorciatoia per screenshot manuale
- [ ] Notifiche desktop
- [ ] Supporto multi-monitor
- [ ] Tema personalizzabile

## 📝 Note

- **Linux only**: Screen capture usa X11/PyQt6
- **API endpoint**: Configurabile per puntare al tuo Hermes locale
- **No disk storage**: Gli screenshot vengono inviati direttamente, non salvati

## 📄 Licenza

MIT License

---

**Developed by Simo** for the Hermes ecosystem 🚀
