import random
import requests
import pandas as pd

QUERY = "(reviewed:true) AND (xref:pfam-PF00042)AND (length:[100 TO 200])"


res = requests.get(
    "https://rest.uniprot.org/uniprotkb/search",
    params={"query": QUERY, "format": "json", "size": 500},
    timeout=60,
)
res.raise_for_status()
results = res.json()["results"]

rng = random.Random()
sampled = rng.sample(results, min(50, len(results)))

proteins = {}
for r in sampled:
    acc = r["primaryAccession"]
    desc = r.get("proteinDescription", {})
    name = (desc.get("recommendedName") or desc.get("submissionNames", [{}])[0]) \
        .get("fullName", {}).get("value", acc)
    proteins[acc] = {
        "name": name,
        "sequence": r["sequence"]["value"],
        "organism": r["organism"]["scientificName"],
    }

print("fetch done")
pd.DataFrame([
    {"Accession": a, "Protein": p["name"], "Organism": p["organism"], "Length": len(p["sequence"])}
    for a, p in proteins.items()
])