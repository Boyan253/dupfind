import dupfind


def test_file_hash_matches_for_identical_content(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"same")
    b.write_bytes(b"same")
    assert dupfind.file_hash(str(a)) == dupfind.file_hash(str(b))

def test_file_hash_differs_for_different_content(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"one")
    b.write_bytes(b"two")
    assert dupfind.file_hash(str(a)) != dupfind.file_hash(str(b))


def test_partial_hash_reads_only_the_head(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"head" + b"x" * 100)
    b.write_bytes(b"head" + b"y" * 100)
    assert dupfind.file_hash(str(a), 4) == dupfind.file_hash(str(b), 4)

def test_group_by_drops_singletons():
    assert dupfind.group_by([1, 2, 3], lambda n: n % 2) == {1: [1, 3]}


def test_find_duplicates(tmp_path):
    for name in ("one.txt", "two.txt"):
        (tmp_path / name).write_text("identical", encoding="utf-8")
    (tmp_path / "other.txt").write_text("different", encoding="utf-8")
    groups = dupfind.find_duplicates(list(dupfind.collect(str(tmp_path))))
    assert len(groups) == 1
    assert len(groups[0]) == 2
