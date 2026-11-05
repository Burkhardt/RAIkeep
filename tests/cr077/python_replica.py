"""Independent Python process for CR077 configured-cloud parity acceptance."""
import json
from pathlib import Path
import sys
from jsonpit import Pit, MutationTrackingMode

root = Path(sys.argv[1])
mode = MutationTrackingMode[sys.argv[2]]
operation = sys.argv[3]
pit = Pit(root, root.name, read_only=False, autoload=True, unflagged=True, tracking_mode=mode)
try:
	item = pit["Ego"]
	if operation == "rename":
		item["Name"] = "RemoteRename"
		del item["Namespace"]
		count = len(pit.historic_items["Ego"].history)
		assert pit.add(item) is False
		assert len(pit.historic_items["Ego"].history) == count
		pit.save(force=True)
	print(json.dumps({"Name": item["Name"], "Status": item.get("Status"), "NamespacePresent": "Namespace" in item,
		"HistoryKeys": [sorted(fragment.keys()) for fragment in pit.historic_items["Ego"].history]}))
finally:
	pit.close()
