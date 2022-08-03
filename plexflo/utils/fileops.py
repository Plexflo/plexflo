from pathlib import Path


def remove_path(path: Path):
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    for p in path.iterdir():
        remove_path(p)
    path.rmdir()
