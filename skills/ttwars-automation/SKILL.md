---
name: ttwars-automation
description: Use when building bots or automation scripts for ttwars.com (Travian private server) — covers HTML parsing, GraphQL API, building IDs, resource management, hero adventures, map coordinates, and troop management
---

# TTWars Automation Skill

## Overview

**TTWars** is a Travian private server variant. This skill provides the complete reference for building automation bots that interact with ttwars.com game servers. The game uses PHP-rendered HTML pages with embedded GraphQL endpoints, jQuery-based AJAX, and a coordinate-based map system.

**Core principle:** Every game page returns structured HTML with consistent CSS classes and data attributes. Parse these to extract game state; use GraphQL for advanced queries.

## When to Use

- Building a bot for any ttwars.com server instance
- Automating resource management, building upgrades, troop training
- Parsing game HTML to extract village state
- Sending GraphQL queries to the game API
- Coordinating hero adventures and map exploration

## Architecture

```
ttwars.com Server
├── PHP Pages (dorf1, dorf2, build, karte, profile, hero, statistics)
│   └── HTML with embedded JSON/GraphQL data in <script> tags
├── GraphQL Endpoint (/api/graphql or embedded in page scripts)
├── AJAX Endpoint (/ajax.php)
└── Map Tile System (/map/block/ and /map/mark/)
```

## Page Endpoints Reference

| Endpoint | Purpose | Key Data |
|----------|---------|----------|
| `dorf1.php` | Resource fields overview | Production rates, troop counts, resource levels |
| `dorf2.php` | Village center buildings | Building slots with levels, names, gids |
| `build.php?id=N` | Individual building page | Building-specific actions |
| `build.php?id=N&gid=M` | Building with specific type | Upgrade costs, training options |
| `karte.php` | World map | Coordinate-based tile data, player/alliance markers |
| `profile` | Player profile | Tribe, alliance, villages, rankings |
| `hero_attributes` | Hero stats | Level, XP, speed, attribute points, production |
| `hero_adventures` | Hero adventures list | Distance, duration, difficulty, mapId |
| `hero_inventory` | Hero equipment | Items, equipment slots |
| `statistics` | Rankings | Player/alliance/village/hero stats |

## Resource Types

| ID | Indonesian | English | CSS Class |
|----|-----------|---------|-----------|
| r1 | Kayu | Wood (Lumber) | `.r1` |
| r2 | Liat | Clay | `.r2` |
| r3 | Besi | Iron | `.r3` |
| r4 | Gandum | Crop | `.r4` |

## Building IDs (gid)

### Resource Fields (dorf1.php, slots 1-18)

| gid | Building | Notes |
|-----|----------|-------|
| 1 | Lumber (Kayu) | Wood resource field |
| 2 | Clay Pit (Liat) | Clay resource field |
| 3 | Iron Mine (Besi) | Iron resource field |
| 4 | Cropland (Gandum) | Crop resource field |

### Village Buildings (dorf2.php, slots 19-40+)

| gid | Building (Indonesian) | Building (English) |
|-----|----------------------|-------------------|
| 5 | Balai Kota | Town Hall |
| 6 | Pasar | Marketplace (note: also gid=17) |
| 7 | Kedutaan | Embassy |
| 8 | Penggilingan Gandum | Grain Mill |
| 9 | Toko Roti | Bakery |
| 10 | Gudang | Warehouse |
| 11 | Lumbung | Granary |
| 12 | Benteng | Wall (varies by tribe) |
| 13 | Pandai Besi | Smithy |
| 14 | Pusat Kebugaran | Training Ground |
| 15 | Bangunan Utama | Main Building |
| 17 | Pasar | Marketplace |
| 18 | Kedutaan | Embassy |
| 19 | Barak | Barracks |
| 20 | Istal | Stable |
| 21 | Bengkel | Workshop |
| 22 | Akademi | Academy |
| 23 | Pusat Kebugaran | Training Ground |
| 24 | Balai Desa | Residence/Palace |
| 25 | Bengkel | Workshop |
| 26 | Istana | Palace |
| 27 | Gudang Ilmu | Hero Mansion |
| 28 | Kantor Dagang | Trade Office |
| 35 | Pandai Besi | Smithy |
| 36 | Ahli Perangkap | Trapper |
| 37 | Padepokan | Great Warehouse/Granary |

## Tribe IDs

| ID | Tribe | Indonesian |
|----|-------|-----------|
| 1 | Romans | Romawi |
| 2 | Teutons | Teuton |
| 3 | Gauls | Galia |
| 4 | Nature | Alam |
| 5 | Natars | Natar |
| 6 | Egyptians | Suku Mesir |
| 7 | Huns | Suku Hun |
| 8 | Simple | Sederhana |
| 9 | Vikings | Suku Viking |

## HTML Parsing Guide

### Village Resource Fields (dorf1.php)

```python
# Parse resource production from dorf1.php
# The production table uses class "villageInfobox production"
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
production = soup.find('table', id='production')
for row in production.find('tbody').find_all('tr'):
    resource = row.find('td', class_='res').text.strip().rstrip(':')
    amount = row.find('td', class_='num').text.strip().replace(',', '')
    print(f"{resource}: {int(amount)}/hour")
```

### Village Buildings (dorf2.php)

```python
# Parse building slots from dorf2.php
# Each building has data attributes: data-aid, data-gid, data-name
for slot in soup.find_all('div', class_='buildingSlot'):
    aid = slot.get('data-aid')      # Slot ID (19-40)
    gid = slot.get('data-gid')      # Building type ID
    name = slot.get('data-name')    # Building name
    level_el = slot.find('div', class_='labelLayer')
    level = level_el.text if level_el else '0'
    print(f"Slot {aid}: {name} (gid={gid}) Level {level}")
```

### Troop Counts (dorf1.php)

```python
# Parse troops from the village info box
troops_table = soup.find('table', id='troops')
for row in troops_table.find('tbody').find_all('tr'):
    unit_img = row.find('img', class_=True)
    unit_class = [c for c in unit_img['class'] if c.startswith('u')][-1]
    count = row.find('td', class_='num').text.strip().replace(',', '')
    name = row.find('td', class_='un').text.strip()
    print(f"{name} ({unit_class}): {count}")
```

### Building Actions (build.php)

```python
# Parse building page for upgrade/train actions
# Look for upgrade buttons and cost tables
costs = soup.find('div', class_='showCosts')
if costs:
    for resource in costs.find_all('span'):
        r_class = resource.get('class', [])
        value = resource.text.strip()
        print(f"Cost: {value}")
```

## GraphQL API

The game embeds GraphQL queries in `<script>` tags. You can extract and replay these.

### Extracting GraphQL from Pages

```python
import re, json

# Find GraphQL query in page source
gql_match = re.search(r'gql:\s*"((?:[^"\\]|\\.)*)"', html)
if gql_match:
    query = gql_match.group(1).replace('\\"', '"').replace('\\n', '\n')
    print(query)

# Extract viewData (response data embedded in page)
view_match = re.search(r'viewData:\s*(\{.*?\}),\s*activePerspective', html, re.DOTALL)
if view_match:
    data = json.loads(view_match.group(1))
```

### Common GraphQL Queries

**Player Profile:**
```graphql
query($uid: Int!, $subTabName: String!) {
  player(id: $uid) {
    id, name, tribeId
    alliance { id, tag }
    hero { gender, horse, level, xp }
    ranks { populationRank, population, attackerRank, attackerPoints }
    villages { id, name, tribeId, mapId, population, x, y }
  }
}
```

**Hero Status:**
```graphql
query {
  ownPlayer {
    hero {
      isRegenerating
      regenerationTimeLeft
      homeVillage { mapId id name }
      status { status inVillage { id mapId name type } arrivalAt arrivalIn }
      adventures { number mapId x y distance place difficulty travelingDuration }
    }
    villages { id mapId name hasRallyPoint x y }
  }
}
```

### Sending GraphQL Requests

```python
import requests

session = requests.Session()
# Login first (cookie-based auth)
session.post(f'https://{server}/login', data={'name': user, 'password': pw, 's1': 'Login'})

# Send GraphQL
response = session.post(f'https://{server}/api/graphql', json={
    'query': query,
    'variables': variables
})
data = response.json()
```

## Map System

### Coordinate System

The map uses (x, y) coordinates. Each tile has a `mapId` calculated from coordinates.

```python
# Convert coordinates to mapId (approximate)
# Map width is typically 201 (-100 to +100) or 401 (-200 to +200)
def coords_to_mapid(x, y, map_width=401):
    return (y + map_width // 2) * map_width + (x + map_width // 2)

def mapid_to_coords(map_id, map_width=401):
    y = map_id // map_width - map_width // 2
    x = map_id % map_width - map_width // 2
    return x, y
```

### Map Tile Images

```
/map/block/{x1}.{y1}.{x2}.{y2}.png   # Terrain tiles
/map/mark/{x1}.{y1}.{x2}.{y2}.png    # Overlay markers (players, alliances)
/map/minimap.jpg                       # Minimap image
```

## Hero System

### Hero Attributes

| Attribute | Description |
|-----------|------------|
| Health | 0-100%, regenerates in village |
| Experience | Accumulates from adventures |
| Speed | Fields per hour (base + equipment bonus) |
| Strength | Combat damage |
| Off Bonus | Attack bonus percentage |
| Def Bonus | Defense bonus percentage |
| Resource Points | Production bonus allocation |

### Hero Production

The hero produces resources. Allocate points to:
- `productionPoints` → All resources equally
- `lumber_small` → Wood only
- `clay_small` → Clay only
- `iron_small` → Iron only
- `crop_small` → Crop only

### Adventures

```python
# Parse adventures from hero_adventures page
adventures = data['data']['ownPlayer']['hero']['adventures']
for adv in adventures:
    print(f"Adventure #{adv['number']}: "
          f"({adv['x']},{adv['y']}) "
          f"Distance: {adv['distance']} "
          f"Duration: {adv['travelingDuration']}s "
          f"Difficulty: {'hard' if adv['difficulty'] == 0 else 'normal'}")
```

### Sending Hero on Adventure

```python
# The adventure button has data-mapid attribute
# POST to the rally point or use the button's onclick
# Endpoint varies by server, typically:
session.post(f'https://{server}/build.php?id={rally_point_id}', data={
    'action': 'adventure',
    'mapId': adventure_map_id
})
```

## Bot Patterns

### Resource Monitor

```python
def monitor_resources(session, server):
    """Poll dorf1.php to track resource levels."""
    html = session.get(f'https://{server}/dorf1.php').text
    soup = BeautifulSoup(html, 'html.parser')

    production = {}
    prod_table = soup.find('table', id='production')
    for row in prod_table.find('tbody').find_all('tr'):
        res = row.find('td', class_='res').text.strip().rstrip(':')
        amt = int(row.find('td', class_='num').text.strip().replace(',', ''))
        production[res] = amt

    return production
```

### Auto Builder

```python
def upgrade_building(session, server, slot_id):
    """Attempt to upgrade a building at the given slot."""
    url = f'https://{server}/build.php?id={slot_id}'
    html = session.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # Look for upgrade button
    upgrade_btn = soup.find('button', class_='green')
    if upgrade_btn and 'upgrade' in str(upgrade_btn).lower():
        # Extract CSRF token if needed
        token = soup.find('input', {'name': 'token'})
        data = {'upgrade': 1}
        if token:
            data['token'] = token['value']
        return session.post(url, data=data)
    return None
```

### Auto Adventure

```python
def auto_adventure(session, server, prefer_short=True):
    """Send hero on the shortest available adventure."""
    # Get adventures from page
    html = session.get(f'https://{server}/hero_adventures').text

    # Extract GraphQL data
    match = re.search(r'viewData:\s*(\{.*?\})\s*,\s*activePerspective', html, re.DOTALL)
    if not match:
        return

    data = json.loads(match.group(1))
    adventures = data['data']['ownPlayer']['hero']['adventures']

    if not adventures:
        return

    # Sort by duration (shortest first)
    adventures.sort(key=lambda a: a['travelingDuration'])

    # Pick best adventure
    target = adventures[0] if prefer_short else adventures[-1]

    # Send hero (endpoint varies, check page for button action)
    rally_point = None
    for v in data['data']['ownPlayer']['villages']:
        if v['hasRallyPoint']:
            rally_point = v['id']
            break

    if rally_point:
        session.post(f'https://{server}/build.php?id={rally_point}', data={
            'action': 'adventure',
            'mapId': target['mapId']
        })
```

## Game Flow (Indonesian → English)

The game interface uses Indonesian (Bahasa) localization. Key translations:

| Indonesian | English |
|-----------|---------|
| Produksi per jam | Production per hour |
| Pasukan | Troops |
| Desa | Village |
| Suku | Tribe |
| Aliansi | Alliance |
| Populasi | Population |
| Koordinat | Coordinates |
| Peta | Map |
| Statistik | Statistics |
| Kesatria | Hero |
| Kesehatan | Health |
| Pengalaman | Experience |
| Kecepatan | Speed |
| Kekuatan | Strength |
| Bonus serang | Attack bonus |
| Bonus bertahan | Defense bonus |
| Sumber daya | Resources |
| Toko Roti | Bakery |
| Gudang | Warehouse |
| Lumbung | Granary |
| Barak | Barracks |
| Istal | Stable |
| Pandai Besi | Smithy |
| Bangunan Utama | Main Building |
| Balai Desa | Residence |
| Istana | Palace |
| Akademi | Academy |

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Internal server error` (GraphQL) | Integer overflow (32-bit) | Use string parsing for large values |
| Empty response | Session expired | Re-login and retry |
| `notNow` class on building | Building upgrade in progress | Wait for completion |
| `maxLevel` class on building | Already at max level | Skip this slot |
| Missing `data-gid` | Empty building slot | Available for construction |

## Rate Limiting

- Poll game pages no faster than once per 5-10 seconds
- GraphQL requests should have 2-3 second delays
- Avoid rapid-fire requests that trigger anti-bot detection
- Use random delays (±20%) to appear human-like

## Security Notes

- Store credentials in environment variables, never in code
- Use session cookies, not repeated logins
- Rotate user agents if making many requests
- Respect server rules regarding automation
