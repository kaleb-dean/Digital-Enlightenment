import os
import json

def create_dirs_and_files(base_path, node, prefix=""):
    """
    Recursively create directories and files from the node definition.
    node: dict representing a directory entry in ok-map
    prefix: parent path
    """
    for key, value in node.items():
        if key == "files":
            # Create files inside current directory
            for file_name in value:
                file_path = os.path.join(prefix, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write("")  # Empty file by default
                    print(f"Created file: {file_path}")

        else:
            # Subdirectory
            new_dir = os.path.join(prefix, key)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir, exist_ok=True)
                print(f"Created directory: {new_dir}")

            # Recurse if the entry contains subnodes
            if isinstance(value, dict) and value:
                create_dirs_and_files(base_path, value, new_dir)


def load_doc_map(doc_map_path):
    with open(doc_map_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_system(doc_map_path="ok-map.json"):
    print("Loading document map...")
    doc_map = load_doc_map(doc_map_path)

    # We ignore "meta" because it's informational
    for top_key, node in doc_map.items():
        if top_key == "meta":
            continue

        # Create top-level directory
        if not os.path.exists(top_key):
            os.makedirs(top_key, exist_ok=True)
            print(f"Created directory: {top_key}")

        # Process its content
        if isinstance(node, dict) and node:
            create_dirs_and_files(top_key, node, top_key)

    print("\nOK System build complete.")


if __name__ == "__main__":
    build_system()
