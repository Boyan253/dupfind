#!/usr/bin/env python3
"""Find duplicate files by content, without hashing more than necessary."""

import argparse
import hashlib
import os
import sys

CHUNK = 1 << 20


def file_hash(path, limit=None):
    """Hash a file, or just its first `limit` bytes."""
    digest = hashlib.blake2b(digest_size=16)
    remaining = limit
    with open(path, "rb") as fh:
        while True:
            size = CHUNK if remaining is None else min(CHUNK, remaining)
            if size <= 0:
                break
            block = fh.read(size)
            if not block:
                break
            digest.update(block)
            if remaining is not None:
                remaining -= len(block)
    return digest.hexdigest()


def group_by(items, keyfunc):
    out = {}
    for item in items:
        try:
            out.setdefault(keyfunc(item), []).append(item)
        except OSError:
            continue
    return {k: v for k, v in out.items() if len(v) > 1}


def collect(root, min_bytes=0):
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                if os.path.getsize(path) >= min_bytes and not os.path.islink(path):
                    yield path
            except OSError:
                continue


def find_duplicates(paths, min_bytes=0):
    """Three passes: size, first 64 KB, full hash. Returns list of groups."""
    by_size = group_by(paths, os.path.getsize)
    candidates = [p for group in by_size.values() for p in group]
    by_head = group_by(candidates, lambda p: file_hash(p, 64 * 1024))
    candidates = [p for group in by_head.values() for p in group]
    by_full = group_by(candidates, file_hash)
    return sorted(by_full.values(), key=lambda g: -os.path.getsize(g[0]))


def human(size):
    value = float(size)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024:
            return "%.1f %s" % (value, unit)
        value /= 1024
    return "%.1f TB" % value


def parse_size(text):
    text = text.strip().upper()
    for i, unit in enumerate(["B", "KB", "MB", "GB", "TB"]):
        if unit != "B" and text.endswith(unit):
            return int(float(text[: -len(unit)]) * (1024 ** i))
    return int(float(text.rstrip("B") or 0))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--min", default="1KB", help="ignore files smaller than this")
    ap.add_argument("--delete-extra", action="store_true",
                    help="delete all but the first copy in each group")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --delete-extra, only print what would go")
    args = ap.parse_args(argv)

    paths = list(collect(os.path.abspath(args.path), parse_size(args.min)))
    groups = find_duplicates(paths)
    wasted = 0
    for group in groups:
        size = os.path.getsize(group[0])
        wasted += size * (len(group) - 1)
        print("%s x%d" % (human(size), len(group)))
        for i, path in enumerate(group):
            print("   %s %s" % ("keep" if i == 0 else "dupe", path))
            if i and args.delete_extra:
                if args.dry_run:
                    print("   would delete %s" % path)
                else:
                    os.remove(path)
    print("\n%d group(s), %s reclaimable" % (len(groups), human(wasted)),
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
