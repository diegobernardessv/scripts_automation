import argparse
import sys
import json
import logging
import pandas as pd
from typing import Dict


class EstoqueAnalyzer:
    def __init__(self, file_path: str, excluir_armazens=None):
        self.file_path = file_path
        self.coluna_armazem = "Local"
        self.coluna_valor = "(D)Custo Total"
        self.coluna_grupo = "Grupo"

        self.armazens_para_excluir = excluir_armazens or [
            30, 39, 70, 71, 72, 80, 88
        ]

        self.categorias = self._definir_categorias()

    def _definir_categorias(self) -> Dict[str, list]:
        grupos_sobressalentes = (
            [3005, 3013, 3017, 3024, 4002, 4004]
            + list(range(4006, 4037))
            + list(range(4038, 4043))
        )

        grupos_embalagens = list(range(5001, 5005))

        return {
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

    def _carregar_dados(self) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")

        colunas_necessarias = [
            self.coluna_armazem,
            self.coluna_valor,
            self.coluna_grupo,
        ]

        for col in colunas_necessarias:
            if col not in df.columns:
                raise ValueError(f"Coluna obrigatória não encontrada: {col}")

        df[self.coluna_armazem] = pd.to_numeric(df[self.coluna_armazem], errors="coerce")
        df[self.coluna_grupo] = pd.to_numeric(df[self.coluna_grupo], errors="coerce")
        df[self.coluna_valor] = pd.to_numeric(df[self.coluna_valor], errors="coerce")

        df = df.dropna(
            subset=[self.coluna_armazem, self.coluna_grupo, self.coluna_valor]
        )

        return df

    def analisar(self) -> Dict:
        df = self._carregar_dados()

        df_filtrado = df[
            ~df[self.coluna_armazem].isin(self.armazens_para_excluir)
        ]

        total_por_armazem = (
            df_filtrado.groupby(self.coluna_armazem)[self.coluna_valor]
            .sum()
            .to_dict()
        )

        soma_por_grupo = (
            df_filtrado.groupby(self.coluna_grupo)[self.coluna_valor]
            .sum()
        )

        total_por_categoria = {}

        for nome, grupos in self.categorias.items():
            valor = soma_por_grupo.reindex(grupos).sum()
            total_por_categoria[nome] = float(valor)

        grupos_refratarios = [
            3003, 3004, 3006, 3007, 3008,
            3009, 3010, 3015, 3018, 3019,
            3025, 4044
        ]

        filtro_refratarios = (
            df_filtrado[self.coluna_grupo].isin(grupos_refratarios)
        ) & (
            df_filtrado[self.coluna_armazem] == 49
        )

        valor_refratarios = df_filtrado.loc[
            filtro_refratarios,
            self.coluna_valor
        ].sum()

        total_por_categoria["Refratarios"] = float(valor_refratarios)

        grupos_usados = set()
        for grupos in self.categorias.values():
            grupos_usados.update(grupos)

        valor_total_categorias = soma_por_grupo.reindex(
            list(grupos_usados)
        ).sum()

        estoque_geral = float(valor_total_categorias + valor_refratarios)

        return {
            "total_por_armazem": total_por_armazem,
            "total_por_categoria": total_por_categoria,
            "estoque_geral": estoque_geral,
        }


def configurar_logger(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    parser = argparse.ArgumentParser(
        description="CLI de Análise de Estoque"
    )

    parser.add_argument(
        "arquivo",
        help="Caminho do arquivo Excel"
    )

    parser.add_argument(
        "--exportar",
        help="Caminho para exportar resultado em JSON",
        default=None
    )

    parser.add_argument(
        "--verbose",
        help="Ativar modo detalhado",
        action="store_true"
    )

    args = parser.parse_args()

    configurar_logger(args.verbose)

    try:
        analyzer = EstoqueAnalyzer(args.arquivo)
        resultado = analyzer.analisar()

        logging.info("Análise concluída com sucesso.")

        print("\n=== ESTOQUE GERAL ===")
        print(f"R$ {resultado['estoque_geral']:,.2f}")

        if args.exportar:
            with open(args.exportar, "w", encoding="utf-8") as f:
                json.dump(resultado, f, indent=4, ensure_ascii=False)

            logging.info(f"Resultado exportado para {args.exportar}")

    except Exception as e:
        logging.error(f"Erro durante execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()