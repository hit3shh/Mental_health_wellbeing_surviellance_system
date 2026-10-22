
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "changing_childhood.csv"
OUTPUT_PATH = ROOT / "docs" / "datasets" / "data_dictionary.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"CSV not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, low_memory=False)

verified = {
    "WP22826": (
        "Main source used most often to stay informed about current events",
        "1=Social media; 2=Online news websites; 3=Radio/TV/newspapers; "
        "4=None; 5=Don't know; 6=Refused"
    ),
    "WP22827": ("Trust in news media", "1=A lot; 2=A little; 3=Not at all; 8=Don't know; 9=Refused"),
    "WP22086": ("Trust in social media platforms", "1=A lot; 2=A little; 3=Not at all; 8=Don't know; 9=Refused"),
    "WP22087": ("Trust in national government", "1=A lot; 2=A little; 3=Not at all; 8=Don't know; 9=Refused"),
    "WP22088": ("Trust in doctors and healthcare workers", "1=A lot; 2=A little; 3=Not at all; 8=Don't know; 9=Refused"),
    "WP22089": ("Trust in scientists", "1=A lot; 2=A little; 3=Not at all; 8=Don't know; 9=Refused"),
    "WP22090": ("Trust in religious organizations", "1=A lot; 2=A little; 3=Not at all; 8=Don't know; 9=Refused"),
    "WP22091": (
        "Identification with local area, country, or world",
        "1=Local area; 2=Country; 3=World; 8=Don't know; 9=Refused"
    ),
    "WP22125": ("Whether respondent has heard of climate change", "1=Yes; 2=No; 8=Don't know; 9=Refused"),
    "WP22828": (
        "What comes to mind when hearing 'climate change'",
        "1=Seasonal weather changes; 2=Extreme weather/global temperature rise caused by human activity; "
        "3=Neither/something else; 8=Don't know; 9=Refused"
    ),
    "countrynew": ("Country name", "Categorical country label; confirm source documentation"),
    "wgt": ("Survey weight", "Weight variable; consult methodology before weighted analysis"),
    "EMP_2010": ("Employment status category", "See Gallup codebook employment section"),
    "INCOME_5": ("Per-capita income quintile", "See Gallup codebook income section"),
    "WP1219": ("Respondent gender", "1=Male; 2=Female"),
    "WP1220": ("Respondent age", "99=99 years or older; 100=Refused"),
    "WP2319": (
        "Feelings about household income",
        "1=Living comfortably; 2=Getting by; 3=Finding it difficult; "
        "4=Finding it very difficult; 5=Don't know; 6=Refused"
    ),
    "WP16056": ("Access to the internet", "1=Yes; 2=No; 3=Don't know; 4=Refused"),
    "WP4657": ("Whether respondent was born in this country", "1=Born in country; 2=Born elsewhere; 3=Don't know; 4=Refused"),
}

rows = []

for col in df.columns:
    if col in verified:
        description, codes = verified[col]
        status = "Documented in uploaded questionnaire/codebook; verify dataset version"
    else:
        description = "Pending verification against the appropriate codebook section"
        codes = "Not decoded; do not recode yet"
        status = "Pending verification"

    rows.append({
        "column": col,
        "data_type": str(df[col].dtype),
        "description": description,
        "response_codes": codes,
        "verification_status": status,
        "missing_count": int(df[col].isna().sum()),
        "unique_values": int(df[col].nunique(dropna=True)),
    })

dictionary = pd.DataFrame(rows)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
dictionary.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"Data dictionary saved to: {OUTPUT_PATH}")
print(f"Columns documented: {len(dictionary)}")
print(f"Pending verification: {(dictionary['verification_status'] == 'Pending verification').sum()}")
print(dictionary[["column", "description", "verification_status"]].to_string(index=False))
