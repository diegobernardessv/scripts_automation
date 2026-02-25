import pandas as pd
import argparse
from decimal import Decimal, ROUND_HALF_UP


def arredondar(valor):
    return float(
        Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    )


def analisar_estoque(arquivo):
    df = pd.read_excel(arquivo)

    coluna_armazem = "Local"
    coluna_valor = "(D)Custo Total"
    coluna_grupo = "Grupo"

    armazens_excluir = [30, 39, 70, 71, 72, 80, 88]

    # Conversão segura
    df[coluna_armazem] = pd.to_numeric(df[coluna_armazem], errors="coerce")
    df[coluna_grupo] = pd.to_numeric(df[coluna_grupo], errors="coerce")
    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors="coerce")

    df = df.dropna(subset=[coluna_armazem, coluna_grupo, coluna_valor])

    # Remove armazéns indesejados
    df = df[~df[coluna_armazem].isin(armazens_excluir)]

    # ========================
    # DEFINIÇÃO DAS CATEGORIAS
    # ========================

    grupos_sobressalentes = (
        [3005, 3013, 3017, 3024, 4002, 4004]
        + list(range(4006, 4037))
        + list(range(4038, 4043))
    )

    grupos_embalagens = list(range(5001, 5005))

    grupos_refratarios = [
        3003, 3004, 3006, 3007, 3008,
        3009, 3010, 3015, 3018, 3019,
        3025, 4044
    ]

    categorias = {
        "Cal": [2001],
        "Ferroligas": [2002],
        "Carburantes": [2003],
        "Desoxidantes": [2004],
        "Eletrodos": [2005],
        "Lingoteiras": [3014],
        "Cilindros": [3011, 3012],
        "Sobressalentes": grupos_sobressalentes,
        "Uniformes": [4003],
        "Epi": [4037],
        "Embalagens": grupos_embalagens,
        "Gases": [3001, 4001],
        "Lubrificantes": [3022, 4005],
    }

    # ========================
    # CÁLCULO POR CATEGORIA
    # ========================

    soma_por_grupo = df.groupby(coluna_grupo)[coluna_valor].sum()

    total_categorias = {}

    for nome, grupos in categorias.items():
        valor = soma_por_grupo.reindex(grupos).sum()
        total_categorias[nome] = arredondar(valor)

    # ========================
    # REFRACTÁRIOS (REGRA ESPECIAL)
    # ========================

    filtro_refratarios = (
        df[coluna_grupo].isin(grupos_refratarios)
    ) & (
        df[coluna_armazem] == 49
    )

    valor_refratarios = arredondar(
        df.loc[filtro_refratarios, coluna_valor].sum()
    )

    total_categorias["Refratarios"] = valor_refratarios

    # ========================
    # ESTOQUE GERAL
    # ========================

    estoque_geral = arredondar(sum(total_categorias.values()))

    # ========================
    # OUTPUT
    # ========================

    print("\n=== VALOR POR CATEGORIA ===")
    for nome, valor in total_categorias.items():
        print(f"{nome}: R$ {valor:,.2f}")

    print("\n=== ESTOQUE GERAL ===")
    print(f"R$ {estoque_geral:,.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "arquivo",
        nargs="?",
        default="analise_estoque.xlsx",
        help="Arquivo Excel de estoque"
    )

    args = parser.parse_args()

    analisar_estoque(args.arquivo)