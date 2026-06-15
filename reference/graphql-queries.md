# TTWars GraphQL Query Reference

TTWars embeds GraphQL queries in page `<script>` tags. These can be extracted and replayed via POST requests.

## How GraphQL is Used

Each page that uses React components embeds a GraphQL query in its initialization script:

```javascript
window.Travian.React.PlayerProfile.render(
    {
        gql: "query($uid: Int!) { player(id: $uid) { ... } }",
        viewData: { /* pre-fetched response data */ },
        playerId: 61
    },
    ["spieler", "allgemein", "statistiken", "hero"]
);
```

## Extracting Queries from Pages

```python
import re

def extract_graphql(html: str) -> str:
    """Extract GraphQL query from page source."""
    match = re.search(r'gql:\s*"((?:[^"\\]|\\.)*)"', html)
    if match:
        query = match.group(1)
        query = query.replace('\\"', '"')
        query = query.replace('\\n', '\n')
        return query
    return ''

def extract_view_data(html: str) -> dict:
    """Extract pre-fetched viewData from page source."""
    import json
    match = re.search(r'viewData:\s*(\{.*?\})\s*,\s*(?:activePerspective|playerId)', html, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return {}
```

## Common Queries

### Player Profile

```graphql
query($uid: Int!, $subTabName: String!) {
    player(id: $uid) {
        id
        name
        tribeId
        alliance { id, tag }
        hero {
            gender
            horse
            imageHash
            level
            xp
            equipment {
                helmet { ...inventoryItemFields }
                leftHand { ...inventoryItemFields }
                rightHand { ...inventoryItemFields }
                body { ...inventoryItemFields }
                horse { ...inventoryItemFields }
                shoes { ...inventoryItemFields }
            }
        }
        ranks {
            populationRank
            population
            attackerRank
            attackerPoints
            defenderRank
            defenderPoints
        }
        villages {
            id
            name
            tribeId
            mapId
            population
            victoryPoints
            victoryPointsPerDay
            x
            y
            occupiedOases {
                bonus { amount, resourceType { id, code } }
            }
            region { id, name }
            typeText
            typeTitle
        }
        profile {
            ownProfile
            isNPC
            allowEdit
            gender
            location
            personalNote
            additionalLanguages
            countryFlag { language, languageName }
            descriptionPlain { description1, description2 }
            medalsGameworld { id, name, desc, code, type, rank }
            medalsLifetime { id, name, desc, code, imgUrl, width }
            daysPlaying
        }
    }
    ownPlayer {
        isSitter
        isLocked
        accessRights { readWriteMessages, buySpendGold, sendRaids }
        villages { id, sortIndex }
    }
    overviewPageFavouriteSubTabKey: favouriteTab(name: $subTabName) { key }
}

fragment inventoryItemFields on InventoryItem {
    typeId
    name
    attributes { description, descriptionDetails }
    tier: quality
    quality
    rarity
}
```

### Hero Status and Adventures

```graphql
query {
    ownPlayer {
        hero {
            isRegenerating
            regenerationTimeLeft
            homeVillage { mapId, id, name }
            status {
                status
                inOasis { belongsTo { mapId, name } }
                inVillage { id, mapId, name, type }
                arrivalAt
                arrivalIn
                onWayTo { id, x, y, type, village { mapId, name } }
            }
            adventures {
                number
                mapId
                x
                y
                distance
                place
                difficulty
                travelingDuration
            }
        }
        villages {
            id
            mapId
            name
            hasRallyPoint
            x
            y
        }
    }
}
```

### Village Buildings

```graphql
query {
    ownPlayer {
        villages {
            id
            name
            buildings {
                id
                gid
                name
                level
                maxLevel
            }
        }
    }
}
```

### Map Data

```graphql
query($x: Int!, $y: Int!) {
    mapTile(x: $x, y: $y) {
        id
        x
        y
        type
        village {
            id
            name
            population
            player { id, name, alliance { id, tag } }
        }
    }
}
```

## Sending GraphQL Requests

```python
import requests

class TTWarsGraphQL:
    def __init__(self, server, session):
        self.server = server
        self.session = session  # Already authenticated session

    def query(self, query_str, variables=None):
        """Execute a GraphQL query."""
        payload = {'query': query_str}
        if variables:
            payload['variables'] = variables

        resp = self.session.post(
            f'https://{self.server}/api/graphql',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        return resp.json()

    def get_player(self, player_id):
        """Get player profile data."""
        return self.query(
            'query($uid: Int!) { player(id: $uid) { id, name, tribeId } }',
            {'uid': player_id}
        )

    def get_hero(self):
        """Get hero status."""
        return self.query('''
            query {
                ownPlayer {
                    hero {
                        isRegenerating
                        status { status }
                        adventures { number, mapId, distance, travelingDuration }
                    }
                }
            }
        ''')
```

## GraphQL Response Format

```json
{
    "data": {
        "player": {
            "id": 61,
            "name": "claire",
            "tribeId": 3,
            "alliance": { "id": 1, "tag": "Friends" }
        }
    },
    "errors": []
}
```

## Error Handling

Common GraphQL errors:

| Error | Cause | Solution |
|-------|-------|----------|
| `Expected a value of type Int but received: "3345771463"` | 32-bit integer overflow | Parse as string |
| `Internal server error` | Server-side issue | Retry with backoff |
| `Not authenticated` | Session expired | Re-login |

## Variables

GraphQL variables are passed as a separate JSON object:

```python
variables = {
    'uid': 61,
    'subTabName': 'profileVillages'
}

result = gql.query(query_string, variables)
```
