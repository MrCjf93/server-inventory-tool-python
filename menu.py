"""Interactive text menu and inventory helper functions."""

from checks import check_server
from storage import export_csv, save_servers


VALID_ENVIRONMENTS = ["dev", "test", "prod"]


def find_server(servers, name):
    """Find a server by name, or return None when it is not found."""
    for server in servers:
        if server["name"] == name:
            return server
    return None


def show_servers(servers):
    """Print a table with aligned columns."""
    if not servers:
        print("No servers to show.")
        return

    print(f'{"Name":<15} {"Address":<22} {"Environment":<13} '
          f'{"Role":<20} {"Status":<9} {"Last checked":<16}')
    print("-" * 100)
    for server in servers:
        print(f'{server["name"]:<15} {server["address"]:<22} '
              f'{server["environment"]:<13} {server["role"]:<20} '
              f'{server["status"]:<9} {server["last_checked"]:<16}')


def show_environment(servers):
    """Ask for an environment and show its servers."""
    environment = input("Environment (dev/test/prod): ").strip().lower()
    if environment not in VALID_ENVIRONMENTS:
        print("Invalid environment. Choose dev, test or prod.")
        return

    matches = [server for server in servers if server["environment"] == environment]
    show_servers(matches)


def add_server(servers, data_file):
    """Ask for server details and add a new server."""
    name = input("Server name: ").strip()
    if not name:
        print("Server name cannot be empty.")
        return
    if find_server(servers, name) is not None:
        print("A server with that name already exists.")
        return

    address = input("Address (hostname or IP): ").strip()
    if not address:
        print("Address cannot be empty.")
        return

    environment = ""
    while environment not in VALID_ENVIRONMENTS:
        environment = input("Environment (dev/test/prod): ").strip().lower()
        if environment not in VALID_ENVIRONMENTS:
            print("Invalid environment. Please try again.")

    role = input("Role: ").strip()
    new_server = {
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": "",
    }
    servers.append(new_server)
    save_servers(servers, data_file)
    print(f"Server '{name}' added.")


def remove_server(servers, data_file):
    """Remove a server, with an extra confirmation for production."""
    name = input("Server name to remove: ").strip()
    server = find_server(servers, name)
    if server is None:
        print("Server not found.")
        return

    if server["environment"] == "prod":
        answer = input("This is a production server. Type yes to remove it: ")
        if answer.strip().lower() != "yes":
            print("Removal cancelled.")
            return

    servers.remove(server)
    save_servers(servers, data_file)
    print(f"Server '{name}' removed.")


def check_one(servers, data_file):
    """Ask for a server name, check it, and save the result."""
    name = input("Server name to check: ").strip()
    server = find_server(servers, name)
    if server is None:
        print("Server not found.")
        return

    status = check_server(server)
    save_servers(servers, data_file)
    print(f"{name}: {status}")


def check_all(servers, data_file):
    """Check every server and save all results."""
    for server in servers:
        status = check_server(server)
        print(f'{server["name"]}: {status}')
    save_servers(servers, data_file)


def run_menu(servers, data_file):
    """Keep displaying the menu until the user chooses Exit."""
    while True:
        print("\n=== Server Inventory Tool ===")
        print("1. Show all servers")
        print("2. Show servers by environment")
        print("3. Add a server")
        print("4. Remove a server")
        print("5. Check one server")
        print("6. Check all servers")
        print("7. Export a CSV report")
        print("8. Exit")

        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            show_servers(servers)
        elif choice == "2":
            show_environment(servers)
        elif choice == "3":
            add_server(servers, data_file)
        elif choice == "4":
            remove_server(servers, data_file)
        elif choice == "5":
            check_one(servers, data_file)
        elif choice == "6":
            check_all(servers, data_file)
        elif choice == "7":
            report_file = export_csv(servers)
            print(f"Report created: {report_file}")
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")
