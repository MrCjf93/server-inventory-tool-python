# Explanation of the Server Inventory Tool

## 1. Three Python constructions in my code

In `menu.py`, `run_menu()` uses a `while True` loop. That means the menu continues until the user chooses option 8. The `break` statement then ends the loop. The `if` and `elif` conditions choose which function should run based on the user's input.

In `menu.py`, `add_server()` has a `while environment not in VALID_ENVIRONMENTS` loop. This checks whether the text is one of the accepted environments. If it is not, the program prints a message and asks again. I used a loop because a single `if` check would not make the program ask repeatedly.

In `menu.py`, `find_server(servers, name)` is a function that accepts two parameters. It goes through the list using a `for` loop and returns the matching dictionary. If nothing matches, it returns `None`. Other functions can reuse this result rather than writing the search again.

## 2. Why a list of dictionaries?

The list holds all servers, and each dictionary holds the details for one server. This is useful because I'm able to loop through every server or find one by its name. Dictionary keys also make the data easier to understand than a list of values without labels. In `menu.py`, `add_server()` creates each dictionary with the required keys. All six values are strings: the name, address, environment, role, status, and last checked time. The whole inventory is a list containing these dictionaries.

## 3. Why JSON for storage and CSV for reports?

In `storage.py`, `save_servers()` writes the list of dictionaries to JSON and `load_servers()` reads it again. JSON is a good format for keeping the full structure of the inventory between program runs. `export_csv()` writes CSV because it is easy to open in spreadsheet programs and has columns suitable for a report to be read by a human. The JSON file is the program's saved data, while each CSV is an exported snapshot.

## 4. How is the program split into modules?

`main.py` is the starting point. Its `main()` function reads CLI options and decides whether to run one command or open the text menu. `menu.py` has `run_menu()` and functions for adding, removing, finding, showing, and checking servers. `storage.py` handles data files through `load_servers()`, `save_servers()`, and `export_csv()`. `checks.py` has `ping_server()` and `check_server()`, which both menu mode and CLI mode use. This means I do not need separate ping code for each mode.

## 5. Standard-library modules used

In `main.py`, `argparse` reads command-line options, and `sys.exit()` returns an exit code. In `storage.py`, `json` reads and writes inventory data, `csv` writes reports, `os` reads `INVENTORY_DATA_FILE`, `pathlib.Path` works with file paths and directories, and `datetime` creates report timestamps. In `checks.py`, `subprocess.run()` calls the system's `ping` program, `platform` chooses the ping arguments for the operating system, and `datetime` records when a check was performed. All of these are from Python's standard library.

## 6. Three examples of good practice

First, I separated responsibilities between files so `main.py` does not have to contain everything. This makes the project easier to read and change. Second, `find_server()` and `check_server()` are reused, so I do not have duplicate search or ping logic. Third, `add_server()` validates environments and stops duplicate names before saving, which helps keep the inventory consistent. I also avoid storing passwords or API keys in the program.

## 7. Sources and tools used

I used the course's Server Inventory Tool assignment as the main specification. It describes the assignment’s requirements for server data, menu choices, CLI behavior, and file formats. I also used the Python concepts from the course, loops, functions, dictionaries, file handling, and standard-library modules.
W3School was also used for general information along with stack overflow and reddit on some occasions. Youtube was also a good source of information and help I had one channel that I returned to on various occasions when questions came up, Brocode is the name of the channel. AI was also used in some cases to both suggest better solutions and show alternatives. It also helped out a bit regarding structures and explaining things that I was unsure about to gain a deeper understanding and for spell checking to correct minor spelling misstakes and adding the different OS commands for both mac / linux to the readme so that any user is able to try the program. 