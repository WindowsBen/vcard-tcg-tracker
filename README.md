# VCard TCG Pull Tracker

A desktop app for tracking card pulls from the [VCard TCG](https://www.vcardtcg.com) by Gamersupps.
Supports all three sets: **Rising Stars**, **Awakened Worlds**, and **Divine Chaos**.

---

## ⬇️ Download (just want the app?)

Head to the [**Releases**](../../releases) page and download the latest `VCard Tracker.exe`.

- No installation required — just run the `.exe`
- Keep the `vcard_tracker.db` file in the same folder as the `.exe` (it's created automatically on first run and stores all your data)

---

## ✨ Features

- 📦 **Box & Pack tracking** — open a box, log its Box Topper(s), then open up to 24 packs of 10 cards each
- 🔍 **Fast autocomplete** — type a partial name and rarity (e.g. `totless 8 h`) to instantly find and log a card
- 📊 **Stats** — see total boxes, packs, cards pulled, and a full rarity breakdown with percentage bars
- 📋 **Collection** — browse every unique card you've pulled, with copy counts, search, sort, and set filtering
- 🕓 **History** — browse past boxes and packs, view their full contents, and delete entries if needed
- 💾 **Persistent storage** — all data is saved locally in a SQLite database between sessions

### Rarity tiers (lowest → highest)
`Mascot` → `Mascot Holo` → `World` → `World Holo` → `Support` → `Support Holo` → `Secret Rare` → `8` → `8 Holo` → `9` → `9 Holo` → `10` → `God Rare`

Plus **Box Toppers**, logged separately when opening a box (1 per box for Awakened Worlds, 2 for Rising Stars and Divine Chaos).

---

## 🛠️ Running from source

**Requirements:**
- Python 3.10+
- See `requirements.txt`

**Setup:**
```bash
git clone https://github.com/WindowsBen/vcard-tcg-tracker.git
cd vcard-tcg-tracker
pip install -r requirements.txt
python main.py
```

---

## 📦 Building the .exe yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "VCard Tracker" main.py
```

Your `.exe` will be in the `dist/` folder.

> ⚠️ Keep `vcard_tracker.db` in the same folder as the `.exe` — this is where all your pull history is saved. Don't delete it unless you want to reset your data.

---

## 📁 Project structure

```
vcard-tcg-tracker/
├── main.py              # Full application source
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── vcard_tracker.db     # Auto-generated on first run (not in repo)
```

---

## 🤝 Contributing

Feel free to open issues or pull requests — whether it's adding a new set's card list, fixing a bug, or suggesting a feature.