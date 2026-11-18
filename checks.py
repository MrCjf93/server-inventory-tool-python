"""Check whether an inventory server responds to ping."""

import platform
import subprocess
from datetime import datetime


def ping_server(address):
    """Return True when ping finishes successfully, otherwise False."""
    if platform.system() == "Windows":
        command = ["ping", "-n", "1", address]
    else:
        # Linux and macOS both use -c to set the ping count.
        command = ["ping", "-c", "1", address]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=False,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def check_server(server):
    """Update one server's status and the time it was checked."""
    if ping_server(server["address"]):
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return server["status"]
