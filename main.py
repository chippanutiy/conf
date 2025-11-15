#!/usr/bin/env python3
"""
Этап 2:
- читаем конфиг
- скачиваем Packages или читаем локальный
- извлекаем поле Depends
- печатаем прямые зависимости
"""

import argparse
import csv
import gzip
import io
import os
import sys
import urllib.request


def read_config(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return dict(zip(rows[0], rows[1]))


def fetch_packages(url):
    if url.startswith("http"):
        data = urllib.request.urlopen(url).read()
    else:
        data = open(url, "rb").read()

    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        return gzip.decompress(data).decode("utf-8", errors="replace")
    return data.decode("utf-8", errors="replace")


def parse_packages(text):
    res = {}
    blocks = text.split("\n\n")

    for block in blocks:
        pkg = None
        deps = []

        for line in block.splitlines():
            if line.startswith("Package:"):
                pkg = line.split(":", 1)[1].strip()

            if line.startswith("Depends:"):
                raw = line.split(":", 1)[1]
                tokens = []
                for part in raw.replace(",", " ").split():
                    if part == "|":
                        continue
                    tokens.append(part.split("(")[0])
                deps = tokens

        if pkg:
            res[pkg] = deps

    return res


def main():
    parser = argparse.ArgumentParser(description="Этап 2")
    parser.add_argument("--config", "-c", required=True)
    args = parser.parse_args()

    cfg = read_config(args.config)
    package = cfg["package"]
    url = cfg["repo_url"]

    if not url:
        print("[ERROR] repo_url не указан", file=sys.stderr)
        sys.exit(1)

    text = fetch_packages(url)
    mapping = parse_packages(text)

    deps = mapping.get(package, [])
    print(f"Прямые зависимости пакета {package}: {deps}")


if __name__ == "__main__":
    main()
