#!/usr/bin/env python3
"""
Этап 1. Минимальный прототип:
- читаем CSV
- приводим параметры
- валидируем
- выводим все параметры (требование)
"""

import csv
import argparse
import os
import sys

REQUIRED = {
    "package",
    "repo_url",
    "test_repo_path",
    "test_mode",
    "ascii_tree",
    "max_depth",
    "render_d2"
}

def read_config(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")

    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if len(rows) < 2:
        raise ValueError("CSV должен содержать заголовок + строку значений")

    header, values = rows[0], rows[1]

    if len(header) != len(values):
        raise ValueError("Количество заголовков и значений различается")

    cfg = dict(zip(header, values))

    # гарантируем наличие всех ключей
    for k in REQUIRED:
        cfg.setdefault(k, "")

    return cfg


def validate(cfg):
    out = {}

    # package
    if not cfg["package"].strip():
        raise ValueError("package — обязательный параметр")
    out["package"] = cfg["package"].strip()

    # repo_url
    url = cfg["repo_url"].strip()
    if url and not (url.startswith("http") or os.path.exists(url)):
        raise ValueError("repo_url должен быть URL или существующим файлом")
    out["repo_url"] = url

    # test_repo_path
    out["test_repo_path"] = cfg["test_repo_path"].strip()

    # test_mode
    tm = cfg["test_mode"].lower().strip()
    if tm not in {"yes", "no"}:
        raise ValueError("test_mode должен быть yes/no")
    out["test_mode"] = (tm == "yes")

    # ascii_tree
    at = cfg["ascii_tree"].lower().strip()
    if at not in {"yes", "no"}:
        raise ValueError("ascii_tree должен быть yes/no")
    out["ascii_tree"] = (at == "yes")

    # max_depth
    try:
        md = int(cfg["max_depth"])
        if md < 0:
            raise ValueError()
    except:
        raise ValueError("max_depth должен быть целым >= 0")
    out["max_depth"] = md

    # render_d2
    rd = cfg["render_d2"].lower().strip()
    if rd not in {"yes", "no"}:
        raise ValueError("render_d2 должен быть yes/no")
    out["render_d2"] = (rd == "yes")

    return out


def main():
    parser = argparse.ArgumentParser(description="Этап 1")
    parser.add_argument("--config", "-c", required=True)
    args = parser.parse_args()

    try:
        cfg_raw = read_config(args.config)
        cfg = validate(cfg_raw)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    print("=== Сырые параметры ===")
    for k, v in cfg_raw.items():
        print(f"{k} = {v}")

    print("\n=== Приведённые параметры ===")
    for k, v in cfg.items():
        print(f"{k} = {v}")


if __name__ == "__main__":
    main()
