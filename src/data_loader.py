from pathlib import Path

def parse_ann(ann_path):
    """Read one BRAT .ann file -> list of entity dicts"""
    entities = []
    ann_path = Path(ann_path)
    if not ann_path.exists():
        return entities

    with open(ann_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith('T'):
                continue  # Skip relations/attributes

            parts = line.split('\t')
            if len(parts) < 3:
                continue

            ent_id = parts[0]
            info = parts[1]
            text = parts[2]

            info_parts = info.split(' ', 1)
            label = info_parts[0]
            raw_spans = info_parts[1]

            spans = []
            for segment in raw_spans.split(';'):
                coords = segment.strip().split()
                if len(coords) == 2:
                    spans.append((int(coords[0]), int(coords[1])))

            if spans:
                entities.append({
                    "id": ent_id,
                    "label": label,
                    "spans": spans,
                    "text": text
                })

    return entities

def load_document(txt_path):
    """One .txt + its matching .ann -> one document dict."""
    txt_path = Path(txt_path)
    return {
        "id": txt_path.stem,
        # newline="" keeps \r\n exactly as-is so character offsets stay aligned
        "text": open(txt_path, encoding="utf-8", newline="").read(),
        "entities": parse_ann(txt_path.with_suffix(".ann")),
    }

def load_corpus(folder):
    """Load every .txt/.ann pair in a folder."""
    return [load_document(t) for t in sorted(Path(folder).glob("*.txt"))
            if t.with_suffix(".ann").exists()]
