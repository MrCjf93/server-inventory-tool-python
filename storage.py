"""Read and write the server inventory and export CSV reports."""

import csv
import json
import os
from datetime import datetime
from pathlib import Path


FIELDS = ["name", "address", "environment", "role", "status", "last_checked"]


def get_data_file():
    """Get the JSON filename from an environment variable, if set."""
    filename = os.environ.get("INVENTORY_DATA_FILE", "servers.json")
    return Path(filename)


def load_servers(data_file):
    """Load the list of servers, or return an empty list for a missing file."""
    if not data_file.exists():
        return []

    with data_file.open("r", encoding="utf-8") as file:
        servers = json.load(file)

    if not isinstance(servers, list):
        raise ValueError("The JSON data file must contain a list of servers.")

    return servers


def save_servers(servers, data_file):
    """Save the current server list to JSON."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with data_file.open("w", encoding="utf-8") as file:
        json.dump(servers, file, indent=2, ensure_ascii=False)


def export_csv(servers):
    """Write a dated CSV report in the reports folder."""
    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
    report_file = reports_folder / f"inventory_{timestamp}.csv"

    with report_file.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(servers)

    return report_file
