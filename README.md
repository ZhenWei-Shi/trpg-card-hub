# TRPG Card Hub

[English](README.md) | [中文](README.zh.md)

**A config-driven, browser-based character sheet system for tabletop RPGs with custom rulesets.**

No app installs. No spreadsheet files. The GM configures the rules in a web UI; players fill in their sheets from any device via a shared URL.

---

## Problem

Narrative and homebrew TTRPGs have no dedicated tooling. Players either handwrite character sheets or maintain local Excel files — neither option works when players are away from home or the GM needs a quick overview of the whole party.

**This project solves three specific problems:**
- Players can view and update their character sheets from a phone, anywhere
- The GM sees every character in one dashboard
- Any custom ruleset can be configured through the admin UI — no code changes needed

---

## Features

| Feature | Details |
|---|---|
| **Config-driven UI** | GM sets attribute names, default values, field labels, visible sections, and theme colors from a visual editor |
| **Campaign room system** | GM creates a room, shares the invite link; characters are scoped to that campaign |
| **Shared character sheets** | All data lives on the server; a URL is the character sheet |
| **Password protection** | Each sheet can be locked with a password; GM can always view all sheets |
| **GM dashboard** | Admin panel with full party overview, room management, and rule configuration |

### Character Sheet (player view)
![Character sheet creation form](assets/screenshot-create.png)

### GM Admin Panel — Rule Configuration
![GM admin panel showing the rule config editor](assets/screenshot-admin.png)

---

## Tech Stack

- **Backend:** Python 3.11 / Flask, SQLite
- **Frontend:** Vanilla HTML/CSS/JS (zero framework dependencies)
- **Deploy:** Docker + gunicorn; includes `railway.toml` and `render.yaml` for one-click cloud deployment

---

## Architecture

The entire UI is driven by a single `config.json`. When the GM saves a config change in the admin panel, all players see the updated form on next page load — no redeployment needed.

```
config.json
  └── app name, theme colors
  └── character.stats[]     → renders attribute inputs + descriptions
  └── character.fields{}    → labels for occupation, appearance, backstory fields
  └── character.sections{}  → show/hide traits / skills / items sections
  └── skill_mode            → "generic" | "coc" | "dnd"
  └── currency, reference   → optional sidebar modules
```

The `admin_required` decorator protects all write endpoints; the GM password lives in `config.json` and is never exposed through the config API.

---

## Running Locally

```bash
# Python
pip install -r requirements.txt
python app.py
# → http://localhost:5000

# Docker
docker-compose up -d
```

Default GM password: `dm123456` — change it in `config.json` before deploying.

---

## Cloud Deployment

The app is stateless except for `data/characters.db`. Any platform that supports Docker and persistent volumes works.

**Recommended platforms:** Railway, Render, Fly.io / Alibaba Cloud, Tencent Cloud, Huawei Cloud

```bash
# Generic VPS flow
git clone https://github.com/ZhenWei-Shi/trpg-card-hub
cd trpg-card-hub
cp .env.example .env        # set SECRET_KEY
docker compose up -d
# open port 5000 in your firewall / security group
```

For Railway and Render: import the repo — `railway.toml` and `render.yaml` are already included. **Mount a persistent volume at `/app/data`** or the database resets on every redeploy.

---

## Usage Flow

```
1. GM logs into /admin  (default password: dm123456)
   └── "Rule Config" tab → set attributes, field names, visible sections

2. GM creates a campaign room
   └── "Rooms" tab → New Room → copy invite link → send to players

3. Players open the link
   └── Fill in the character sheet configured by the GM, optionally set a password

4. Anytime, anywhere
   └── Open the room link → enter password → view / edit the sheet
```

---

## Configuration Reference

All rule configuration is done through **Admin → Rule Config** — no file editing required.

| Setting | Description |
|---|---|
| Attribute list | Name, abbreviation, default value, minimum value, description text |
| Field labels | Display name and placeholder for occupation / appearance / backstory |
| Section toggles | Show or hide the traits, skills, and items sections |
| Theme colors | Primary color, background color, border color |

Changes take effect immediately for all players on next page load. Existing character data is unaffected.

---

## License

MIT
