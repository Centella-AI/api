from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, QED, MolSurf,Draw

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Smile(BaseModel):
    smile : str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/trans/{tid}")
async def read_item(tid: int, q: Union[str, None] = None):
    return {"item_id": tid, "q": q}

@app.post("/predictsmile")
def read_item(d: Smile):
    mol = Chem.MolFromSmiles(d.smile)
    logp = Crippen.MolLogP(mol)
    tpsa = Descriptors.TPSA(mol)
    mw = Descriptors.MolWt(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    rotb = Lipinski.NumRotatableBonds(mol)
    bioavail = QED.qed(mol)
    tox_pred = 0 # toxicity.predict(mol)
    permeability =0 # MolSurf.pyTPSA(mol)
    img = Draw.MolToImage(mol)
    return {"2d":img,"predict":[{"name":"LogP","value":logp},{"name":"TPSA","value":tpsa},{"name":"Molecular Weight","value":mw},{"name":"Number of H-Bond Donors","value":hbd},{"name":"Number of H-Bond Acceptors","value":hba},{"name":"Number of Rotatable Bonds","value":rotb},{"name":"Bioavailability Score","value":bioavail},{"name":"Toxicity Prediction","value":tox_pred},{"name":"Permeability Score","value":permeability}]}