## Biological Assumptions

This tool constructs plasmids intended to replicate in an unknown bacterial host.

Replication capability is ensured by:
- Detecting the chromosomal origin of replication (ORI) of the host genome using GC skew and k-mer enrichment.
- Incorporating the host-derived ORI region (±500 bp) into the plasmid backbone.

This approach is biologically motivated by studies of broad-host-range plasmids, which show that replication can be initiated via host-encoded factors (e.g., DnaA) acting on iteron-rich origins (Jain & Srivastava, 2013).

No host-specific replication proteins are assumed unless explicitly required.

## Phase 4: Origin of Replication Detection

The origin of replication (ORI) is identified using a combination of:

- GC skew analysis to detect replication asymmetry.
- k-mer enrichment to identify local clustering of replication-initiation motifs.

These two independent signals are combined to reduce false positives.

The ORI detection logic is implemented in `src/ori_finder.py` as a reusable module via the `find_ori()` function.

