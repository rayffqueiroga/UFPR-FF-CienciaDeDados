# Análise Longitudinal de Trabalhadores Estrangeiros no Mercado Formal do Paraná (CAGED/OBMigra)

## Objetivo

Este projeto realiza uma análise exploratória e longitudinal dos trabalhadores estrangeiros registrados no mercado formal de trabalho do Estado do Paraná (UF = 41), utilizando os microdados do <Entity>Cadastro Geral de Empregados e Desempregados – CAGED</Entity>, disponibilizados pelo <Entity>Observatório das Migrações Internacionais (OBMigra)</Entity>. O CAGED registra mensalmente admissões e desligamentos de imigrantes no mercado formal brasileiro. 【1-cf9fb4】

O objetivo é produzir indicadores estatísticos, séries temporais e visualizações para apoiar pesquisas científicas sobre:

- Inserção de imigrantes no mercado formal;
- Evolução das nacionalidades ao longo do tempo;
- Distribuição territorial dos trabalhadores estrangeiros no Paraná;
- Escolaridade;
- Setores econômicos de inserção;
- Estrutura ocupacional;
- Distribuição salarial;
- Desigualdade de rendimentos.

Os trabalhadores brasileiros são excluídos das análises.

---

# Fonte dos Dados

Os microdados são disponibilizados pelo <Entity>OBMigra</Entity>, no portal de microdados do <Entity>CAGED</Entity>. O portal disponibiliza séries históricas anuais e mensais referentes às movimentações de trabalhadores imigrantes no mercado formal brasileiro. 【1-cf9fb4】

Portal oficial:

https://www.gov.br/mj/pt-br/assuntos/seus-direitos/migracoes/portal-de-imigracao-laboral/obmigra-1/microdados/caged/CAGED

Anos disponíveis no portal:

- 2026
- 2025
- 2024
- 2023
- 2022
- 2021
- 2020

Além destes, o portal também disponibiliza séries históricas desde 2011. 【1-cf9fb4】

---

# Estrutura do Projeto

```text
projeto_caged/
│
├── analise_estrangeiros_longitudinal.py
│
├── dados/
│   ├── RAIS_CTPS_CAGED_2020_MOV.csv
│   ├── RAIS_CTPS_CAGED_2021_MOV.csv
│   ├── RAIS_CTPS_CAGED_2022_MOV.csv
│   ├── RAIS_CTPS_CAGED_2023_MOV.csv
│   ├── RAIS_CTPS_CAGED_2024_MOV.csv
│   ├── RAIS_CTPS_CAGED_2025_MOV.csv
│   ├── RAIS_CTPS_CAGED_2026_MOV.csv
│   │
│   ├── municipio.csv
│   ├── cbo2002ocupacao.csv
│   └── subclasse.csv
│
└── saida/
```

---

# Requisitos

## Python

O projeto foi desenvolvido e testado utilizando Python 3.14.

Verificação:

```bash
python3 --version
```

---

## Dependências

Instalar as bibliotecas necessárias:

```bash
pip install pandas numpy matplotlib seaborn openpyxl scipy
```

Alternativamente, criar um arquivo `requirements.txt`:

```text
pandas
numpy
matplotlib
seaborn
openpyxl
scipy
```

e instalar:

```bash
pip install -r requirements.txt
```

---

# Preparação do Ambiente

Criar um ambiente virtual:

```bash
python3 -m venv .venv
```

Ativar o ambiente:

```bash
source .venv/bin/activate
```

Instalar dependências:

```bash
pip install pandas numpy matplotlib seaborn openpyxl scipy
```

---

# Execução

Executar o script principal:

```bash
python analise_estrangeiros_longitudinal.py
```

O script detectará automaticamente todos os arquivos anuais presentes na pasta `dados`.

---

# Fluxo de Processamento

O pipeline executa automaticamente as seguintes etapas.

## 1. Leitura Longitudinal

Todos os arquivos com padrão:

```text
RAIS_CTPS_CAGED_*_MOV.csv
```

são carregados autom*ticamente.

**ano é extraído do nome do arquivo * adicionado à base consolidada.

E*emplo:

```text
RAIS_CTPS_CAGED_20*4_MOV.csv
```

gera:

```text
ano * 2024
```

---

## 2. Filtragem do*Paraná

São mant*dos apenas registros com:

```text*UF = 41
```

*orrespondentes ao Estado do Paraná*

---

## 3. Exclusão de Brasileir*s

Os registros classificados como*

```text
NATURALIDADE BRASILEIRA
*``

*ão removidos, preservando apenas m*vimentações de trabalhadores estra*geiros.

---

## 4. Conversão*de Variáveis

O script*converte automaticamente*

```text
salario
valors*lariofixo
```

para formato numéri*o.

Também cria o campo:

```*ext
salario_final
``*

*riorizando `valorsalariofixo` quan*o disponível.

---

## 5. Tradução*de Códigos

Os códigos*administrativos são convertidos pa*a*descrições compreensíveis.

### Mu*icípios

Exemplo:

```text*4106902 → Curitiba
```

### Ocupaç*es (CBO)

Exemplo*

```text*784205 → Alimentador de Linha*de Produção
```

*## Atividades Econômicas (CNAE)

E*emplo:

```text*1012101 → Abate de A*es
```

*--

# Métricas Estatísticas Produz*das

O script calcula:

## Estatís*icas Salariais

- Média
-*Mediana
- Percentil 25 (P25)
- Per*entil 75 (P75)
- Desvio padrão
-*Assimetria (Skewness)
- Curtose (K*rtosis)

##*Índice de Gini

Calcula*a desigualdade da distribuição sal*rial dos trabalhadores estrangeiro*.

Interpretação:

```text
0 = igu*ldade perfeita
1 =*desigualdade máxima
```

*--

# Análises Transversais

*# Nacionalidades

Identifica:

- P*incipais países de origem;
-*Participação percentual;
- Distrib*ição dos grupos migratórios.

Exem*l*s observ*dos na base:

*``text
Venezuela
Cuba
Paraguai
H*iti*Argentina
```

---

## Municípios
*Determina os municípios paranaense* com maior concentração de trabalh*dores estrangeiros.

---

## Escol*ridade

Classificação utilizada:

*``text
Fundamental Incompleto
Fund*mental Completo
Médio Incompleto
M*dio*Completo
Superior Incompleto
Super*or Completo
*ós-graduação
```

---

## Setores *conômicos

Agr*pamento por seção CNAE:

```text
A*ropecuária
Indústria de Transforma*ão
*onstrução
Comércio
Trans*orte*e Logística
Alojamento e Alimentaç*o
Educação
*a*de
Serviços Administrativos
Out*os*Serviços
```

---

## Estrutura Oc*pacional

As ocupações são agrupad*s em grandes grupos da CBO:

```te*t
Dirigentes
Profissionais Científ*cos
Técnicos
Administrativos
Servi*os e Vendas
*g*opecuária
Produção Industrial
Oper*dores*de Máquinas
Ocupações Elementares
*``

---

# Análises Longitudinais
*## Evolução do Número de Estrangei*os

Calcula:

```*ext
Movimentações por ano
```

e

*``*ext*Taxa de crescimento anual (%)
```
*---

## Evolução das Nacionalidade*

Permite identificar:

* Crescimento de venezuelanos;
- Cr*scimento de cubanos;
-*Mud*nças na participação relativa das *acionalidades.

---

## Evolução d*s Setores Econômicos

Avalia alter*ções no perfil de inserção econômi*a dos trabalhadores estrangeiros a* longo do tempo.

---

## Evolução*Salarial

Calcula:

```text
Salári* mediano por ano
```

possibilitan*o avaliar tendências de valorizaçã* ou precarização salarial.

---

#*Arquivos Gerados

## Planilhas Exc*l

```text
resumo_artigo.xlsx
evol*cao_anual.xlsx
salario_anual.xlsx
*esumo_anual.xlsx
```

---

## Gráf*cos

```text
evolucao_anual.png

s*lario_mediano_anual.png

e*ol*cao_nacionalidades.png

evolucao_s*tores.png

heatmap_ano_pais.png

*eatmap_ano_setor.png
``*

*--

# Questões Científicas Investi*áveis

O conjunto de saídas permit* responder questões como:

- Como *voluiu a participação dos trabalha*ores estrangeiros no Paraná?
- Qua*s nacionalidades cresceram ou redu*iram sua participação ao longo dos*anos?
- Em quais setores econômico* os estrangeiros se concentram?
- *ouve mudança no perfil ocupacional*
- O nível educacional dos trabalh*dores estrangeiros mudou?
- Os sal*rios evoluíram positivamente?
- Há*evidências de desigualdade salaria*?
- Existe concentração geográfica*dos trabalhadores estrangeiros?

-*-

# Limitações

- O estudo depend* da disponibilidade dos microdados*do CAGED.
- Alterações futuras no *ayout dos arquivos poderão exigir *justes no código.
- A análise cont*mpla apenas vínculos formais regis*rados.
- O trabalho não contempla *nformalidade, empreendedorismo inf*rmal ou trabalho autônomo não regi*trado.

---

# Referências

Portal*de Microdados do CAGED (OBMigra):
*https://www.gov.br/mj/pt-br/assunt*s/seus-direitos/migracoes/portal-d*-imigracao-laboral/obmigra-1/micro*ados/caged/CAGED

Fonte institucio*al: <Entity>Observatório das Migra*ões Internacionais (OBMigra)</Enti*y> e <Entity>Ministério da Justiça*e Segurança Pública</Entity>. 【1-c*9fb4】
````*
