#to parse design file
def parse_design_file(path):
    mcs = []
    antibiotics = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            left, right = [x.strip() for x in line.split(",")]

            if "Cloning" in left:
                mcs.append({"site": left, "enzyme": right})
            else:
                antibiotics.append({"marker": left, "name": right})

    return {
        "mcs": mcs,
        "antibiotic_markers": antibiotics
    }

#to parse markers file
def parse_markers_tab(path):
    markers = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            name = parts[0]
            seq = parts[-1]
            markers[name] = seq.upper()

    return markers
    
#to validate
def validate_design(design, marker_db):
    missing = []

    for m in design["mcs"]:
        if m["enzyme"] not in marker_db:
            missing.append(m["enzyme"])

    for a in design["antibiotic_markers"]:
        if a["marker"] not in marker_db:
            missing.append(a["marker"])

    return missing