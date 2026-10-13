from Bio.Align import PairwiseAligner

aligner = PairwiseAligner()
aligner.mode = "global"
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -5
aligner.extend_gap_score = -0.5

def sequence_identity(seq1, seq2):
    alignment = aligner.align(seq1, seq2)[0]

    aligned1, aligned2 = str(alignment).splitlines()[-2:]

    coordinates = alignment.coordinates
    matches = 0
    columns = 0

    for i in range(len(coordinates[0]) - 1):
        start1, end1 = coordinates[0][i:i+2]
        start2, end2 = coordinates[1][i:i+2]

        len1 = end1 - start1
        len2 = end2 - start2

        if len1 > 0 and len2 > 0:
            for k in range(min(len1, len2)):
                columns += 1
                if seq1[start1+k] == seq2[start2+k]:
                    matches += 1
            columns += abs(len1 - len2)
        else:
            columns += max(len1, len2)

    return 100 * matches / columns if columns else 0