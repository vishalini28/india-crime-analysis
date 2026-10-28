import re
import pdfplumber
import pandas as pd

NUM = r"-?[\d,]+(?:\.\d+)?"

def parse_pdf(path, columns):
    """Read rows like '1 Agra 5665 6947 7026 17.5 402.4 79.3' into a DataFrame."""
    n = len(columns) - 1
    pattern = re.compile(rf"^\d+\s+(.+?)\s+((?:{NUM}\s+){{{n-1}}}{NUM})$")
    rows = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for line in (page.extract_text() or "").split("\n"):
                m = pattern.match(line.strip())
                if m:
                    nums = [float(x.replace(",", "")) for x in m.group(2).split()]
                    rows.append([m.group(1)] + nums)
    return pd.DataFrame(rows, columns=columns)

ipc = parse_pdf(
    "1_datasets/raw/ipc_city_wise_2021_2023.pdf",
    ["city", "ipc_2021", "ipc_2022", "ipc_2023",
     "population_lakhs_2011", "ipc_rate_2023", "ipc_chargesheet_rate_2023"],
)
violent = parse_pdf(
    "1_datasets/raw/table_3.pdf",
    ["city", "violent_2021", "violent_2022", "violent_2023",
     "population_lakhs_2011", "violent_rate_2023", "violent_chargesheet_rate_2023"],
)

ipc.to_csv("1_datasets/processed/ipc_city_2021_2023.csv", index=False)
violent.to_csv("1_datasets/processed/violent_city_2021_2023.csv", index=False)

print("IPC rows:", len(ipc), "| Violent rows:", len(violent))
print(ipc.head())
print(violent.head())
