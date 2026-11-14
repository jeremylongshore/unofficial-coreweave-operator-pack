"""Pack distribution must not silently accept missing or escaping local references."""

import importlib.util
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cw_pack_gate", ROOT / "tools/validate-pack.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def test_installed_reference_must_exist(tmp_path):
    (tmp_path / "SKILL.md").write_text("[procedure](references/missing.md)")
    assert gate.links(tmp_path) == ["SKILL.md: references/missing.md"]


def test_reference_cannot_escape_via_symlink(tmp_path):
    root = tmp_path / "skill"
    root.mkdir()
    outside = tmp_path / "private.md"
    outside.write_text("private")
    (root / "leak.md").symlink_to(outside)
    (root / "SKILL.md").write_text("[procedure](leak.md)")
    assert gate.links(root) == ["SKILL.md: leak.md"]


def test_valid_local_anchor_and_external_reference(tmp_path):
    (tmp_path / "notes.md").write_text("# Notes\n")
    (tmp_path / "SKILL.md").write_text("[notes](notes.md#notes) [reference](https://example.invalid/reference)")
    assert gate.links(tmp_path) == []


def test_secret_snapshot_includes_new_and_modified_files_but_not_ignored_cache(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(".cache/\nprivate-corpus/\n")
    (root / "tracked.txt").write_text("original")
    (root / "deleted.txt").write_text("deleted")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    (root / "tracked.txt").write_text("uncommitted edit")
    (root / "deleted.txt").unlink()
    (root / "new.txt").write_text("new file")
    for directory in (".cache", "private-corpus"):
        (root / directory).mkdir()
        (root / directory / "ignored.txt").write_text("must not be copied")
    target = tmp_path / "snapshot"
    target.mkdir()
    gate.snapshot_worktree(root, target)
    assert sorted(p.name for p in target.iterdir()) == [".gitignore", "new.txt", "tracked.txt"]
    assert (target / "tracked.txt").read_text() == "uncommitted edit"


@pytest.mark.parametrize("parent_link", [False, True])
def test_secret_snapshot_refuses_symlinks(tmp_path, parent_link):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("private")
    if parent_link:
        (root / "linked").mkdir()
        (root / "linked" / "secret.txt").write_text("tracked")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        (root / "linked" / "secret.txt").unlink()
        (root / "linked").rmdir()
        (root / "linked").symlink_to(outside, target_is_directory=True)
    else:
        (root / "linked").symlink_to(outside / "secret.txt")
    target = tmp_path / "snapshot"
    target.mkdir()
    with pytest.raises(ValueError, match="refuses symlink"):
        gate.snapshot_worktree(root, target)
    assert not list(target.iterdir())
