#!/usr/bin/env python3
"""
Generate a doc-map.json for the OK System.
This script scans the folder structure and outputs a map of all files and directories.
Usage:
    python generate_doc_map.py --output doc-map.json
"""

import os
import json
import argparse


def build_map(root_dir):
    doc_map = {}
    for current_path, dirs, files in os.walk(root_dir):
        rel = os.path.relpath(current_path, root_dir)
        if rel == ".":
            rel = "root"
        doc_map[rel] = {
            "directories": dirs,
            "files": files
        }
    return doc_map


def main():
    parser = argparse.ArgumentParser(description="Generate OK System doc map.")
    parser.add_argument("--root", default=".", help="Root directory to map.")
    parser.add_argument("--output", default="doc-map.json", help="Output JSON file.")
    args = parser.parse_args()

    doc_map = build_map(args.root)

    with open(args.output, "w") as f:
        json.dump(doc_map, f, indent=2)

    print(f"doc map written to {args.output}")


if __name__ == "__main__":
    main()
