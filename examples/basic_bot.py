#!/usr/bin/env python3
"""
TTWars Basic Bot Example
A minimal bot that connects to a TTWars server, reads village state,
and provides helper methods for automation.

Usage:
    python basic_bot.py --server unl7.ttwars.com --user myuser --pass mypass
"""

import requests
import re
import json
import time
import argparse
from bs4 import BeautifulSoup


class TTWarsBot:
    """Basic TTWars automation bot."""

    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.base_url = f"https://{server}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.login(username, password)

    def login(self, username: str, password: str):
        """Authenticate with the game server."""
        resp = self.session.post(f"{self.base_url}/login", data={
            'name': username,
            'password': password,
            's1': 'Login'
        })
        if resp.status_code == 200 and 'dorf1' in resp.url:
            print(f"[+] Logged in as {username}")
        else:
            raise Exception(f"Login failed: {resp.status_code}")

    def get_page(self, path: str) -> str:
        """Fetch a game page and return HTML."""
        time.sleep(2)  # Rate limiting
        resp = self.session.get(f"{self.base_url}/{path}")
        return resp.text

    def get_production(self) -> dict:
        """Get hourly resource production rates."""
        html = self.get_page('dorf1.php')
        soup = BeautifulSoup(html, 'html.parser')

        production = {}
        table = soup.find('table', id='production')
        if not table:
            return production

        for row in table.find('tbody').find_all('tr'):
            res_td = row.find('td', class_='res')
            num_td = row.find('td', class_='num')
            if res_td and num_td:
                resource = res_td.text.strip().rstrip(':')
                amount = int(num_td.text.strip().replace(',', ''))
                production[resource] = amount

        return production

    def get_troops(self) -> list:
        """Get troops stationed in the village."""
        html = self.get_page('dorf1.php')
        soup = BeautifulSoup(html, 'html.parser')

        troops = []
        table = soup.find('table', id='troops')
        if not table:
            return troops

        for row in table.find('tbody').find_all('tr'):
            img = row.find('img', class_=True)
            if not img:
                continue
            # Extract unit class (e.g., u21, uhero)
            unit_classes = [c for c in img.get('class', []) if c.startswith('u')]
            count_td = row.find('td', class_='num')
            name_td = row.find('td', class_='un')
            if unit_classes and count_td:
                troops.append({
                    'unit': unit_classes[-1],
                    'name': name_td.text.strip() if name_td else 'Unknown',
                    'count': int(count_td.text.strip().replace(',', ''))
                })

        return troops

    def get_buildings(self) -> list:
        """Get all buildings in the village center."""
        html = self.get_page('dorf2.php')
        soup = BeautifulSoup(html, 'html.parser')

        buildings = []
        for slot in soup.find_all('div', class_='buildingSlot'):
            aid = slot.get('data-aid')
            gid = slot.get('data-gid')
            name = slot.get('data-name', '')
            level_el = slot.find('div', class_='labelLayer')
            level = level_el.text.strip() if level_el else '0'

            buildings.append({
                'slot': int(aid) if aid else None,
                'gid': int(gid) if gid else None,
                'name': name,
                'level': int(level)
            })

        return buildings

    def get_resource_fields(self) -> list:
        """Get resource field levels from dorf1."""
        html = self.get_page('dorf1.php')
        soup = BeautifulSoup(html, 'html.parser')

        fields = []
        container = soup.find('div', id='resourceFieldContainer')
        if not container:
            return fields

        for link in container.find_all('a', href=True):
            href = link.get('href', '')
            if '/build.php?id=' not in href:
                continue

            classes = link.get('class', [])
            level_el = link.find('div', class_='labelLayer')
            aid = link.get('data-aid')
            gid = link.get('data-gid')

            fields.append({
                'slot': int(aid) if aid else None,
                'gid': int(gid) if gid else None,
                'level': int(level_el.text.strip()) if level_el else 0,
                'max_level': 'notNow' in classes
            })

        return fields

    def get_hero_status(self) -> dict:
        """Get hero status from the hero attributes page."""
        html = self.get_page('hero_attributes')
        soup = BeautifulSoup(html, 'html.parser')

        # Extract hero data from embedded script
        script_match = re.search(r'render\(\s*(\{.*?\})\s*,', html, re.DOTALL)
        if not script_match:
            return {}

        try:
            # Try to parse the embedded data
            data_str = script_match.group(1)
            # This may need cleanup for valid JSON
            return {'raw': data_str[:500]}
        except Exception:
            return {}

    def get_adventures(self) -> list:
        """Get available hero adventures."""
        html = self.get_page('hero_adventures')

        # Extract viewData JSON
        match = re.search(r'viewData:\s*(\{.*?\})\s*,\s*activePerspective', html, re.DOTALL)
        if not match:
            return []

        try:
            data = json.loads(match.group(1))
            adventures = data.get('data', {}).get('ownPlayer', {}).get('hero', {}).get('adventures', [])
            return adventures
        except json.JSONDecodeError:
            return []

    def extract_graphql(self, page_html: str) -> str:
        """Extract GraphQL query embedded in a page."""
        match = re.search(r'gql:\s*"((?:[^"\\]|\\.)*)"', page_html)
        if match:
            return match.group(1).replace('\\"', '"').replace('\\n', '\n')
        return ''

    def summary(self):
        """Print a summary of the village state."""
        print("\n" + "="*50)
        print("TTWARS VILLAGE SUMMARY")
        print("="*50)

        # Production
        prod = self.get_production()
        print("\n--- Production (per hour) ---")
        for resource, amount in prod.items():
            print(f"  {resource}: {amount:,}")

        # Troops
        troops = self.get_troops()
        print(f"\n--- Troops ({len(troops)} types) ---")
        for t in troops:
            print(f"  {t['name']}: {t['count']:,}")

        # Buildings
        buildings = self.get_buildings()
        print(f"\n--- Buildings ({len(buildings)} slots) ---")
        for b in buildings:
            if b['name']:
                print(f"  Slot {b['slot']}: {b['name']} (Level {b['level']})")

        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(description='TTWars Basic Bot')
    parser.add_argument('--server', required=True, help='Server hostname')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--pass', dest='password', required=True, help='Password')
    args = parser.parse_args()

    bot = TTWarsBot(args.server, args.user, args.password)
    bot.summary()


if __name__ == '__main__':
    main()
