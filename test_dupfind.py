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
