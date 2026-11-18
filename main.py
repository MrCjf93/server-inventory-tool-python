"""Start the text menu or run a command-line inventory operation."""

import argparse
import sys

from checks import check_server
from menu import check_all, find_server, run_menu, show_servers
from storage import export_csv, get_data_file, load_servers, save_servers


def main():
    """Read command-line arguments and perform the requested action."""
    parser = argparse.ArgumentParser(description="Manage and check a server inventory.")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--list", action="store_true", help="List servers")
    actions.add_argument("--check", metavar="NAME", help="Ping one server")
    actions.add_argument("--check-all", action="store_true", help="Ping all servers")
    actions.add_argument("--export", action="store_true", help="Export a CSV report")
    parser.add_argument("--environment", choices=["dev", "test", "prod"], help="Filter --list by environment")
    args = parser.parse_args()

    if args.environment and not args.list:
        parser.error("--environment can only be used with --list")

    data_file = get_data_file()
    try:
        servers = load_servers(data_file)
    except (OSError, ValueError) as error:
        print(f"Could not load the data file: {error}", file=sys.stderr)
        return 1

    if args.list:
        if args.environment:
            servers = [server for server in servers if server["environment"] == args.environment]
        show_servers(servers)
        return 0

    if args.check:
        server = find_server(servers, args.check)
        if server is None:
            print(f"Server '{args.check}' not found.")
            return 1
        status = check_server(server)
        save_servers(servers, data_file)
        print(f'{server["name"]}: {status}')
        return 0 if status == "up" else 1

    if args.check_all:
        check_all(servers, data_file)
        return 1 if any(server["status"] == "down" for server in servers) else 0

    if args.export:
        report_file = export_csv(servers)
        print(f"Report created: {report_file}")
        return 0

    try:
        run_menu(servers, data_file)
    except (EOFError, KeyboardInterrupt):
        print("\nMenu closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
