# TTWars Page Structure Reference

Detailed HTML structure of each game page for parsing.

## dorf1.php — Resource Fields Overview

### Structure

```html
<div id="content" class="village1">
    <div id="resourceFieldContainer" class="resourceField6 tribe3">
        <!-- Link to village center -->
        <a href="/dorf2.php" class="villageCenter"></a>

        <!-- Resource field slots (1-18) -->
        <a href="/build.php?id=1"
           class="notNow level colorLayer resourceField gid4 buildingSlot1 level20"
           data-aid="1" data-gid="4">
            <div class="labelLayer">20</div>
        </a>
        <!-- ... more fields ... -->
    </div>

    <div class="villageInfoWrapper">
        <!-- Production table -->
        <div class="villageInfobox production">
            <table id="production">
                <thead><tr><th colspan="4">Produksi per jam:</th></tr></thead>
                <tbody>
                    <tr>
                        <td class="ico"><div><i class="r1"></i></div></td>
                        <td class="res">Kayu:</td>
                        <td class="num">4,900,000</td>
                    </tr>
                    <!-- r2=Liat, r3=Besi, r4=Gandum -->
                </tbody>
            </table>
        </div>

        <!-- Troops table -->
        <div class="villageInfobox units">
            <table id="troops">
                <thead><tr><th colspan="3">Pasukan:</th></tr></thead>
                <tbody>
                    <tr>
                        <td class="ico"><img class="unit uhero" src="/img/x.gif"></td>
                        <td class="num">1</td>
                        <td class="un">kesatria</td>
                    </tr>
                    <tr>
                        <td class="ico"><img class="unit u21" src="/img/x.gif"></td>
                        <td class="num">3,024,023,111</td>
                        <td class="un">Phalanx</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

### Key Selectors

| Data | Selector |
|------|----------|
| Resource fields | `#resourceFieldContainer a[href*="build.php"]` |
| Field level | `a .labelLayer` |
| Field type | `a[data-gid]` |
| Production | `#production tbody tr` |
| Troops | `#troops tbody tr` |
| Resource rate | `td.res` + `td.num` |

## dorf2.php — Village Center

### Structure

```html
<div id="content" class="village2">
    <div id="villageContent">
        <!-- Building slots (19-40+) -->
        <div class="buildingSlot a19 g9 aid19 gaul"
             data-aid="19"
             data-gid="9"
             data-building-id="4756719"
             data-name="Toko Roti">
            <a class="level colorLayer maxLevel aid19 gaul"
               href="/build.php?id=19&amp;gid=9"
               data-level="5">
                <div class="labelLayer">5</div>
            </a>
            <img src="/img/x.gif" class="building g9 gaul" alt="">
            <svg><!-- building shape --></svg>
        </div>

        <!-- Empty slot -->
        <div class="buildingSlot a36 g0 aid36 gaul" data-aid="36" data-gid="0">
            <img src="/img/x.gif" class="building iso gaul" alt="">
            <a href="/build.php?id=36" class="emptyBuildingSlot"></a>
        </div>
    </div>
</div>
```

### Key Selectors

| Data | Selector |
|------|----------|
| Building slots | `.buildingSlot` |
| Slot ID | `.buildingSlot[data-aid]` |
| Building type | `.buildingSlot[data-gid]` |
| Building name | `.buildingSlot[data-name]` |
| Building level | `.buildingSlot .labelLayer` |
| Max level | `.buildingSlot a.maxLevel` |
| Upgrading | `.buildingSlot a.notNow` |
| Empty slot | `.buildingSlot .emptyBuildingSlot` |

## hero_attributes — Hero Stats

### Embedded Data

The hero page embeds full JSON data in a `<script>` tag:

```javascript
window.Travian.React.Hero.render(
    {
        "activeTabKey": "inventory",
        "favouriteTabKey": null,
        "tabBarName": "heroV2",
        "screenProps": {
            "inventory": {"knowledgeBaseLink": null},
            "attributes": {"knowledgeBaseLink": null},
            "appearance": {"knowledgeBaseLink": null}
        }
    },
    ["allgemein", "hero", "heroAppearance", "items", "build", "plus", "karte", "crafting"]
);
```

### HTML Attributes

| Data | Selector |
|------|----------|
| Hero level | `h1.titleInHeader` (text contains level) |
| Health bar | `.attributeHealth_medium` parent |
| XP value | `.attributeExperience_medium` parent `.value` |
| Speed | `.speedValue strong` |
| Strength input | `input[name="power"]` |
| Off bonus input | `input[name="offBonus"]` |
| Def bonus input | `input[name="defBonus"]` |
| Resource points | `input[name="productionPoints"]` |
| Hero location | `.heroState a` |

## hero_adventures — Adventure List

### Embedded Data

```javascript
window.Travian.React.HeroAdventure.render({
    gql: "query { ownPlayer { hero { adventures { ... } } } }",
    viewData: { /* full response data */ },
    activePerspective: "perspectiveResources"
});
```

### Adventure Table

```html
<table class="borderGap adventureList">
    <thead>
        <tr>
            <th class="place">Tempat</th>
            <th class="distance">Jarak</th>
            <th class="duration">Durasi</th>
            <th class="difficulty">Bahaya</th>
            <th class="button"></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="place"><img class="grassland" alt="Padang rumput"></td>
            <td class="distance">1 Bidang</td>
            <td class="duration"><div class="duration">00:00:01</div></td>
            <td class="difficulty"><i class="difficulty_normal"></i></td>
            <td class="button">
                <button data-mapid="47568">Jelajahi</button>
            </td>
        </tr>
    </tbody>
</table>
```

### Key Selectors

| Data | Selector |
|------|----------|
| Adventure rows | `.adventureList tbody tr` |
| Place type | `td.place img` class (grassland, forest, lake, clay, hill) |
| Distance | `td.distance` |
| Duration | `td.duration .duration` |
| Difficulty | `td.difficulty i` class (`difficulty_normal`, `difficulty_hard`) |
| Map ID | `td.button button[data-mapid]` |
| Explore button | `td.button button` |

## statistics — Player Rankings

### Structure

```html
<table id="player" class="row_table_data borderGap">
    <thead>
        <tr>
            <td class="ra">Rank</td>
            <td class="tribe">Tribe</td>
            <td class="pla">Player</td>
            <td class="banner">Banner</td>
            <td class="al">Alliance</td>
            <td class="pop">Population</td>
            <td class="vil">Villages</td>
        </tr>
    </thead>
    <tbody>
        <tr class="hover">
            <td class="ra">1.</td>
            <td class="tribe"><i class="tribe2_medium"></i></td>
            <td class="pla"><a href="/profile/71">Nowens</a></td>
            <td class="banner"></td>
            <td class="al">-</td>
            <td class="pop">6737</td>
            <td class="vil">6</td>
        </tr>
    </tbody>
</table>
```

### Key Selectors

| Data | Selector |
|------|----------|
| Rank | `td.ra` |
| Tribe icon | `td.tribe i` class (tribe1-tribe9) |
| Player name | `td.pla a` |
| Player ID | `td.pla a[href*="/profile/"]` |
| Alliance | `td.al a` |
| Population | `td.pop` |
| Village count | `td.vil` |

## karte.php — World Map

### Map Data

The map loads tile data via AJAX. Initial data is embedded:

```javascript
Travian.Game.Map.Options.Default.data = {
    "elements": [
        {
            "position": {"x": 21, "y": 62},
            "symbols": [{
                "dataId": "adventure681",
                "type": "adventure",
                "parameters": {"difficulty": 1},
                "title": "Petualangan"
            }]
        }
    ]
};
```

### Map Tile URLs

```
/map/block/{x1}.{y1}.{x2}.{y2}.png    # Terrain imagery
/map/mark/{x1}.{y1}.{x2}.{y2}.png?t={timestamp}  # Overlay markers
/map/minimap.jpg                        # Minimap overview
```

### Coordinate System

- Map center: (0, 0)
- Map size: typically 201×201 or 401×401
- Coordinates: (x, y) where x is horizontal, y is vertical
- Tiles are loaded in 600×600 pixel blocks
