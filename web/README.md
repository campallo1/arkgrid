# ArkGrid Gem Optimizer - Web UI

This is a minimal Flask web UI that wraps the existing `gem_optimizer.py` logic.

Requirements
- Python 3.11

Quick start (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r web/requirements.txt
python web/app.py
```

Then open: http://127.0.0.1:8000

Notes:
- Gem lines use format: `WP OP AddDamage AtkPower BossDmg` (one gem per line).
- Specify number of `ANCIENT`, `RELIQUIA`, and `LEGENDARY` cores in the form.
- The web UI imports the `Gem` and `GemOptimizer` classes from `gem_optimizer.py` located at the workspace root.
