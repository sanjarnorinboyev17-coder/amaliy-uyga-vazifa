"""3.2 uyga vazifa: konfiguratsiya, CSV va aylanuvchi loglar."""

import csv
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).parent
CONFIG_JSON = BASE_DIR / "config.json"
CONFIG_YAML = BASE_DIR / "config.yaml"
CONVERTED_JSON = BASE_DIR / "config_from_yaml.json"
CONVERTED_YAML = BASE_DIR / "config_from_json.yaml"
SOURCE_CSV = BASE_DIR / "events.csv"
ERROR_CSV = BASE_DIR / "error_events.csv"
ROTATING_LOG = BASE_DIR / "rotating_app.log"
ERROR_REPORT = BASE_DIR / "error_report.txt"


def read_config_and_log(config: dict[str, object]) -> logging.Logger:
	"""Debug yoqilgan bo'lsa, qo'shimcha DEBUG xabarini yozadi."""
	logger = logging.getLogger("homework_3_2")
	logger.setLevel(logging.DEBUG)
	logger.handlers.clear()
	logger.propagate = False

	handler = RotatingFileHandler(
		ROTATING_LOG,
		maxBytes=1_000_000,
		backupCount=3,
		encoding="utf-8",
	)
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
	logger.addHandler(handler)

	logger.info("Konfiguratsiya o'qildi")
	if config.get("debug") is True:
		logger.debug("DEBUG rejimi yoqilgan: qo'shimcha diagnostika xabari")
	logger.error("Namuna ERROR: test xabari")
	return logger


def convert_yaml_to_json() -> dict[str, object]:
	"""YAML konfiguratsiyani o'qib, JSON formatida saqlaydi."""
	with CONFIG_YAML.open("r", encoding="utf-8") as file:
		config = yaml.safe_load(file)
	with CONVERTED_JSON.open("w", encoding="utf-8") as file:
		json.dump(config, file, indent=4)
	return config


def convert_json_to_yaml(config: dict[str, object]) -> None:
	"""JSON konfiguratsiyani YAML formatida saqlaydi."""
	with CONVERTED_YAML.open("w", encoding="utf-8") as file:
		yaml.safe_dump(config, file, allow_unicode=True, sort_keys=False)


def prepare_config_files() -> dict[str, object]:
	"""Konfiguratsiyani o'qiydi va ikki format o'rtasida aylantiradi."""
	if CONFIG_JSON.exists():
		with CONFIG_JSON.open("r", encoding="utf-8") as file:
			config = json.load(file)
	else:
		config = {"env": "development", "port": 8000, "debug": True}
		with CONFIG_JSON.open("w", encoding="utf-8") as file:
			json.dump(config, file, indent=4)

	with CONFIG_YAML.open("w", encoding="utf-8") as file:
		yaml.safe_dump(config, file, allow_unicode=True, sort_keys=False)
	convert_yaml_to_json()
	convert_json_to_yaml(config)
	return config


def prepare_and_filter_csv() -> int:
	"""CSVni qatorma-qator o'qib, statusi error qatorlarni ajratadi."""
	events = [
		{"id": "1", "service": "web", "status": "ok"},
		{"id": "2", "service": "database", "status": "error"},
		{"id": "3", "service": "cache", "status": "ok"},
		{"id": "4", "service": "worker", "status": "error"},
		{"id": "5", "service": "api", "status": "ok"},
	]
	field_names = ["id", "service", "status"]
	with SOURCE_CSV.open("w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=field_names)
		writer.writeheader()
		writer.writerows(events)

	error_count = 0
	with SOURCE_CSV.open("r", newline="", encoding="utf-8") as source_file:
		reader = csv.DictReader(source_file)
		with ERROR_CSV.open("w", newline="", encoding="utf-8") as error_file:
			writer = csv.DictWriter(error_file, fieldnames=field_names)
			writer.writeheader()
			for row in reader:
				if row["status"] == "error":
					writer.writerow(row)
					error_count += 1
	return error_count


def create_error_report() -> list[str]:
	"""Barcha .log fayllardan ERROR qatnashgan satrlarni hisobotga yozadi."""
	error_lines = []
	for log_file in BASE_DIR.glob("*.log"):
		with log_file.open("r", encoding="utf-8", errors="replace") as file:
			for line in file:
				if "ERROR" in line:
					error_lines.append(f"{log_file.name}: {line.rstrip()}")

	with ERROR_REPORT.open("w", encoding="utf-8") as report_file:
		if error_lines:
			report_file.write("\n".join(error_lines) + "\n")
		else:
			report_file.write("ERROR yozuvi topilmadi.\n")
	return error_lines


def main() -> None:
	config = prepare_config_files()
	logger = read_config_and_log(config)
	error_count = prepare_and_filter_csv()
	error_lines = create_error_report()
	logger.info("CSV filtrlash tugadi: %d ta ERROR qator", error_count)
	logger.info("ERROR hisoboti tayyorlandi: %d ta yozuv", len(error_lines))
	print(f"Debug rejimi: {config.get('debug')}")
	print(f"YAML -> JSON va JSON -> YAML konvertatsiyasi bajarildi.")
	print(f"CSVdan {error_count} ta error qator ajratildi.")
	print(f"ERROR hisoboti: {ERROR_REPORT.name}")
	print(f"Rotating log: {ROTATING_LOG.name} (limit: 1 MB)")


if __name__ == "__main__":
	main()
