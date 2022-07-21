from io import StringIO
from pathlib import Path
import numpy as np
import pandas as pd

def processa(file_path_spec, file_path_rem, parte):
    df_spec = pd.read_csv(file_path_spec)
    for index, row in df_spec.iterrows():
        df_spec.at[index, "start_pos"] = row["start_pos"]-1
    df_colspecs = df_spec[["start_pos", "end_pos"]]
    colspecs = [tuple(r) for r in df_colspecs.to_numpy()]
    columns =  df_spec["name"].values.tolist()
    descriptions = df_spec["description"].values.tolist()
    start_pos = df_spec["start_pos"].values.tolist()
    end_pos = df_spec["end_pos"].values.tolist()
    with open(file_path_rem) as f:
        lines = f.readlines()
    if parte == "header":
        lines = lines[0]
    elif parte == "detalhe":
        lines =  lines[1:len(lines)-1]
    elif parte == "trailer":
        lines = lines[-1]
    lines = ''.join(lines)   
    df = pd.read_fwf(StringIO(lines), colspecs=colspecs, names=columns, dtype=str)
    df.loc[1] = descriptions
    df.loc[2] = start_pos
    df.loc[3] = end_pos
    spec_name = Path(file_path_spec).stem
    remessa_name = Path(file_path_rem).stem
    df.T.to_csv(f"{remessa_name}_{spec_name}_processado.csv", sep=',', encoding='utf-8')
    
file_rem = 'CB210701.REM'

processa('spec/bb/header_bb.csv',file_rem, "header")
processa('spec/bb/detalhe_bb.csv',file_rem, "detalhe")



