from src.utils import parse_design_file, parse_markers_tab, validate_design

def test_design_parsing():
    design = parse_design_file("examples/Design_pUC19.txt")
    markers = parse_markers_tab("data/markers.tab")

    missing = validate_design(design, markers)
    assert isinstance(design, dict)
    assert isinstance(missing, list)
