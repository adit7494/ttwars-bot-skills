# TTWars Bot Skills Project

## Skill Reference

The main skill file is at `skills/ttwars-automation/SKILL.md`. Load this when building bots or automation for ttwars.com servers.

## Key Files

- `skills/ttwars-automation/SKILL.md` — Main AI-agent-loadable skill
- `examples/basic_bot.py` — Minimal bot with login, resource parsing, building reading
- `examples/resource_monitor.py` — Continuous resource monitoring
- `examples/auto_builder.py` — Automated building upgrades
- `examples/hero_adventure.py` — Hero adventure automation
- `reference/buildings.md` — Complete building ID mapping
- `reference/graphql-queries.md` — GraphQL query reference
- `reference/page-structure.md` — HTML structure for parsing

## Tech Stack

- Python 3.8+
- `requests` for HTTP
- `beautifulsoup4` for HTML parsing
- GraphQL embedded in page `<script>` tags
