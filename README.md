[README Server.md](https://github.com/user-attachments/files/35032964/README.Server.md)
# Server Inventory Tool

This is a small Python program for keeping track of servers. It stores server information in JSON, checks addresses with `ping`, and exports the inventory as a CSV report. I can use it through an interactive text menu or by running commands in a terminal.

The program is written with Python's standard library only. It is intended to work in a terminal in VS Code, in Vim on Linux, or on macOS.

## Requirements

- Python 3.8 or later (check with `python3 --version`)
- A terminal and the system's `ping` command
- No third-party Python packages are required

The program uses `ping -c 1` on Linux and macOS, and `ping -n 1` on Windows. It has a five-second timeout for each address. Some servers block ICMP/ping even when they are running, so `down` means that the ping check failed, not necessarily that the whole server is offline.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Starts the program, reads CLI options with `argparse`, and sets exit codes. |
| `menu.py` | Shows the interactive menu and handles adding, removing, listing, and checking servers. |
| `storage.py` | Loads and saves JSON, reads the data filename, and exports CSV. |
| `checks.py` | Runs ping and updates status and last-check time. |
| `servers.json` | Starting inventory data. |
| `.gitignore` | Ignores Python cache files and generated reports. |
| `EXPLANATION Server inv tool.md` | My explanation of the program's Python constructs and design. |
| `tests/test_inventory.py` | Automated tests for important behaviours. |



## Starting the program

Open a terminal and change into the project directory:

```bash
cd server-inventory-tool
python3 main.py
```

On Linux with Vim, edit a file using `vim main.py`, then run the program from the shell using `python3 main.py`. On macOS, use Terminal or the integrated VS Code terminal. In VS Code, open the project folder and use **Terminal > New Terminal**. If your Python command is `python` instead of `python3`, use `python main.py`.

Without command-line options, a menu appears:

```text
1. Show all servers
2. Show servers by environment
3. Add a server
4. Remove a server
5. Check one server
6. Check all servers
7. Export a CSV report
8. Exit
```

When adding a server, the program keeps asking for an environment until you type `dev`, `test`, or `prod`. New servers start with the status `unknown`. Duplicate names are not accepted. Removing a production server requires typing `yes` as an extra confirmation. Changes to the inventory are saved to JSON.

## Command-line mode

These commands perform an action and then exit:

```bash
python3 main.py --help
python3 main.py --list
python3 main.py --list --environment prod
python3 main.py --check web01
python3 main.py --check-all
python3 main.py --export
```

The environment filter works with `--list` only.

## JSON storage and environment variable

By default, server data is loaded from `servers.json` in the current working directory. The starter file contains four servers. You can tell the program to use a different file by setting `INVENTORY_DATA_FILE` before running it.

On Linux and macOS:

```bash
export INVENTORY_DATA_FILE=my_servers.json
python3 main.py --list
```

Or for a single command:

```bash
INVENTORY_DATA_FILE=my_servers.json python3 main.py --list
```

In Windows PowerShell:

```powershell
$env:INVENTORY_DATA_FILE = "my_servers.json"
python main.py --list
```

If the selected JSON file does not exist, the inventory starts empty. Adding a server will create the file. If the JSON file contains invalid JSON, the program reports an error instead of replacing the data.

Each server is a dictionary in a list. For example:

```json
{
  "name": "dev01",
  "address": "localhost",
  "environment": "dev",
  "role": "utvecklingsserver",
  "status": "unknown",
  "last_checked": ""
}
```

The allowed environments are `dev`, `test`, and `prod`. The allowed statuses are `unknown`, `up`, and `down`. After a check, the last-checked field gets a timestamp such as `2026-11-17 13:15`.

## CSV reports

Choose menu option 7 or run:

```bash
python3 main.py --export
```

The program creates `reports/` automatically. Report names include the date and time. Each report contains a header and one row per server. Reports are not saved in Git because `reports/` is in `.gitignore`.

## Exit codes

- `0`: the command completed successfully.
- `1`: at least one server was `down` after `--check` / `--check-all`, the requested server was missing, or the JSON file could not be loaded.
- `2`: `argparse` rejected invalid command-line arguments.

In a Linux or macOS shell, check the last exit code right after running the command:

```bash
python3 main.py --check dev01
echo $?
```

This is useful in scripts and automation because a script can check the exit code instead of reading the printed text.

## Testing

Automated tests can be run from the project directory:

```bash
python3 -m unittest discover -s tests -v
```

You are able to run tests manually by starting the menu, adding a server in a new JSON file, trying an invalid environment, trying a duplicate name, removing a production server, running the list commands, pinging localhost, and exporting a report.

## Limitations and design decisions

The inventory is meant for a small number of servers as a school project. It is not ment to be a continuous monitoring system. Checks only run one server at a time, so checking many servers may take some time. The menu does not edit an existing server's address or role; it can remove and add servers instead. A failed ping becomes `down` even if the host is online but blocks ping traffic. The JSON and CSV files are plain text; and as a good practice never put passwords or secrets in the inventory.


