import os
import shutil

def copy_recursive(target_dir, public_path):
    for child in os.listdir(target_dir):
        from_path = os.path.join(target_dir, child)
        dest_path = os.path.join(public_path, child)

        if os.path.isdir(from_path):
            print("[copy_recursive] detected a dir, calling function for: ", from_path)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            copy_recursive(from_path, dest_path)
        else:
            print("[copy_recursive] detected a file, copying this: ", from_path)
            shutil.copy(from_path, dest_path)