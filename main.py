#!/usr/bin/env python3
"""
Этап 3:
- тестовый режим (заглавные буквы) или реальный APT
- BFS с рекурсией
- ограничение глубины
- обработка циклов
"""

import argparse
import csv
import os
import sys
import gzip
import io
import urllib.request


def read_config(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return dict(zip(rows[0], rows[1]))


def parse_test_repo(path):
    graph = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        name, deps = line.split(":", 1)
        deps = [d.strip() for d in deps.replace(",", " ").split()]
        graph[name.strip()] = deps
    return graph


def fetch_packages(url):
    data = urllib.request.urlopen(url).read()
    if url.endswith(".gz"):
        data = gzip.decompress(data)
    return data.decode("utf-8", errors="replace")


def parse_packages(txt):
    res = {}
    blocks = txt.split("\n\n")
    for b in blocks:
        pkg = None
        deps = []
        for line in b.splitlines():
            if line.startswith("Package:"):
                pkg = line.split(":", 1)[1].strip()
            if line.startswith("Depends:"):
                raw = line.split(":", 1)[1]
                parts = []
                for p in raw.replace(",", " ").split():
                    if p == "|":
                        continue
                    parts.append(p.split("(")[0])
                deps = parts
        if pkg:
            res[pkg] = deps
    return res


def build_bfs(start, direct, max_depth):
    visited = set()
    result = {}

    def rec(level_nodes, depth):
        if depth > max_depth:
            return

        next_nodes = []
        for node in level_nodes:
            if node in visited:
                continue
            visited.add(node)

            deps = direct.get(node, [])
            result[node] = deps

            for d in deps:
                if d not in visited:
                    next_nodes.append(d)

        if next_nodes:
            rec(next_nodes, depth + 1)

    rec([start], 0)
    return result


def main():
    parser = argparse.ArgumentParser(description="Этап 3")
    parser.add_argument("--config", "-c", required=True)
    args = parser.parse_args()

    cfg = read_config(args.config)

    package = cfg["package"]
    max_depth = int(cfg["max_depth"])
    test_mode = cfg["test_mode"].lower() == "yes"

    if test_mode:
        direct = parse_test_repo(cfg["test_repo_path"])
    else:
        txt = fetch_packages(cfg["repo_url"])
        direct = parse_packages(txt)

    graph = build_bfs(package, direct, max_depth)

    print("Граф зависимостей:")
    for k, v in graph.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
