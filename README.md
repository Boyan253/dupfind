# dupfind

> Find duplicate files by content hash, cheaply: size first, then a partial hash, then a full one.

## Why

Duplicate-finders that hash every byte of every file take all afternoon on a
Downloads folder. `dupfind` only hashes what it has to.

## How it narrows down

1. Group by **file size** — files of different sizes cannot be duplicates.
2. Within each size group, hash the **first 64 KB**.
3. Only for files that still match, hash the **whole file**.

Most files are eliminated in step one, having been read zero times.
