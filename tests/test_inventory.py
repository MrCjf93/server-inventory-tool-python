"""Basic tests for the server inventory project."""

import csv
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from checks import check_server, ping_server
from menu import add_server, find_server, remove_server
from storage import export_csv, load_servers


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_folder.cleanup)
        self.data_file = Path(self.temp_folder.name) / "inventory.json"

    def test_missing_file_starts_empty(self):
        self.assertEqual(load_servers(self.data_file), [])

    def test_add_retries_environment_and_saves(self):
        answers = ["new01", "localhost", "wrong", "dev", "web"]
        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            servers = []
            add_server(servers, self.data_file)
        self.assertEqual(len(servers), 1)
        self.assertEqual(servers[0]["status"], "unknown")
        self.assertEqual(load_servers(self.data_file)[0]["environment"], "dev")

    def test_duplicate_name_is_not_added(self):
        servers = [{"name": "existing"}]
        with patch("builtins.input", return_value="existing"), redirect_stdout(io.StringIO()):
            add_server(servers, self.data_file)
        self.assertEqual(len(servers), 1)

    def test_production_remove_needs_confirmation(self):
        servers = [{"name": "db01", "environment": "prod"}]
        with patch("builtins.input", side_effect=["db01", "no"]), redirect_stdout(io.StringIO()):
            remove_server(servers, self.data_file)
        self.assertIsNotNone(find_server(servers, "db01"))
        with patch("builtins.input", side_effect=["db01", "yes"]), redirect_stdout(io.StringIO()):
            remove_server(servers, self.data_file)
        self.assertEqual(servers, [])

    @patch("checks.ping_server", return_value=False)
    def test_check_updates_down_and_time(self, _mock_ping):
        server = {"address": "192.0.2.10", "status": "unknown", "last_checked": ""}
        status = check_server(server)
        self.assertEqual(status, "down")
        self.assertRegex(server["last_checked"], r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

    @patch("checks.platform.system", return_value="Darwin")
    @patch("checks.subprocess.run")
    def test_mac_ping_uses_c(self, mock_run, _mock_system):
        mock_run.return_value.returncode = 0
        self.assertTrue(ping_server("localhost"))
        self.assertEqual(mock_run.call_args.args[0], ["ping", "-c", "1", "localhost"])

    @patch("checks.platform.system", return_value="Windows")
    @patch("checks.subprocess.run")
    def test_windows_ping_uses_n(self, mock_run, _mock_system):
        mock_run.return_value.returncode = 1
        self.assertFalse(ping_server("localhost"))
        self.assertEqual(mock_run.call_args.args[0], ["ping", "-n", "1", "localhost"])

    def test_csv_export_includes_header(self):
        server = {"name": "demo", "address": "localhost", "environment": "dev",
                  "role": "web", "status": "unknown", "last_checked": ""}
        old_folder = Path.cwd()
        try:
            os.chdir(self.temp_folder.name)
            report = export_csv([server])
            with report.open(encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))
        finally:
            os.chdir(old_folder)
        self.assertEqual(rows[0]["name"], "demo")
        self.assertEqual(rows[0]["environment"], "dev")


if __name__ == "__main__":
    unittest.main()
