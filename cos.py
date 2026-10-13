import torch
import esm
from protData import proteins

model, alphabet = esm.pretrained.esm2_t36_3B_UR50D()
model.eval()

batch_converter = alphabet.get_batch_converter()
model = model.to('cpu')

embeddings = {}

for acc, protein in proteins.items():
    batch = [(acc, protein["sequence"])]
    _, _, tokens = batch_converter(batch)
    tokens = tokens.to('cpu')

    with torch.no_grad():
        result = model(tokens, repr_layers=[6])

    residue_embeddings = result["representations"][6][0, 1:len(protein["sequence"])+1]
    embeddings[acc] = residue_embeddings.mean(dim=0).cpu().numpy()

print('cos done')
exp_emb = embeddings