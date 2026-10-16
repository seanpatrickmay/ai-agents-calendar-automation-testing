# Local calendar
Keep the app small: Python standard library, SQLite and plain browser assets.
Bind only to loopback. No deployment or cloud credentials. Pi (launched from `../studio/pi-studio.py`) uses the five custom calendar tools plus the studio file tools and `stable_id`, with local Ollama. Confirm destructive operations unless already explicitly authorized.
Run `python3 -m unittest discover -s tests -v` using isolated temporary databases.
Keep runtime data, logs and credentials out of Git. Preserve existing user changes.
