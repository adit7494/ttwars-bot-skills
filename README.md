# TTWars Bot Skills 🏰🤖

A comprehensive skill/reference for building automation bots for **TTWars** (Travian private server). This skill enables AI agents (Claude, ChatGPT, Copilot, etc.) to understand the game's internal structure and write working bot code.

## What is TTWars?

TTWars is a Travian-based browser strategy game. Players build villages, train troops, manage resources, and compete on a shared world map. The game runs on PHP servers with embedded GraphQL APIs.

## What This Skill Covers

| Area | Details |
|------|---------|
| **Page Endpoints** | dorf1, dorf2, build, karte, profile, hero, statistics |
| **HTML Parsing** | CSS selectors, data attributes, embedded JSON |
| **GraphQL API** | Player queries, hero status, village data |
| **Buildings** | Complete gid mapping (40+ building types) |
| **Resources** | Wood, Clay, Iron, Crop production tracking |
| **Hero System** | Attributes, adventures, equipment, production |
| **Map System** | Coordinate conversion, tile loading, mark overlays |
| **Tribes** | All 9 tribe types with IDs |
| **Localization** | Indonesian → English translation table |

## Quick Start

### For AI Agents (Claude, ChatGPT, etc.)

Load the skill file into your context:

```
skills/ttwars-automation/SKILL.md
```

The skill provides everything needed to:
1. Parse game HTML pages
2. Extract GraphQL queries from page source
3. Send API requests with proper authentication
4. Build automation loops for resource management, building, and adventures

### For Developers

```bash
# Clone the repository
git clone https://github.com/adit7494/ttwars-bot-skills.git
cd ttwars-bot-skills

# Install Python dependencies
pip install requests beautifulsoup4

# Run the example bot
python examples/basic_bot.py
```

## Repository Structure

```
ttwars-bot-skills/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── skills/
│   └── ttwars-automation/
│       └── SKILL.md                   # Main skill reference (AI agent loadable)
├── examples/
│   ├── basic_bot.py                   # Minimal bot example
│   ├── resource_monitor.py            # Resource tracking
│   ├── auto_builder.py                # Building automation
│   └── hero_adventure.py              # Hero adventure automation
├── reference/
│   ├── buildings.md                   # Building ID reference
│   ├── graphql-queries.md             # GraphQL query examples
│   └── page-structure.md              # HTML structure reference
├── config/
│   └── .env.example                   # Environment variable template
└── .claude/
    └── CLAUDE.md                      # Claude Code project config
```

## Using with AI Agents

### Claude Code

```bash
# Copy the skill to your Claude skills directory
cp -r skills/ttwars-automation ~/.claude/skills/

# Or reference it directly in your prompt:
# "Using the ttwars-automation skill, write a bot that..."
```

### ChatGPT / Other LLMs

Paste the contents of `skills/ttwars-automation/SKILL.md` into your conversation context, then ask the agent to build specific automation features.

### Cursor / Copilot

Add the skill file to your project's context files or reference it in your `.cursorrules`.

## Example: Basic Bot

```python
import requests
from bs4 import BeautifulSoup

class TTWarsBot:
    def __init__(self, server, username, password):
        self.server = server
        self.session = requests.Session()
        self.login(username, password)

    def login(self, username, password):
        self.session.post(f'https://{self.server}/login', data={
            'name': username,
            'password': password,
            's1': 'Login'
        })

    def get_production(self):
        html = self.session.get(f'https://{self.server}/dorf1.php').text
        soup = BeautifulSoup(html, 'html.parser')
        production = {}
        table = soup.find('table', id='production')
        for row in table.find('tbody').find_all('tr'):
            res = row.find('td', class_='res').text.strip().rstrip(':')
            amt = int(row.find('td', class_='num').text.strip().replace(',', ''))
            production[res] = amt
        return production

    def get_buildings(self):
        html = self.session.get(f'https://{self.server}/dorf2.php').text
        soup = BeautifulSoup(html, 'html.parser')
        buildings = []
        for slot in soup.find_all('div', class_='buildingSlot'):
            buildings.append({
                'slot': slot.get('data-aid'),
                'gid': slot.get('data-gid'),
                'name': slot.get('data-name'),
                'level': slot.find('div', class_='labelLayer').text
            })
        return buildings

# Usage
bot = TTWarsBot('unl7.ttwars.com', 'your_username', 'your_password')
print(bot.get_production())
print(bot.get_buildings())
```

## Supported Servers

This skill works with any TTWars server instance. Common server URLs:
- `unl7.ttwars.com`
- `unl3.ttwars.com`
- `speed.ttwars.com`
- Any self-hosted TTWars instance

The HTML structure and API endpoints are consistent across TTWars servers.

## GraphQL API

The game embeds GraphQL queries in page `<script>` tags. Key queries:

```graphql
# Player profile
query($uid: Int!) {
  player(id: $uid) {
    id, name, tribeId
    alliance { id, tag }
    villages { id, name, population, x, y }
  }
}

# Hero status
query {
  ownPlayer {
    hero {
      isRegenerating
      homeVillage { mapId name }
      adventures { number mapId x y distance travelingDuration }
    }
  }
}
```

See `reference/graphql-queries.md` for the complete query reference.

## Game Resources

| Resource | Indonesian | Production Field |
|----------|-----------|-----------------|
| Wood | Kayu | gid=1 |
| Clay | Liat | gid=2 |
| Iron | Besi | gid=3 |
| Crop | Gandum | gid=4 |

## Tribes

| ID | Tribe | Special Unit |
|----|-------|-------------|
| 1 | Romans | Imperian |
| 2 | Teutons | Teutonic Knight |
| 3 | Gauls | Haeduan |
| 6 | Egyptians | — |
| 7 | Huns | — |
| 9 | Vikings | — |

## Contributing

1. Fork the repository
2. Add new skill patterns or examples
3. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

## Disclaimer

This project is for educational purposes. Always respect the terms of service of any game server you interact with. The authors are not responsible for any consequences of using this software.

---
