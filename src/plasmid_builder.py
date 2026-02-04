from src.ori_finder import ori_finder
from src.utils import parse_design_file, parse_markers_tab


def build_plasmid(genome_fasta, design_file, markers_tab):
    # Load genome sequence
    with open(genome_fasta) as f:
        genome = "".join(
            line.strip() for line in f if not line.startswith(">")
        )

    # Find ORI
    ori_data = ori_finder(genome_fasta)

    # Handle ORI edge case
    if ori_data.get("ori_positions"):
        ori_pos = ori_data["ori_positions"][0]
        ORI_WINDOW = 500
        start = max(0, ori_pos - ORI_WINDOW)
        end = min(len(genome), ori_pos + ORI_WINDOW)
        ori_seq = genome[start:end]
    else:
        ori_seq = genome  # safe fallback

    design = parse_design_file(design_file)
    markers = parse_markers_tab(markers_tab)

    plasmid_seq = ori_seq

    # ----------------------------
    # Add antibiotic markers
    # ----------------------------
    for ab in design.get("antibiotic_markers", []):
        marker_name = ab.get("marker")
        if marker_name in markers:
            plasmid_seq += markers[marker_name]
        else:
            # Gracefully skip missing marker
            continue

    # ----------------------------
    # Add MCS / restriction sites
    # ----------------------------
    for mcs in design.get("mcs", []):
        enzyme = mcs.get("enzyme")
        if enzyme in markers:
            plasmid_seq += markers[enzyme]
        else:
            continue

    return plasmid_seq






if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Usage: python -m src.plasmid_builder <genome.fa> <design.txt> <markers.tab> <output.fa>")
        sys.exit(1)

    genome_fasta = sys.argv[1]
    design_file = sys.argv[2]
    markers_tab = sys.argv[3]
    output_fasta = sys.argv[4]

    plasmid_seq = build_plasmid(genome_fasta, design_file, markers_tab)

    with open(output_fasta, "w") as f:
        f.write(">Designed_Plasmid\n")
        for i in range(0, len(plasmid_seq), 60):
            f.write(plasmid_seq[i:i+60] + "\n")

    print(f"Plasmid written to {output_fasta}")
