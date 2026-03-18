import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# ---------------------------------------------------
# Create PDF Setup
# ---------------------------------------------------
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", 'B', 14)

# Title
pdf.cell(200, 10, "Comprehensive Health Profile Summary (2017–2025)", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", '', 12)
intro_text = (
    "This document synthesizes your health data into three key profiles: "
    "the Lipid Profile, the Cardiovascular Profile, and the Whole Blood Biochemical Profile. "
    "The analysis is based on the full set of lab reports provided, covering the period from "
    "December 2017 to September 2025."
)
pdf.multi_cell(0, 8, intro_text)
pdf.ln(5)

# ---------------------------------------------------
# 1. Lipid Profile Section
# ---------------------------------------------------
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "1. Lipid Profile Analysis", ln=True)
pdf.set_font("Arial", '', 11)

lipid_analysis = (
    "Your lipid profile is characterized by dyslipidemia — with a pattern of high triglycerides, "
    "low HDL ('good') cholesterol, and occasionally elevated LDL ('bad') cholesterol.\n\n"
    "• Triglycerides: Frequently above the desirable <150 mg/dL limit, with spikes such as 369 mg/dL in 2018 "
    "and 210 mg/dL in 2023. More recently (2025), your values returned to the normal range.\n"
    "• HDL Cholesterol: Persistently below the recommended >40 mg/dL, with a very low 32 mg/dL in 2025.\n"
    "• LDL Cholesterol: Elevated in late 2024 and early 2025, but improved to 94 mg/dL in September 2025.\n"
    "• Non-HDL Cholesterol: Measured at a borderline high (153.0 mg/dL) in April 2025.\n"
)
pdf.multi_cell(0, 8, lipid_analysis)
pdf.ln(3)

# Data & Plot for Lipid Trends
lipid_data = {
    "Date": ["2017-12-21","2018-05-25","2018-09-12","2019-06-24","2021-04-02","2022-04-02",
             "2023-04-11","2023-09-18","2024-04-01","2024-09-18","2025-04-28","2025-09-23"],
    "Total Cholesterol": [165,191,123,145,169,176,183,182,177,193,192,151],
    "Triglycerides": [218,369,123,141,141,130,210,122,195,185,147,127],
    "HDL": [31,35,None,36,39,41.4,41,43,40,35,39,32],
    "LDL": [90,82,67,81,101,109,100,115,98,121,124,94]
}
lipid_df = pd.DataFrame(lipid_data)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Total Cholesterol", data=lipid_df, marker="o", label="Total Cholesterol")
sns.lineplot(x="Date", y="Triglycerides", data=lipid_df, marker="o", label="Triglycerides")
sns.lineplot(x="Date", y="HDL", data=lipid_df, marker="o", label="HDL")
sns.lineplot(x="Date", y="LDL", data=lipid_df, marker="o", label="LDL")
plt.axhline(150, color="red", linestyle="--", label="Triglyceride Normal Limit 150")
plt.axhline(40, color="blue", linestyle="--", label="HDL Target 40")
plt.xticks(rotation=45)
plt.title("Lipid Profile Trends (2017–2025)")
plt.ylabel("mg/dL")
plt.legend()
plt.tight_layout()
plt.savefig("lipid_trends.png")
plt.close()
pdf.image("lipid_trends.png", x=15, w=170)
pdf.ln(80)

# ---------------------------------------------------
# 2. Cardiovascular Profile Section
# ---------------------------------------------------
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "2. Cardiovascular Profile Analysis", ln=True)
pdf.set_font("Arial", '', 11)

cardio_text = (
    "This section integrates lipid levels, inflammation markers, and glucose metabolism.\n\n"
    "Risk Drivers:\n"
    "• Primary Risk Factor: Dyslipidemia — high triglycerides and low HDL.\n"
    "• Favorable Factors: Excellent glucose control (HbA1c consistently ~5.0-5.2%). "
    "Low inflammation as measured by CRP, mostly under 3 mg/L except a single spike in Sept 2023.\n\n"
    "Summary: While dyslipidemia is the key cardiovascular concern, your glucose metabolism and very "
    "low systemic inflammation significantly mitigate overall cardiovascular risk."
)
pdf.multi_cell(0, 8, cardio_text)
pdf.ln(3)

cv_data = {
    "Date":["2017-12-21","2018-05-25","2019-06-24","2021-04-02","2022-04-02","2023-04-11","2023-09-18",
            "2024-04-01","2024-09-18","2025-04-28","2025-09-23"],
    "CRP":[None,None,None,None,0.91,0.20,3.26,1.31,0.96,2.63,0.20]
}
cv_df = pd.DataFrame(cv_data)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="CRP", data=cv_df, marker="o", label="CRP (mg/L)")
plt.axhline(5, color="red", linestyle="--", label="Normal Upper Limit")
plt.xticks(rotation=45)
plt.title("Cardiovascular Inflammation Marker (CRP)")
plt.ylabel("mg/L")
plt.legend()
plt.tight_layout()
plt.savefig("cv_trends.png")
plt.close()
pdf.image("cv_trends.png", x=15, w=170)
pdf.ln(70)

# ---------------------------------------------------
# 3. Biochemical Profile Section
# ---------------------------------------------------
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "3. Whole Blood Biochemical Profile", ln=True)
pdf.set_font("Arial", '', 11)

bio_text = (
    "This section covers liver function, iron stores, and thyroid function.\n\n"
    "• Liver Function: ALT and AST normalized after initial elevation in 2017. "
    "However, bilirubin has been persistently elevated (>1.5 mg/dL) with a recent rise to ~4.0 mg/dL.\n"
    "• Iron Stores: Ferritin showed very high peaks in 2018, 2022, and 2023 (>500 ng/mL) but "
    "have since declined to high-normal (~245 ng/mL in Sept 2025).\n"
    "• Thyroid and Kidney Function: TSH remained consistently stable in the reference range across all years.\n"
)
pdf.multi_cell(0, 8, bio_text)
pdf.ln(3)

bio_data = {
    "Date":["2017-12-21","2018-05-25","2019-06-24","2022-04-02","2023-04-11","2023-09-18","2024-04-01",
            "2024-09-18","2025-09-23"],
    "Bilirubin":[None,None,None,None,2.26,2.13,2.58,1.83,3.99],
    "Ferritin":[None,531.8,364.1,512,546,None,258.2,289.6,245.3]
}
bio_df = pd.DataFrame(bio_data)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Bilirubin", data=bio_df, marker="o", label="Total Bilirubin (mg/dL)")
plt.axhline(1.5, color="red", linestyle="--", label="Normal Limit 1.5")
plt.xticks(rotation=45)
plt.title("Total Bilirubin Trends")
plt.ylabel("mg/dL")
plt.legend()
plt.tight_layout()
plt.savefig("bil_trends.png")
plt.close()
pdf.image("bil_trends.png", x=15, w=170)
pdf.ln(70)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Ferritin", data=bio_df, marker="o", label="Ferritin (ng/mL)")
plt.axhline(300, color="red", linestyle="--", label="Upper Normal Limit 300")
plt.xticks(rotation=45)
plt.title("Ferritin (Iron Stores) Trends")
plt.ylabel("ng/mL")
plt.legend()
plt.tight_layout()
plt.savefig("fer_trends.png")
plt.close()
pdf.image("fer_trends.png", x=15, w=170)

# ---------------------------------------------------
# Final Save
# ---------------------------------------------------
pdf.output("Health_Profile_Report_v2.pdf")
