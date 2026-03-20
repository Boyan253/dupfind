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
