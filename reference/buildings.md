# TTWars Building Reference

Complete mapping of building IDs (gid) to building names and types.

## Resource Fields (dorf1.php)

These are the 18 resource field slots on the village overview page.

| Slot | gid | Building | Resource |
|------|-----|----------|----------|
| 1 | 4 | Cropland | Crop |
| 2 | 4 | Cropland | Crop |
| 3 | 1 | Lumber | Wood |
| 4 | 3 | Iron Mine | Iron |
| 5 | 4 | Cropland | Crop |
| 6 | 4 | Cropland | Crop |
| 7 | 4 | Cropland | Crop |
| 8 | 4 | Cropland | Crop |
| 9 | 4 | Cropland | Crop |
| 10 | 4 | Cropland | Crop |
| 11 | 4 | Cropland | Crop |
| 12 | 4 | Cropland | Crop |
| 13 | 4 | Cropland | Crop |
| 14 | 4 | Cropland | Crop |
| 15 | 4 | Cropland | Crop |
| 16 | 2 | Clay Pit | Clay |
| 17 | 4 | Cropland | Crop |
| 18 | 4 | Cropland | Crop |

**Field distribution varies by map position.** Common distributions:
- 3-4-5-6 (Wood-Clay-Iron-Crop)
- 4-4-4-6
- 1-1-1-15
- 4-5-3-6

## Village Buildings (dorf2.php)

Buildings that can be constructed in the village center (slots 19-40).

### Core Buildings

| gid | Building (EN) | Building (ID) | Max Level | Purpose |
|-----|--------------|---------------|-----------|---------|
| 15 | Main Building | Bangunan Utama | 20 | Construction speed bonus |
| 10 | Warehouse | Gudang | 20 | Resource storage |
| 11 | Granary | Lumbung | 20 | Crop storage |
| 17 | Marketplace | Pasar | 20 | Resource trading |
| 18 | Embassy | Kedutaan | 20 | Alliance management |

### Military Buildings

| gid | Building (EN) | Building (ID) | Max Level | Purpose |
|-----|--------------|---------------|-----------|---------|
| 19 | Barracks | Barak | 20 | Infantry training |
| 20 | Stable | Istal | 20 | Cavalry training |
| 21 | Workshop | Bengkel | 20 | Siege engines |
| 14 | Training Ground | Pusat Kebugaran | 20 | Troop training speed |
| 13 | Smithy | Pandai Besi | 20 | Unit research |
| 22 | Academy | Akademi | 20 | Advanced unit research |

### Special Buildings

| gid | Building (EN) | Building (ID) | Max Level | Purpose |
|-----|--------------|---------------|-----------|---------|
| 24 | Residence | Balai Desa | 20 | Culture points, settlers |
| 26 | Palace | Istana | 20 | Capital designation |
| 27 | Hero Mansion | Gudang Ilmu | 20 | Hero oasis control |
| 28 | Trade Office | Kantor Dagang | 20 | Merchant capacity |
| 36 | Trapper | Ahli Perangtrap | 20 | Trap construction (Gaul) |
| 37 | Great Warehouse | Padepokan | 20 | Extra storage |

### Resource Buildings

| gid | Building (EN) | Building (ID) | Max Level | Purpose |
|-----|--------------|---------------|-----------|---------|
| 8 | Grain Mill | Penggilingan Gandum | 5 | +5% crop per level |
| 9 | Bakery | Toko Roti | 5 | +5% crop per level |
| 4 | Brickyard | -- | 20 | +5% clay per level |
| 5 | Iron Foundry | -- | 20 | +5% iron per level |
| 6 | Sawmill | -- | 20 | +5% wood per level |

## HTML Parsing

### Building Slot Data Attributes

```html
<div class="buildingSlot a19 g9 aid19 gaul"
     data-aid="19"
     data-gid="9"
     data-building-id="4756719"
     data-name="Toko Roti">
```

| Attribute | Description |
|-----------|------------|
| `data-aid` | Slot ID (19-40) |
| `data-gid` | Building type ID |
| `data-building-id` | Unique building instance ID |
| `data-name` | Building name (Indonesian) |

### Building State Classes

| CSS Class | Meaning |
|-----------|---------|
| `maxLevel` | Building at maximum level |
| `notNow` | Currently being upgraded |
| `emptyBuildingSlot` | Empty slot, available for construction |
| `good` | Can be upgraded |
| `colorLayer` | Visual indicator layer |

### Level Display

```html
<a class="level colorLayer maxLevel aid19 gaul" href="/build.php?id=19&amp;gid=9">
    <div class="labelLayer">5</div>
</a>
```

The `labelLayer` div contains the current building level.

## Upgrade Costs

Upgrade costs scale with level. The general formula:

```
Wood  = base_wood * 1.2^(level-1)
Clay  = base_clay * 1.2^(level-1)
Iron  = base_iron * 1.2^(level-1)
Crop  = base_crop * 1.2^(level-1)
Time  = base_time * 1.2^(level-1)
```

Base costs vary by building type. Check the individual `build.php?id=N&gid=M` page for exact costs at each level.

## Tribe-Specific Buildings

| Tribe | Unique Building | gid |
|-------|----------------|-----|
| Gauls | Trapper (Ahli Perangkap) | 36 |
| Romans | Embassy (extra) | 18 |
| Teutons | Brewery | 33 |

## Wall Types

| Tribe | Wall Building | gid |
|-------|--------------|-----|
| Romans | City Wall | 31 |
| Teutons | Earth Wall | 32 |
| Gauls | Palisade | 33 |
| Egyptians | Stone Wall | 41 |
| Huns | Makeshift Wall | 42 |
