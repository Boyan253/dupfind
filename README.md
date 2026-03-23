# dupfind

> Find duplicate files by content hash, cheaply: size first, then a partial hash, then a full one.

## Why

Duplicate-finders that hash every byte of every file take all afternoon on a
Downloads folder. `dupfind` only hashes what it has to.
