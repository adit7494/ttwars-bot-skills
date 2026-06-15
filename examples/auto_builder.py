#!/usr/bin/env python3
"""
TTWars Auto Builder
Automatically upgrades buildings when resources are available.
Prioritizes resource fields, then infrastructure buildings.

Usage:
    python auto_builder.py --server unl7.ttwars.com --user myuser --pass mypass
"""

import requests
import time
import argparse
from bs4 import BeautifulSoup


class AutoBuilder:
    """Automated building upgrade system."""

    # Priority order for building upgrades
    BUILDING_PRIORITY = {
        1: 10,   # Lumber
        2: 10,   # Clay
        3: 10,   # Iron
        4: 10,   # Crop
        15: 8,   # Main Building
        10: 7,   # Warehouse
        11: 7,   # Granary
        13: 6,   # Smithy
        19: 5,   # Barracks
        20: 5,   # Stable
        22: 4,   # Academy
        17: 3,   # Marketplace
        18: 3,   # Embassy
    }

    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.base_url = f"https://{server}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self._login(username, password)

    def _login(self, username: str, password: str):
        self.session.post(f"{self.base_url}/login", data={
            'name': username, 'password': password, 's1': 'Login'
        })
        print(f"[+] Logged in")

    def get_buildings(self) -> list:
        """Get all buildings and their levels."""
        time.sleep(2)
        html = self.session.get(f"{self.base_url}/dorf2.php").text
        soup = BeautifulSoup(html, 'html.parser')

        buildings = []
        for slot in soup.find_all('div', class_='buildingSlot'):
            aid = slot.get('data-aid')
            gid = slot.get('data-gid')
            name = slot.get('data-name', '')
            level_el = slot.find('div', class_='labelLayer')
            link = slot.find('a', class_=True)

            is_max = link and 'maxLevel' in link.get('class', [])
            is_upgrading = link and 'notNow' in link.get('class', [])

            buildings.append({
                'slot': int(aid) if aid else None,
                'gid': int(gid) if gid else 0,
                'name': name,
                'level': int(level_el.text.strip()) if level_el else 0,
                'max_level': is_max,
                'upgrading': is_upgrading
            })

        return buildings

    def get_resource_fields(self) -> list:
        """Get resource field levels from dorf1."""
        time.sleep(2)
        html = self.session.get(f"{self.base_url}/dorf1.php").text
        soup = BeautifulSoup(html, 'html.parser')

        fields = []
        container = soup.find('div', id='resourceFieldContainer')
        if not container:
            return fields

        for link in container.find_all('a', href=True):
            if '/build.php?id=' not in link.get('href', ''):
                continue

            classes = link.get('class', [])
            level_el = link.find('div', class_='labelLayer')

            fields.append({
                'slot': int(link.get('data-aid', 0)),
                'gid': int(link.get('data-gid', 0)),
                'level': int(level_el.text.strip()) if level_el else 0,
                'upgrading': 'notNow' in classes,
                'max_level': 'maxLevel' in classes
            })

        return fields

    def try_upgrade(self, slot_id: int) -> bool:
        """Attempt to upgrade a building at the given slot."""
        time.sleep(2)
        url = f"{self.base_url}/build.php?id={slot_id}"
        html = self.session.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        # Find upgrade button (green button)
        upgrade_btn = soup.find('button', class_='green')
        if not upgrade_btn:
            print(f"  [-] Slot {slot_id}: No upgrade button found")
            return False

        # Check for sufficient resources
        # The button text or surrounding context indicates if upgrade is possible
        btn_text = upgrade_btn.text.strip().lower()
        if 'upgrade' in btn_text or 'tingkatkan' in btn_text:
            # Submit the upgrade
            token_input = soup.find('input', {'name': 'token'})
            data = {'upgrade': '1'}
            if token_input:
                data['token'] = token_input['value']

            resp = self.session.post(url, data=data)
            if resp.status_code == 200:
                print(f"  [+] Slot {slot_id}: Upgrade initiated!")
                return True

        return False

    def auto_upgrade_cycle(self):
        """Run one upgrade cycle across all buildings."""
        print("\n[*] Scanning buildings...")

        # Get resource fields
        fields = self.get_resource_fields()
        print(f"  Found {len(fields)} resource fields")

        # Get village buildings
        buildings = self.get_buildings()
        print(f"  Found {len(buildings)} village buildings")

        # Build priority list
        candidates = []

        for f in fields:
            if f['upgrading'] or f['max_level']:
                continue
            priority = self.BUILDING_PRIORITY.get(f['gid'], 1)
            candidates.append({**f, 'priority': priority, 'type': 'field'})

        for b in buildings:
            if b['upgrading'] or b['max_level'] or not b['gid']:
                continue
            priority = self.BUILDING_PRIORITY.get(b['gid'], 1)
            candidates.append({**b, 'priority': priority, 'type': 'building'})

        # Sort by priority (highest first), then by level (lowest first)
        candidates.sort(key=lambda x: (-x['priority'], x['level']))

        if not candidates:
            print("  [-] No buildings available for upgrade")
            return

        # Try to upgrade the highest priority building
        for candidate in candidates[:3]:
            name = candidate.get('name', f"gid={candidate['gid']}")
            print(f"  Trying: {name} (Level {candidate['level']}, "
                  f"Priority {candidate['priority']})")
            if self.try_upgrade(candidate['slot']):
                return

    def run(self, cycles: int = 10, interval: int = 300):
        """Run auto-builder for N cycles."""
        print(f"[*] Auto-builder: {cycles} cycles, {interval}s interval")
        print("=" * 50)

        for i in range(cycles):
            print(f"\n=== Cycle {i+1}/{cycles} ===")
            try:
                self.auto_upgrade_cycle()
            except Exception as e:
                print(f"[!] Error: {e}")

            if i < cycles - 1:
                print(f"[*] Waiting {interval}s...")
                time.sleep(interval)

        print("\n[*] Auto-builder finished.")


def main():
    parser = argparse.ArgumentParser(description='TTWars Auto Builder')
    parser.add_argument('--server', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--pass', dest='password', required=True)
    parser.add_argument('--cycles', type=int, default=10)
    parser.add_argument('--interval', type=int, default=300)
    args = parser.parse_args()

    builder = AutoBuilder(args.server, args.user, args.password)
    builder.run(cycles=args.cycles, interval=args.interval)


if __name__ == '__main__':
    main()
