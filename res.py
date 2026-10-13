from itertools import combinations
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from cos import exp_emb
from seq import sequence_identity
from protData import proteins
import numpy as np


results = []

for a, b in combinations(proteins.keys(), 2):
    seq1 = proteins[a]["sequence"]
    seq2 = proteins[b]["sequence"]

    identity = sequence_identity(seq1, seq2)

    # cos_sim = cosine_similarity(
    #     exp_emb[a].reshape(1, -1),
    #     exp_emb[b].reshape(1, -1)
    # )[0, 0]
    E = np.stack([exp_emb[a] for a in proteins])
    mu = E.mean(axis=0)
    embeddings_c = {a: exp_emb[a] - mu for a in proteins}
    cos_sim_c = cosine_similarity(
        embeddings_c[a].reshape(1, -1),
        embeddings_c[b].reshape(1, -1)
    )[0, 0]
    results.append({
        "Protein A": a,
        "Protein B": b,
        "seq": identity,
        "cos": cos_sim_c
    })

    

df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)


x = df["seq"]
y = df["cos"] 

print("Spearman:", spearmanr(x, y).statistic)
print("Pearson:", pearsonr(x, y).statistic)
plt.figure(figsize=(8, 6))
plt.scatter(x, y)
plt.xlabel("Sequence Identity (%)")
plt.ylabel("ESM-2 Cosine Similarity (Centered)")
plt.title("Sequence Identity and ESM-2 Cosine Similarity")
plt.grid(True)
# plt.show()
plt.savefig(f"figs2/fig_s{spearmanr(x, y).statistic}_p{pearsonr(x, y).statistic}.png", dpi=300)