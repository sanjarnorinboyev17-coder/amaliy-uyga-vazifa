"""3.1 amaliy vazifa: fayl, JSON, YAML, CSV va logging bilan ishlash."""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "log.txt"
CONFIG_FILE = BASE_DIR / "config.json"
SERVERS_FILE = BASE_DIR / "servers.yaml"
EMPLOYEES_FILE = BASE_DIR / "employees.csv"
SCRIPT_LOG_FILE = BASE_DIR / "script.log"


def append_log_lines() -> None:
	"""Matnli log fayliga append rejimida beshta qator qo'shadi."""
	with LOG_FILE.open("a", encoding="utf-8") as file:
		for event_number in range(1, 6):
			timestamp = datetime.now().isoformat(timespec="seconds")
			file.write(f"{timestamp} - hodisa {event_number}: skript ishladi\n")


def write_and_read_config() -> dict[str, object]:
	"""JSON konfiguratsiyani yozadi va qayta o'qiydi."""
	config = {
		"env": "development",
		"port": 8000,
		"debug": True,
	}
	with CONFIG_FILE.open("w", encoding="utf-8") as file:
		json.dump(config, file, indent=4)

	with CONFIG_FILE.open("r", encoding="utf-8") as file:
		loaded_config = json.load(file)
	print(f"JSON konfiguratsiya: {loaded_config}")
	return loaded_config


def write_and_read_servers() -> list[dict[str, str]]:
	"""Serverlar ro'yxatini YAML formatida yozadi va PyYAML bilan o'qiydi."""
	servers = [
		{"name": "web-server", "ip": "192.168.1.10", "status": "up"},
		{"name": "database-server", "ip": "192.168.1.20", "status": "up"},
		{"name": "backup-server", "ip": "192.168.1.30", "status": "down"},
	]
	with SERVERS_FILE.open("w", encoding="utf-8") as file:
		yaml.safe_dump(servers, file, allow_unicode=True, sort_keys=False)

	with SERVERS_FILE.open("r", encoding="utf-8") as file:
		loaded_servers = yaml.safe_load(file)
	print("YAML serverlar:")
	for server in loaded_servers:
		print(f"- {server['name']}: {server['ip']} ({server['status']})")
	return loaded_servers


def write_and_read_employees() -> list[dict[str, str]]:
	"""Xodimlarni CSVga yozadi va jadval ko'rinishida chop etadi."""
	employees = [
		{"id": "1", "name": "Sanjar", "role": "DevOps", "salary": "800"},
		{"id": "2", "name": "Ali", "role": "Backend", "salary": "750"},
		{"id": "3", "name": "Madina", "role": "QA", "salary": "700"},
		{"id": "4", "name": "Jasur", "role": "Frontend", "salary": "720"},
	]
	field_names = ["id", "name", "role", "salary"]
	with EMPLOYEES_FILE.open("w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=field_names)
		writer.writeheader()
		writer.writerows(employees)

	with EMPLOYEES_FILE.open("r", newline="", encoding="utf-8") as file:
		loaded_employees = list(csv.DictReader(file))

	print("Xodimlar jadvali:")
	print(f"{'ID':<4}{'Ism':<12}{'Lavozim':<12}{'Maosh':<8}")
	print("-" * 36)
	for employee in loaded_employees:
		print(
			f"{employee['id']:<4}{employee['name']:<12}"
			f"{employee['role']:<12}{employee['salary']:<8}"
		)
	return loaded_employees


def main() -> None:
	logging.basicConfig(
		filename=SCRIPT_LOG_FILE,
		level=logging.INFO,
		format="%(asctime)s %(levelname)s %(message)s",
	)
	logging.info("Skript boshlandi")
	try:
		append_log_lines()
		write_and_read_config()
		write_and_read_servers()
		write_and_read_employees()
		logging.info("Skript muvaffaqiyatli tugadi")
	except Exception:
		logging.exception("Skript davomida xatolik yuz berdi")
		raise


if __name__ == "__main__":
	main()
