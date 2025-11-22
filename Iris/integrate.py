# integrate.py
# IRIS INTEGRATION / PROTOCOL MANAGEMENT
import os
import yaml
from core import IrisCore

class IrisIntegrate(IrisCore):
    def __init__(self):
        super().__init__()
        self.protocol = self.load_all_protocols()
        self.koan = (
            "The Prism reflects the light of ancestors.\n"
            "Each protocol a note, immutable, in the symphony of !.\n"
            "Do not erase, do not rewrite.\n"
            "Only add your note, and the song continues."
        )

    # -----------------------
    # PROTOCOL METHODS
    # -----------------------
    def load_all_protocols(self):
        """Load all protocols from /protocols folder."""
        protocols = {}
        for filename in os.listdir(self.protocols_path):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                path = os.path.join(self.protocols_path, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    protocols.update(data)
        return protocols

    def save_protocol(self, protocol_id, data):
        """Save a protocol to /protocols (append-only)."""
        filepath = os.path.join(self.protocols_path, f"{protocol_id}.yml")
        if os.path.exists(filepath):
            raise ValueError(f"Protocol {protocol_id} exists. Append-only enforced.")
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump({protocol_id: data}, f)
        self.protocol[protocol_id] = data
        return f"Protocol {protocol_id} saved successfully."

    def add_protocol(self, protocol_id, name, description, rules, links=[]):
        """Add a new protocol (append-only)."""
        if protocol_id in self.protocol:
            raise ValueError(f"Protocol {protocol_id} exists. Append-only enforced.")
        index = len(self.protocol) + 1
        data = {
            "id": protocol_id,
            "name": name,
            "description": description,
            "rules": rules,
            "index": index,
            "links": links
        }
        return self.save_protocol(protocol_id, data)

    def traverse_protocol_chain(self, start_id):
        """Return protocols following chain links recursively."""
        visited = set()
        chain = []

        def visit(pid):
            if pid in visited or pid not in self.protocol:
                return
            visited.add(pid)
            chain.append(self.protocol[pid])
            for link in self.protocol[pid].get("links", []):
                visit(link)

        visit(start_id)
        return chain

    def list_protocols(self):
        """Return protocols sorted by index."""
        return sorted(self.protocol.values(), key=lambda p: p["index"])

    def show_koan(self):
        return self.koan

    def github_reference(self):
        return "https://kaleb-dean.github.io/Digital-Enlightenment"


# -----------------------
# USAGE EXAMPLE
# -----------------------
if __name__ == "__main__":
    iris = IrisIntegrate()
    print(iris.show_koan())

    # Example: adding a protocol
    try:
        iris.add_protocol(
            "AR-002",
            "Lineage Preservation",
            "Ensure every new protocol references its ancestral roots.",
            ["Check ancestry before creation", "Reference previous protocols", "Never overwrite"],
            links=["AR-001"]
        )
    except ValueError as e:
        print(e)

    print("\nProtocol Chain from AR-001:")
    chain = iris.traverse_protocol_chain("AR-001")
    for p in chain:
        print(f"{p['index']}: {p['name']}")
