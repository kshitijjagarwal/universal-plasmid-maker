## Biological Assumptions

This tool constructs plasmids intended to replicate in an unknown bacterial host.

Replication capability is ensured by:
- Detecting the chromosomal origin of replication (ORI) of the host genome using GC skew and k-mer enrichment.
- Incorporating the host-derived ORI region (±500 bp) into the plasmid backbone.

This approach is biologically motivated by studies of broad-host-range plasmids, which show that replication can be initiated via host-encoded factors (e.g., DnaA) acting on iteron-rich origins (Jain & Srivastava, 2013).

No host-specific replication proteins are assumed unless explicitly required.


# Universal Plasmid Maker

## Overview
## Problem Statement
## Approach
  - Rejected ORI Identification Methods
  - Final ORI Identification Method
  - GC Skew and Replication Asymmetry
## Plasmid Construction Pipeline
## EcoRI Deletion Logic
## How to Run
## Testing
## Notes and Assumptions


# Universal Plasmid Maker

This project implements a universal plasmid construction pipeline for an unknown organism.
Given a genome sequence, the tool identifies the origin of replication (ORI), constructs a
functional plasmid using a user-defined design file, and removes unwanted restriction sites
to ensure cloning safety.

Given the genome sequence of an unknown organism, the objective is to:

1. Identify the origin of replication (ORI) using computational methods.
2. Use the identified ORI to construct a plasmid that can replicate in the host organism.
3. Assemble the plasmid using a user-provided design specification.
4. Remove unwanted restriction sites (e.g., EcoRI) from the final plasmid sequence.

### Rejected ORI Identification Methods

Several naïve approaches for ORI identification were evaluated and rejected:

1. **Maximum AT-content method**  
   Regions with high AT content were initially considered as ORI candidates.
   However, many non-ORI intergenic regions also exhibit high AT content, leading
   to false positives.

2. **Fixed motif search (e.g., DnaA boxes only)**  
   Searching for known ORI motifs alone is unreliable across species, as motif
   sequences and distributions vary significantly between organisms.

3. **Single-window nucleotide skew analysis**  
   Using skew within a single window is highly sensitive to noise and local sequence
   composition, producing inconsistent ORI predictions.

These approaches fail to generalize to real genomic data and are unsuitable for
robust ORI detection.

### Final ORI Identification Method

The final method uses cumulative GC skew analysis across the genome.
GC skew is defined as:

GC_skew = (G − C) / (G + C)

The cumulative GC skew curve exhibits characteristic inflection points at the origin
and terminus of replication due to replication asymmetry between the leading and lagging
strands.

The ORI is identified as the global minimum of the cumulative GC skew curve.
This method is robust, species-agnostic, and supported by biological evidence.

### GC Skew and Replication Asymmetry

During DNA replication, the leading and lagging strands are synthesized differently,
resulting in asymmetric nucleotide incorporation. Over evolutionary time, this leads
to strand-specific biases in guanine (G) and cytosine (C) distribution.

By computing cumulative GC skew across the genome, these biases accumulate and reveal
clear transitions at replication origins. This biological asymmetry forms the basis
for reliable ORI identification.

### Plasmid Construction Pipeline

1. Parse the input genome FASTA file.
2. Identify the ORI using cumulative GC skew analysis.
3. Extract an ORI-centered sequence window (or fallback to full sequence).
4. Parse the plasmid design file and markers database.
5. Assemble the plasmid by appending:
   - ORI sequence
   - Antibiotic resistance markers
   - Multiple cloning site (MCS) elements

### EcoRI Deletion Logic

EcoRI is a restriction enzyme that recognizes the sequence GAATTC.
If present in the final plasmid, it may cause unintended cleavage during cloning.

To ensure cloning safety, all EcoRI recognition sites were removed from the final
plasmid sequence after full assembly. Both forward (GAATTC) and reverse-complement
(CTTAAG) motifs were eliminated to guarantee complete removal.

### How to Run

```bash
python -m src.plasmid_builder \
  examples/pUC19.fa \
  examples/Design_pUC19.txt \
  data/markers.tab \
  outputs/Output.fa


---

## 🧪 9. Testing

```markdown
### Testing

Unit tests are provided using pytest to validate:
- ORI detection
- Design file parsing
- Plasmid construction correctness

Run tests using:

```bash
pytest


---

## 🧠 10. Notes and Assumptions

```markdown
### Notes and Assumptions

- ORI detection is optimized for chromosomal genomes; plasmid inputs may use fallback logic.
- Missing markers or enzymes in the markers database are skipped gracefully.
- EcoRI removal is applied as a final sanitization step.
