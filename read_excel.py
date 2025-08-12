import pandas as pd
import os

# Analisar arquivo Excel mais detalhadamente
file_path = 'attached_assets/Pasta1_1754997528539.xlsx'

if os.path.exists(file_path):
    print(f"\n=== Análise detalhada: {file_path} ===")
    try:
        # Ler com header=None para ver estrutura bruta
        df = pd.read_excel(file_path, sheet_name=' PEDIDO 2025 ARIELLE', header=None)
        print(f"Dimensões: {df.shape}")
        print("\nPrimeiras 15 linhas (estrutura bruta):")
        for i in range(min(15, len(df))):
            print(f"Linha {i}: {list(df.iloc[i])}")
        
        # Tentar identificar cabeçalhos
        print("\n=== Tentando identificar estrutura de lotes ===")
        for i in range(min(20, len(df))):
            row_values = [str(val) for val in df.iloc[i] if pd.notna(val)]
            if any('LOTE' in str(val).upper() for val in row_values):
                print(f"Linha {i} contém LOTE: {row_values}")
            elif any('CONGREGAÇÃO' in str(val).upper() for val in row_values):
                print(f"Linha {i} contém CONGREGAÇÃO: {row_values}")
                
        # Verificar colunas com dados numéricos (tamanhos)
        print("\n=== Análise de colunas com dados ===")
        for col in df.columns:
            non_null_count = df[col].notna().sum()
            if non_null_count > 5:  # Colunas com pelo menos 5 valores
                print(f"Coluna {col}: {non_null_count} valores não nulos")
                unique_vals = df[col].dropna().unique()[:10]  # Primeiros 10 valores únicos
                print(f"  Valores únicos (amostra): {unique_vals}")
                
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
else:
    print(f"Arquivo não encontrado: {file_path}")