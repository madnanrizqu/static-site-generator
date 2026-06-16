import os
import shutil
import sys
from pathlib import Path
from copystatic import copy_recursive

def main():
    root_path = find_project_root()
    public_path = os.path.join(root_path, 'public')
    static_path = os.path.join(root_path, 'static')

    if not os.path.exists(public_path):
        print("public_path does not exist:", public_path)
        sys.exit(1)
    if not os.path.exists(static_path):
        print("static_path does not exist:", static_path)
        sys.exit(2)
    if not os.path.isdir(public_path):
        print("public_path is not a dir:", public_path)
        sys.exit(3)
    if not os.path.isdir(static_path):
        print("static_path is not a dir:", static_path)
        sys.exit(4)

    shutil.rmtree(public_path)
    os.mkdir(public_path)

    try:
        copy_recursive(static_path, public_path)
    except Exception as e:
        print("Error copying to public:", e)
        sys.exit(5)

def find_project_root(marker=".git"):
    current_path = Path(__file__).resolve()
    for parent in [current_path, *current_path.parents]:
        if (Path(os.path.join(parent, marker))).exists():
            return parent
    return current_path.parent


if __name__ == "__main__":
    main()
