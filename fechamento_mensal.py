import pandas as pd

def analisar_estoque(file_path):
    """
    Lê uma planilha de estoque, filtra os armazéns indesejados,
    e calcula o valor total de estoque por armazém.
    """
    try:
        # Carrega a planilha para uma estrutura de dados chamada DataFrame
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{file_path}' não foi encontrado.")
        return

    # --- CONFIGURAÇÃO ---
    # Coloque os nomes exatos das colunas da sua planilha aqui
    coluna_armazem = 'Local'
    coluna_valor = '(D)Custo Total' # Usaremos o custo total já existente na planilha
    coluna_grupo = 'Grupo'

    # Lista de armazéns que devem ser IGNORADOS no cálculo
    armazens_para_excluir = [30, 39, 70, 71, 72, 80, 88]
    # --- FIM DA CONFIGURAÇÃO ---

    print(f"\nAnalisando o arquivo: {file_path}")
    print(f"Excluindo os armazéns: {armazens_para_excluir}")

    # 1. Filtra para EXCLUIR as linhas com os armazéns indesejados
    df_filtrado = df[~df[coluna_armazem].isin(armazens_para_excluir)]

    # 2. Agrupa os dados JÁ FILTRADOS e soma o valor
    total_por_armazem = df_filtrado.groupby(coluna_armazem)[coluna_valor].sum()

    # 3. Exibe os resultados
    print("\n=== VALOR DE FECHAMENTO DE ESTOQUE POR ARMAZÉM (FILTRADO) ===")
    total_formatado = total_por_armazem.map('R$ {:,.2f}'.format)
    print(total_formatado)

    # --- NOVA ANÁLISE: VALOR POR CATEGORIA ---
    print("\n=== VALOR POR CATEGORIA DE MATERIAL ===")

    # Definição de intervalos e listas de grupos complexos
    # range(inicio, fim) no Python vai até fim-1, por isso somamos 1 ao final
    grupos_sobressalentes = [3005, 3013, 3017, 3024, 4002, 4004] + list(range(4006, 4037)) + list(range(4038, 4043))
    grupos_embalagens = list(range(5001, 5005))
    grupos_refratarios = [3003, 3004, 3006, 3007, 3008, 3009, 3010, 3015, 3018, 3019, 3025, 4044]

    # Dicionário mapeando Nome da Categoria -> Lista de Grupos
    categorias = {
        'Cal': [2001],
        'Ferroligas': [2002],
        'Carburantes': [2003],
        'Desoxidantes': [2004],
        'Eletrodos': [2005],
        'Lingoteiras': [3014],
        'Cilindros': [3011, 3012],
        'Sobressalentes': grupos_sobressalentes,
        'Uniformes': [4003],
        'Epi': [4037],
        'Embalagens': grupos_embalagens,
        'Gases': [3001, 4001],
        'Lubrificantes': [3022, 4005]
    }

    # 1. Processa categorias baseadas apenas no Grupo
    for nome, grupos in categorias.items():
        # Filtra onde o grupo está na lista e soma o valor
        valor = df_filtrado[df_filtrado[coluna_grupo].isin(grupos)][coluna_valor].sum()
        print(f"{nome}: R$ {valor:,.2f}")

    # 2. Processa Refratários (Regra Específica: Grupos X E Armazém 49)
    filtro_refratarios = (df_filtrado[coluna_grupo].isin(grupos_refratarios)) & (df_filtrado[coluna_armazem] == 49)
    valor_refratarios = df_filtrado.loc[filtro_refratarios, coluna_valor].sum()
    print(f"Refratarios: R$ {valor_refratarios:,.2f}")

if __name__ == "__main__":
    # Coloque aqui o caminho para a sua planilha de estoque.
    caminho_do_arquivo = 'analise_estoque.xlsx'
    analisar_estoque(caminho_do_arquivo)