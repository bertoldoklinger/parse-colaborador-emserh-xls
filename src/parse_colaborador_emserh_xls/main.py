import pandas as pd
from datetime import date
from requests import post

month_map = {
    1: "jan.",
    2: "fev.",
    3: "mar.",
    4: "abr.",
    5: "mai.",
    6: "jun.",
    7: "jul.",
    8: "ago.",
    9: "set.",
    10: "out.",
    11: "nov.",
    12: "dez.",
}

def format_date_to_ptbr_manual(date_str):
    if pd.isnull(date_str):
        return "Data inválida"
    date_obj = pd.to_datetime(date_str)
    day = date_obj.day
    month = month_map[date_obj.month]
    year = date_obj.year
    return f"{day} de {month} de {year}"

def process_xls(input_file, output_file):
    df = pd.read_excel(input_file, engine="xlrd", dtype={"CPF": str, "matrícula": str})

    df["CPF"] = df["CPF"].fillna("").apply(lambda x: x.zfill(11))
    if "matrícula" in df.columns:
        df["matrícula"] = df["matrícula"].fillna("").apply(lambda x: x.zfill(9))

    df["Admissão"] = df["Admissão"].apply(
        lambda x: format_date_to_ptbr_manual(x) if pd.notnull(x) else "Data inválida"
    )

    df.to_csv(output_file, index=False)
    print(f"Arquivo processado com sucesso. Resultado salvo em {output_file}")

date_atual = date.today()
output_file = f"colaboradores_emserh_{date_atual.day if date_atual.day >= 10 else f'0{date_atual.day}'}_{date_atual.month if date_atual.month >= 10 else f'0{date_atual.month}'}_{date_atual.year}.csv"

process_xls("src/parse_colaborador_emserh_xls/colaboradores_emserh_10_12_2024.XLS", output_file)