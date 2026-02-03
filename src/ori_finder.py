import sys
from collections import Counter
from Bio import SeqIO
import numpy as np
from scipy.signal import find_peaks

WINDOW_GC = 500
KMER = 8
WINDOW_ENRICH = 5000
TOTAL_DIST = 10000

def gc_skew(sequence, window):
    sk = []
    for i in range(0, len(sequence) - window + 1, window):
        chunk = sequence[i:i+window]
        g = chunk.count("G")
        c = chunk.count("C")
        if (g + c):
            sk.append((g-c)/(g + c))
        else:
            sk.append(0)
    return np.array(sk)

def kmer_count(sequence, k):
    ans = Counter()
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        #Increment the count for the found kmer
        ans[kmer] += 1
    return ans

def enrichment_profile(seq, bg_freq, k, window):
    scores = []
    for  i in range(0, len(seq) - window + 1, window):
        chunk = seq[i:i+window]
        local_count = kmer_count(chunk, k)
        w_total = sum(local_count.values())
        score = 0
        for mer, cnt in local_count.items():
            if mer in bg_freq and bg_freq[mer] > 0:
                score += (cnt/w_total) / bg_freq[mer]
        scores.append(score)
    return np.array(scores)


def ori_finder(genome_fasta): #it will identify ori using both GC skey and k mer enrichment, then return a dictionary with ORI positions and data
    record = next(SeqIO.parse(genome_fasta, "fasta"))
    seq=str(record.seq).upper()

    #Calculation for GC skew
    skew = gc_skew(seq, WINDOW_GC)

    #Background kmer freq
    bg_counts = kmer_count(seq, KMER)
    bg_total = sum(bg_counts.values())
    bg_freq = {}
    for k_mer, count in bg_counts.items():
        bg_freq[k_mer] = count / bg_total

    #Local enrichment
    enrichment = enrichment_profile(seq, bg_freq, KMER, WINDOW_ENRICH)

    #Peak detection
    peaks = find_peaks(enrichment, prominence=1)[0]

    #GC sign flip detection
    sign_change = np.where(np.diff(np.sign(skew)) != 0)[0]

    #ORI candidates
    ori_positions = set()
    for p  in peaks:
        coord = p*WINDOW_ENRICH
        if any(abs(coord - sc*WINDOW_GC) < TOTAL_DIST for sc in sign_change):
            ori_positions.add(coord)

    return  {
        "ori_positions": sorted(ori_positions),
        "gc_skew": skew,
        "enrichment": enrichment
        }