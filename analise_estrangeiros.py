from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# CONFIGURACAO
# ======================================================

PASTA_DADOS = Path("dados")

OUT = Path("saida")
OUT.mkdir(exist_ok=True)

GRAF = OUT / "graficos"
GRAF.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# ======================================================
# FUNCOES
# ======================================================

def ler_csv_seguro(arquivo):

    encodings = [
        "utf-8",
        "latin1",
        "cp1252",
        "iso-8859-1"
    ]

    for enc in encodings:

        try:

            df = pd.read_csv(
                arquivo,
                sep=";",
                dtype=str,
                encoding=enc,
                low_memory=False
            )

            print(
                f"{arquivo.name} -> encoding={enc}"
            )

            return df

        except Exception:
            continue

    raise Exception(
        f"Nao foi possivel ler {arquivo}"
    )

def gini(x):

    x = np.asarray(x)

    x = x[~np.isnan(x)]

    if len(x) == 0:
        return np.nan

    x = np.sort(x)

    n = len(x)

    acumulado = np.cumsum(x)

    return (
        (
            n + 1
            - 2 * np.sum(acumulado) / acumulado[-1]
        )
        / n
    )

# ======================================================
# LEITURA LONGITUDINAL
# ======================================================

arquivos = sorted(
    PASTA_DADOS.glob(
        "RAIS_CTPS_CAGED_*_MOV.csv"
    )
)

if not arquivos:
    raise Exception(
        "Nenhum arquivo encontrado"
    )

dfs = []

for arquivo in arquivos:

    ano = int(
        arquivo.stem.split("_")[3]
    )

    print(f"\nLendo {arquivo.name}")

    tmp = ler_csv_seguro(
        arquivo
    )

    COLUNAS_MINIMAS = [
        "competenciamov",
        "pais",
        "uf",
        "municipio",
        "cbo2002ocupacao",
        "subclasse",
        "secao",
        "nivel_instrucao",
        "salario"
    ]

    faltando = [
        c for c in COLUNAS_MINIMAS
        if c not in tmp.columns
    ]

    if faltando:

        print(
            f"Arquivo ignorado. "
            f"Colunas faltando: {faltando}"
        )

        continue

    tmp["ano"] = ano

    dfs.append(tmp)

df = pd.concat(
    dfs,
    ignore_index=True
)

# ======================================================
# FILTRO PARANÁ
# ======================================================

df = df[
    df["uf"] == "41"
].copy()

# ======================================================
# REMOVER BRASILEIROS
# ======================================================

df = df[
    ~df["pais"]
     .astype(str)
     .str.upper()
     .str.contains(
         "BRASILEIRA",
         na=False
     )
].copy()

print(
    f"Estrangeiros: {len(df):,}"
)

# ======================================================
# SALARIO
# ======================================================

for campo in [
    "salario",
    "valorsalariofixo"
]:

    if campo in df.columns:

        df[campo] = pd.to_numeric(
            df[campo],
            errors="coerce"
        )

if "valorsalariofixo" in df.columns:

    df["salario_final"] = np.where(
        df["valorsalariofixo"].notna(),
        df["valorsalariofixo"],
        df["salario"]
    )

else:

    df["salario_final"] = df["salario"]

# ======================================================
# ESCOLARIDADE
# ======================================================

ESCOLARIDADE = {
    "01":"Fundamental Incompleto",
    "02":"Fundamental Completo",
    "03":"Médio Incompleto",
    "04":"Médio Completo",
    "05":"Superior Incompleto",
    "06":"Superior Completo",
    "07":"Pós-graduação",
    "-1":"Não Informado"
}

df["escolaridade"] = (
    df["nivel_instrucao"]
      .map(ESCOLARIDADE)
)

# ======================================================
# MUNICIPIOS
# ======================================================

mun = pd.read_csv(
    PASTA_DADOS / "municipio.csv",
    sep=";",
    encoding="latin1",
    dtype=str
)

mun = mun.rename(
    columns={
        "Código Município Completo":"municipio",
        "Nome_Município":"municipio_nome"
    }
)

df["municipio"] = df["municipio"].astype(str)
mun["municipio"] = mun["municipio"].astype(str)

df = df.merge(
    mun[
        [
            "municipio",
            "municipio_nome"
        ]
    ],
    on="municipio",
    how="left"
)

# ======================================================
# CBO
# ======================================================

cbo = pd.read_csv(
    PASTA_DADOS / "cbo2002ocupacao.csv",
    sep=";",
    encoding="latin1",
    dtype=str
)

cbo = cbo.rename(
    columns={
        "Código":"cbo2002ocupacao",
        "Descrição":"ocupacao"
    }
)

df["cbo2002ocupacao"] = (
    df["cbo2002ocupacao"]
      .astype(str)
      .str.zfill(6)
)

cbo["cbo2002ocupacao"] = (
    cbo["cbo2002ocupacao"]
      .astype(str)
      .str.zfill(6)
)

df = df.merge(
    cbo,
    on="cbo2002ocupacao",
    how="left"
)

# ======================================================
# SETORES
# ======================================================

SECAO_CNAE = {
    "A":"Agropecuária",
    "B":"Indústrias Extrativas",
    "C":"Indústria de Transformação",
    "D":"Energia",
    "E":"Água e Resíduos",
    "F":"Construção",
    "G":"Comércio",
    "H":"Transporte e Logística",
    "I":"Alojamento e Alimentação",
    "J":"Informação e Comunicação",
    "K":"Financeiro",
    "L":"Imobiliário",
    "M":"Profissionais",
    "N":"Administrativos",
    "O":"Administração Pública",
    "P":"Educação",
    "Q":"Saúde",
    "R":"Cultura",
    "S":"Outros Serviços"
}

df["setor"] = (
    df["secao"]
      .map(SECAO_CNAE)
)

# ======================================================
# RESUMO
# ======================================================

sal = df["salario_final"]

resumo = pd.DataFrame({
    "Indicador":[
        "Registros",
        "Nacionalidades",
        "Municipios",
        "Setores",
        "Media",
        "Mediana",
        "P25",
        "P75",
        "Desvio Padrao",
        "Assimetria",
        "Curtose",
        "Gini"
    ],
    "Valor":[
        len(df),
        df["pais"].nunique(),
        df["municipio_nome"].nunique(),
        df["setor"].nunique(),
        round(sal.mean(),2),
        round(sal.median(),2),
        round(sal.quantile(.25),2),
        round(sal.quantile(.75),2),
        round(sal.std(),2),
        round(sal.skew(),4),
        round(sal.kurtosis(),4),
        round(gini(sal),4)
    ]
})

resumo.to_excel(
    OUT / "resumo_artigo.xlsx",
    index=False
)

# ======================================================
# EVOLUCAO ANUAL
# ======================================================

evolucao = (
    df.groupby("ano")
      .size()
      .reset_index(name="movimentacoes")
)

evolucao["crescimento_%"] = (
    evolucao["movimentacoes"]
      .pct_change()
      * 100
)

evolucao.to_excel(
    OUT / "evolucao_anual.xlsx",
    index=False
)

# ======================================================
# EVOLUCAO SALARIAL
# ======================================================

salario_ano = (
    df.groupby("ano")
      ["salario_final"]
      .median()
      .reset_index()
)

# ======================================================
# TOP PAISES
# ======================================================

top_paises = (
    df["pais"]
      .value_counts()
      .head(10)
      .index
)

pais_ano = (
    df[df["pais"].isin(top_paises)]
      .groupby(
          ["ano","pais"]
      )
      .size()
      .reset_index(name="quantidade")
)

# ======================================================
# TOP SETORES
# ======================================================

top_setores = (
    df["setor"]
      .value_counts()
      .head(8)
      .index
)

setor_ano = (
    df[df["setor"].isin(top_setores)]
      .groupby(
          ["ano","setor"]
      )
      .size()
      .reset_index(name="quantidade")
)

# ======================================================
# GRAFICOS
# ======================================================

plt.figure(figsize=(12,6))

sns.lineplot(
    data=evolucao,
    x="ano",
    y="movimentacoes",
    marker="o"
)

plt.title(
    "Evolucao Anual dos Estrangeiros"
)

plt.tight_layout()

plt.savefig(
    GRAF / "evolucao_anual.png",
    dpi=300
)

plt.close()

plt.figure(figsize=(12,6))

sns.lineplot(
    data=salario_ano,
    x="ano",
    y="salario_final",
    marker="o"
)

plt.title(
    "Salario Mediano por Ano"
)

plt.tight_layout()

plt.savefig(
    GRAF / "salario_mediano_anual.png",
    dpi=300
)

plt.close()

plt.figure(figsize=(16,8))

sns.lineplot(
    data=pais_ano,
    x="ano",
    y="quantidade",
    hue="pais",
    marker="o"
)

plt.title(
    "Evolucao das Nacionalidades"
)

plt.tight_layout()

plt.savefig(
    GRAF / "evolucao_nacionalidades.png",
    dpi=300
)

plt.close()

plt.figure(figsize=(16,8))

sns.lineplot(
    data=setor_ano,
    x="ano",
    y="quantidade",
    hue="setor",
    marker="o"
)

plt.title(
    "Evolucao por Setor Economico"
)

plt.tight_layout()

plt.savefig(
    GRAF / "evolucao_setores.png",
    dpi=300
)

plt.close()

print("\nConcluido.")
print(f"Resultados em: {OUT.resolve()}")
