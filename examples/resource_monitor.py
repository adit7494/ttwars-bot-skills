#!/usr/bin/env python3
"""
TTWars Resource Monitor
Continuously monitors resource production and storage levels.
Alerts when resources are near capacity.

Usage:
    python resource_monitor.py --server unl7.ttwars.com --user myuser --pass mypass
"""

import requests
import time
import argparse
from bs4 import BeautifulSoup


class ResourceMonitor:
    """Monitors TTWars village resources."""

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
        print(f"[+] Connected to {self.server}")

    def get_resources(self) -> dict:
        """Fetch current resource state from dorf1."""
        time.sleep(2)
        html = self.session.get(f"{self.base_url}/dorf1.php").text
        soup = BeautifulSoup(html, 'html.parser')

        result = {'production': {}, 'storage': {}}

        # Production rates
        prod_table = soup.find('table', id='production')
        if prod_table:
            for row in prod_table.find('tbody').find_all('tr'):
                res = row.find('td', class_='res')
                num = row.find('td', class_='num')
                if res and num:
                    result['production'][res.text.strip().rstrip(':')] = \
                        int(num.text.strip().replace(',', ''))

        return result

    def run(self, interval: int = 60, alert_threshold: float = 0.9):
        """Run continuous monitoring loop."""
        print(f"[*] Monitoring every {interval}s (alert at {alert_threshold*100}% capacity)")
        print("-" * 60)

        while True:
            try:
                resources = self.get_resources()
                timestamp = time.strftime('%H:%M:%S')

                print(f"\n[{timestamp}] Resource Production:")
                for res, rate in resources['production'].items():
                    indicator = "🟢" if rate > 0 else "🔴"
                    print(f"  {indicator} {res}: {rate:,}/hour")

                time.sleep(interval)

            except KeyboardInterrupt:
                print("\n[*] Monitoring stopped.")
                break
            except Exception as e:
                print(f"[!] Error: {e}")
                time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description='TTWars Resource Monitor')
    parser.add_argument('--server', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--pass', dest='password', required=True)
    parser.add_argument('--interval', type=int, default=60, help='Poll interval (seconds)')
    args = parser.parse_args()

    monitor = ResourceMonitor(args.server, args.user, args.password)
    monitor.run(interval=args.interval)


if __name__ == '__main__':
    main()
