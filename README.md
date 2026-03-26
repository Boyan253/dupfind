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

## Usage

```
python dupfind.py ~/Downloads
python dupfind.py D:/Media --min 10MB
python dupfind.py . --delete-extra --dry-run    # see what would go
python dupfind.py . --delete-extra              # actually delete
```

## Output

```
1.2 GB x3
   keep D:/Media/trip.mov
   dupe D:/Media/backup/trip.mov
   dupe D:/Media/old/trip (1).mov

12 group(s), 8.4 GB reclaimable
```

The first file in each group is kept. Always run `--dry-run` first.
