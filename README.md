## Biological Assumptions

This tool constructs plasmids intended to replicate in an unknown bacterial host.

Replication capability is ensured by:
- Detecting the chromosomal origin of replication (ORI) of the host genome using GC skew and k-mer enrichment.
- Incorporating the host-derived ORI region (±500 bp) into the plasmid backbone.

This approach is biologically motivated by studies of broad-host-range plasmids, which show that replication can be initiated via host-encoded factors (e.g., DnaA) acting on iteron-rich origins (Jain & Srivastava, 2013).

No host-specific replication proteins are assumed unless explicitly required.
