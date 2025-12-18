# Mini Worms (worms-mini)

Ein kleines, lokales 2-Spieler Browsergame (Canvas) als eigenständiger Flask-Service für Google Cloud Run (Source Deploy, ohne Dockerfile).

## Lokal starten

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
python main.py
