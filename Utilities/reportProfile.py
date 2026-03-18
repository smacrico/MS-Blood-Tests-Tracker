import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# ---------------------------------------------------
# 1. Setup and format
# ---------------------------------------------------
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", 'B', 14)

# Title
pdf.cell(200, 10, "Comprehensive Health Profile Summary (2017–2025)", ln=True, align="C")
pdf.ln(10)

# ---------------------------------------------------
# 2. Lipid Profile Data
# ---------------------------------------------------
lipid_data = {
    "Date": ["2017-12-21","2018-05-25","2018-09-12","2019-06-24","2021-04-02","2022-04-02",
             "2023-04-11","2023-09-18","2024-04-01","2024-09-18","2025-04-28","2025-09-23"],
    "Total Cholesterol": [165,191,123,145,169,176,183,182,177,193,192,151],
    "Triglycerides": [218,369,123,141,141,130,210,122,195,185,147,127],
    "HDL": [31,35,None,36,39,41.4,41,43,40,35,39,32],
    "LDL": [90,82,67,81,101,109,100,115,98,121,124,94]
}
lipid_df = pd.DataFrame(lipid_data)
date_labels = lipid_df["Date"]

# Trend Plot for Lipid Profile
plt.figure(figsize=(10,5))
sns.lineplot(x=date_labels, y=lipid_df["Total Cholesterol"], marker="o", label="Total Cholesterol")
sns.lineplot(x=date_labels, y=lipid_df["Triglycerides"], marker="o", label="Triglycerides")
sns.lineplot(x=date_labels, y=lipid_df["HDL"], marker="o", label="HDL")
sns.lineplot(x=date_labels, y=lipid_df["LDL"], marker="o", label="LDL")
plt.axhline(150, color="red", linestyle="--", label="Triglyceride Limit (150)")
plt.axhline(40, color="blue", linestyle="--", label="HDL Target (40)")
plt.xticks(rotation=45)
plt.title("Lipid Profile Trends (2017–2025)")
plt.ylabel("mg/dL")
plt.legend()
plt.tight_layout()
plt.savefig("lipid_trends.png")
plt.close()

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "1. Lipid Profile Analysis", ln=True)
pdf.image("lipid_trends.png", x=10, y=None, w=180)
pdf.ln(90)

# ---------------------------------------------------
# 3. Cardiovascular Profile Data
# ---------------------------------------------------
cv_data = {
    "Date":["2017-12-21","2018-05-25","2019-06-24","2021-04-02","2022-04-02","2023-04-11","2023-09-18",
            "2024-04-01","2024-09-18","2025-04-28","2025-09-23"],
    "CRP":[None,None,None,None,0.91,0.20,3.26,1.31,0.96,2.63,0.20],
    "HbA1c":[None,None,None,None,None,None,None,5.2,5.1,None,5.0]
}
cv_df = pd.DataFrame(cv_data)

plt.figure(figsize=(10,5))
sns.lineplot(x=cv_df["Date"], y=cv_df["CRP"], marker="o", label="CRP (mg/L)")
plt.axhline(5, color="red", linestyle="--", label="Upper Normal Limit (5.0)")
plt.xticks(rotation=45)
plt.title("Cardiovascular Inflammation Marker (CRP)")
plt.ylabel("mg/L")
plt.legend()
plt.tight_layout()
plt.savefig("cv_trends.png")
plt.close()

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "2. Cardiovascular Profile Analysis", ln=True)
pdf.image("cv_trends.png", x=10, w=180)
pdf.ln(90)

# ---------------------------------------------------
# 4. Biochemical Profile Data
# ---------------------------------------------------
bio_data = {
    "Date":["2017-12-21","2018-05-25","2019-06-24","2022-04-02","2023-04-11","2023-09-18","2024-04-01",
            "2024-09-18","2025-09-23"],
    "Bilirubin":[None,None,None,None,2.26,2.13,2.58,1.83,3.99],
    "Ferritin":[None,531.8,364.1,512,546,None,258.2,289.6,245.3]
}
bio_df = pd.DataFrame(bio_data)

plt.figure(figsize=(10,5))
sns.lineplot(x=bio_df["Date"], y=bio_df["Bilirubin"], marker="o", label="Bilirubin (mg/dL)")
plt.axhline(1.5, color="red", linestyle="--", label="Normal Limit (1.5)")
plt.xticks(rotation=45)
plt.title("Total Bilirubin Trends (2017–2025)")
plt.ylabel("mg/dL")
plt.legend()
plt.tight_layout()
plt.savefig("bil_trends.png")
plt.close()

plt.figure(figsize=(10,5))
sns.lineplot(x=bio_df["Date"], y=bio_df["Ferritin"], marker="o", label="Ferritin (ng/mL)")
plt.axhline(300, color="red", linestyle="--", label="Upper Normal Limit (300)")
plt.xticks(rotation=45)
plt.title("Ferritin (Iron Stores) Trends")
plt.ylabel("ng/mL")
plt.legend()
plt.tight_layout()
plt.savefig("fer_trends.png")
plt.close()

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "3. Whole Blood Biochemical Profile", ln=True)
pdf.image("bil_trends.png", x=10, w=180)
pdf.ln(70)
pdf.image("fer_trends.png", x=10, w=180)

# ---------------------------------------------------
# 5. Save Final PDF
# ---------------------------------------------------
pdf.output("Health_Profile_Report.pdf")
