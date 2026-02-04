from src.plasmid_builder import build_plasmid

def test_plasmid_builds():
    plasmid = build_plasmid(
        "examples/pUC19.fa",
        "examples/Design_pUC19.txt",
        "data/markers.tab"
    )

    assert isinstance(plasmid, str)
    assert len(plasmid) > 1000
