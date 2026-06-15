#!/usr/bin/env python3
"""
TTWars Hero Adventure Automation
Automatically sends the hero on the shortest available adventures
to maximize XP gain with minimal downtime.

Usage:
    python hero_adventure.py --server unl7.ttwars.com --user myuser --pass mypass
"""

import requests
import re
import json
import time
import argparse


class HeroAdventurer:
    """Automated hero adventure system."""

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
        print(f"[+] Logged in to {self.server}")

    def get_adventures(self) -> dict:
        """Fetch hero adventures and status from the adventures page."""
        time.sleep(2)
        html = self.session.get(f"{self.base_url}/hero_adventures").text

        # Extract viewData JSON from embedded script
        match = re.search(
            r'viewData:\s*(\{.*?\})\s*,\s*activePerspective',
            html, re.DOTALL
        )
        if not match:
            print("[!] Could not find adventure data")
            return {}

        try:
            data = json.loads(match.group(1))
            return data.get('data', {}).get('ownPlayer', {}).get('hero', {})
        except json.JSONDecodeError as e:
            print(f"[!] JSON parse error: {e}")
            return {}

    def find_best_adventure(self, adventures: list, prefer_hard: bool = False) -> dict:
        """Select the best adventure based on preferences."""
        if not adventures:
            return None

        # Filter by difficulty if requested
        if prefer_hard:
            hard = [a for a in adventures if a['difficulty'] == 0]  # 0 = hard
            if hard:
                adventures = hard

        # Sort by traveling duration (shortest first)
        adventures.sort(key=lambda a: a['travelingDuration'])
        return adventures[0]

    def send_hero_adventure(self, adventure: dict) -> bool:
        """Send hero on an adventure to the given mapId."""
        # The adventure button has data-mapid attribute
        # We need to POST to the rally point build page
        time.sleep(2)

        # First, get the rally point page to find the correct endpoint
        html = self.session.get(f"{self.base_url}/hero_adventures").text

        # Find the button for this adventure
        map_id = adventure['mapId']
        pattern = rf'data-mapid="{map_id}".*?<div><div>Jelajahi</div></div>'

        # Try direct POST to adventure endpoint
        # TTWars typically uses build.php with the rally point ID
        # We need to find the rally point building ID from the hero data
        data = {
            'action': 'adventure',
            'mapId': str(map_id),
            's1': 'ok'
        }

        # Try common rally point IDs (usually slot 39 or similar)
        for slot_id in [39, 40, 38]:
            resp = self.session.post(
                f"{self.base_url}/build.php?id={slot_id}",
                data=data
            )
            if resp.status_code == 200 and 'error' not in resp.text.lower():
                print(f"  [+] Hero sent to adventure #{adventure['number']} "
                      f"at ({adventure['x']}, {adventure['y']})")
                return True

        print(f"  [-] Failed to send hero on adventure #{adventure['number']}")
        return False

    def run(self, max_adventures: int = 10, prefer_hard: bool = False):
        """Run adventure automation loop."""
        print(f"[*] Hero Adventure Bot: up to {max_adventures} adventures")
        print("=" * 50)

        completed = 0

        while completed < max_adventures:
            hero = self.get_adventures()
            if not hero:
                print("[!] Could not get hero data, retrying...")
                time.sleep(10)
                continue

            # Check if hero is available
            status = hero.get('status', {})
            if status.get('status') != 100:
                print(f"[*] Hero not ready (status: {status.get('status')}%), waiting...")
                time.sleep(30)
                continue

            # Get adventures
            adventures = hero.get('adventures', [])
            if not adventures:
                print("[*] No adventures available, waiting...")
                time.sleep(60)
                continue

            # Find best adventure
            best = self.find_best_adventure(adventures, prefer_hard)
            if not best:
                print("[*] No suitable adventures found")
                break

            print(f"\n[*] Adventure #{best['number']}: "
                  f"({best['x']}, {best['y']}) "
                  f"Distance: {best['distance']} "
                  f"Duration: {best['travelingDuration']}s "
                  f"Difficulty: {'hard' if best['difficulty'] == 0 else 'normal'}")

            # Send hero
            if self.send_hero_adventure(best):
                completed += 1
                # Wait for adventure to complete + buffer
                wait_time = best['travelingDuration'] + 5
                print(f"  [*] Waiting {wait_time}s for adventure to complete...")
                time.sleep(wait_time)
            else:
                time.sleep(10)

        print(f"\n[*] Completed {completed} adventures")


def main():
    parser = argparse.ArgumentParser(description='TTWars Hero Adventure Bot')
    parser.add_argument('--server', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--pass', dest='password', required=True)
    parser.add_argument('--max', type=int, default=10, help='Max adventures')
    parser.add_argument('--hard', action='store_true', help='Prefer hard difficulty')
    args = parser.parse_args()

    adventurer = HeroAdventurer(args.server, args.user, args.password)
    adventurer.run(max_adventures=args.max, prefer_hard=args.hard)


if __name__ == '__main__':
    main()
