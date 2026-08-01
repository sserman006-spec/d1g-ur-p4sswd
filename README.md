# 🔐 D1G UR P4SSWD

**Account Security Checker** — a colorful, zero-dependency CLI tool that checks whether your password has been exposed in a data breach, scores its real-world strength, and generates a secure, memorable replacement if you need one.

> Built after a friend's Instagram account got hacked — most account takeovers trace back to weak or leaked passwords, not sophisticated attacks. This tool tells you *before* it happens, not after.

---

## 🚀 Quick Start

### Requirements
- Python 3.10 or higher
- No external dependencies — pure Python standard library

### Installation

```bash
git clone https://github.com/sserman006-spec/d1g-ur-p4sswd.git
cd d1g-ur-p4sswd
python3 digurpasswd.py
```

That's it. No `pip install`. No virtual environment. No setup. Just run.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Breach Check** | Checks your password against 900M+ known breached passwords via the [Have I Been Pwned](https://haveibeenpwned.com/API/v3) Pwned Passwords API |
| 💪 **Strength Score** | Rates your password 0–100 based on length, character variety, and common weak patterns — includes an estimated crack time |
| 🔑 **Passphrase Generator** | Generates strong, memorable passphrases (e.g. `Falcon-River-Canyon-Solstice-32`) using cryptographically secure randomness |
| 🎨 **Dynamic UI** | 9 different randomized intro animations, a live spinner during the breach check, and a fully centered, colorful terminal interface |
| 🔒 **Privacy First** | Nothing you type is ever stored, logged, or written to disk — everything lives in memory for the duration of a single run |

---

## 🖥️ How It Works

### 1. Breach Check (`password_checker.py`)
Uses the **k-anonymity** method:
1. Your password is hashed locally with SHA-1 — it never leaves your machine in plain text.
2. Only the first 5 characters of the hash are sent to the HIBP API.
3. HIBP returns every breached hash sharing that prefix (hundreds of them).
4. Your script checks locally whether your full hash is in that list.

Your actual password and full hash **never leave your device**.

### 2. Strength Scoring (`strength_checker.py`)
Combines two signals:
- **Entropy math** — `length × log2(character_pool_size)` to estimate crack time against a realistic offline attack speed.
- **Pattern detection** — flags dictionary words, keyboard walks (`qwerty`, `asdf`), and predictable "word+numbers" shapes, since real attackers try these before brute force.

### 3. Passphrase Generation (`passphrase_generator.py`)
Uses Python's `secrets` module (not `random` — which is *not* cryptographically secure) to pick random words and numbers, producing passphrases that are both strong and easy to remember.

---

## 📁 Project Structure

```
d1g-ur-p4sswd/
├── digurpasswd.py           # Main program — UI, menu, animations
├── password_checker.py      # Breach check via HIBP API
├── strength_checker.py      # Strength scoring + crack-time estimate
└── passphrase_generator.py  # Secure passphrase generator
```

---

## 🔒 Privacy & Disclaimer

Passwords entered into this tool are **never stored, logged, printed to a file, or transmitted anywhere** beyond the single, privacy-preserving breach-check API call described above. Everything happens in memory for the duration of one run and is discarded when the tool exits.

For a deeper walkthrough of the design and privacy approach, see my LinkedIn post: **[link here]**

---

## ⚠️ Limitations

- A "not found in breaches" result means the password isn't in HIBP's *current* dataset — not an absolute guarantee it's safe everywhere.
- This tool checks your **password**, not a specific platform account. No external tool can verify whether a third-party account (e.g. Instagram) is compromised without the owner's own login access.
- The breach check requires an internet connection; the strength score and passphrase generator work fully offline.

---

## ✅ Responsible Use

This is an educational / personal-security tool built to help people check their **own** passwords — not a tool for testing, guessing, or accessing anyone else's accounts or credentials. Please only use it on passwords you own.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| HTTP requests | `urllib.request` (stdlib) |
| Hashing | `hashlib` (stdlib) |
| Secure randomness | `secrets` (stdlib) |
| Pattern/entropy logic | `re`, `math` (stdlib) |
| Terminal UI | Raw ANSI escape codes (no external UI library) |
| Breach data | [HIBP Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords) |

---

## 👤 Author

**Serman Muthu Sundaresh B** (aka **N4MR3S**)
BE CSE (Cybersecurity), 3rd Year
PSNA College of Engineering and Technology

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to fork, learn from, and build on, with attribution appreciated.
