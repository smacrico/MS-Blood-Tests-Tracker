import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# ---------------------------------------------------
# Helper: Table drawing with bold for abnormal values
# ---------------------------------------------------
def add_table(pdf, df, abnormal_rules=None, col_widths=None):
    pdf.set_font("Arial", 'B', 9)
    th = 8  # row height
    # Header
    for i, col in enumerate(df.columns):
        width = col_widths[i] if col_widths else 25
        pdf.cell(width, th, str(col), border=1, align="C")
    pdf.ln(th)
    # Rows
    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        for i, col in enumerate(df.columns):
            val = row[col]
            text = "" if pd.isna(val) else str(val)
            width = col_widths[i] if col_widths else 25
            # Abnormal check
            if abnormal_rules and col in abnormal_rules and not pd.isna(val):
                low, high = abnormal_rules[col]
                try:
                    v = float(val)
                    if (low is not None and v < low) or (high is not None and v > high):
                        pdf.set_font("Arial", 'B', 9)
                        pdf.cell(width, th, text, border=1, align="C")
                        pdf.set_font("Arial", '', 9)
                    else:
                        pdf.cell(width, th, text, border=1, align="C")
                except:
                    pdf.cell(width, th, text, border=1, align="C")
            else:
                pdf.cell(width, th, text, border=1, align="C")
        pdf.ln(th)

# ---------------------------------------------------
# Create PDF Document
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
    "The analysis is based on lab reports from December 2017 to September 2025."
)
pdf.multi_cell(0, 8, intro_text)
pdf.ln(5)

# =============================
# Section 1: Lipid Profile
# =============================
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "1. Lipid Profile Analysis", ln=True)
pdf.set_font("Arial", '', 11)

lipid_analysis = (
    "Your lipid profile shows dyslipidemia — high triglycerides, low HDL, and occasional LDL elevation.\n\n"
    "• Triglycerides: Often above the <150 mg/dL target, spiking to 369 mg/dL (2018) and 210 mg/dL (2023).\n"
    "• HDL: Persistently under target (>40 mg/dL), down to 32 mg/dL in late 2025.\n"
    "• LDL: Elevated in 2024–25 (121–124 mg/dL), normalized to 94 mg/dL by Sept 2025.\n"
    "• Non-HDL: Borderline-high at 153 mg/dL in April 2025.\n"
)
pdf.multi_cell(0, 8, lipid_analysis)

lipid_df = pd.DataFrame({
    "Date": ["21/12/2017","25/05/2018","12/09/2018","24/06/2019","02/04/2021","02/04/2022",
             "11/04/2023","18/09/2023","01/04/2024","18/09/2024","28/04/2025","23/09/2025"],
    "Total Chol": [165,191,123,145,169,176,183,182,177,193,192,151],
    "Trig": [218,369,123,141,141,130,210,122,195,185,147,127],
    "HDL": [31,35,None,36,39,41.4,41,43,40,35,39,32],
    "LDL": [90,82,67,81,101,109,100,115,98,121,124,94]
})
abnormal_rules = {
    "Total Chol": (None, 200),
    "Trig": (None, 150),
    "HDL": (40, None),   # abnormal if < 40
    "LDL": (None,116)
}
add_table(pdf, lipid_df, abnormal_rules=abnormal_rules, col_widths=[25,30,30,25,25])
pdf.ln(5)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Total Chol", data=lipid_df, marker="o", label="Total Cholesterol")
sns.lineplot(x="Date", y="Trig", data=lipid_df, marker="o", label="Triglycerides")
sns.lineplot(x="Date", y="HDL", data=lipid_df, marker="o", label="HDL")
sns.lineplot(x="Date", y="LDL", data=lipid_df, marker="o", label="LDL")
plt.axhline(150, color="red", linestyle="--", label="Trig Limit 150")
plt.axhline(40, color="blue", linestyle="--", label="HDL Target 40")
plt.xticks(rotation=45)
plt.title("Lipid Profile Trends")
plt.tight_layout()
plt.savefig("lipid_trends.png")
plt.close()
pdf.image("lipid_trends.png", x=15, w=170)
pdf.ln(80)

# =============================
# Section 2: Cardiovascular Profile
# =============================
pdf.add_page()
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "2. Cardiovascular Profile Analysis", ln=True)
pdf.set_font("Arial", '', 11)

cardio_text = (
    "Cardiovascular health drivers:\n"
    "• Dyslipidemia (high triglycerides + low HDL) remains primary risk factor.\n"
    "• Strengths include excellent glucose control (HbA1c ~5.0–5.2%) "
    "and persistently low systemic inflammation (CRP < 3 mg/L, except Sept 2023).\n"
    "Overall: Low inflammation and healthy glucose largely offset lipid-related risks."
)
pdf.multi_cell(0, 8, cardio_text)

cv_df = pd.DataFrame({
    "Date":["21/12/2017","25/05/2018","24/06/2019","02/04/2021","02/04/2022",
            "11/04/2023","18/09/2023","01/04/2024","18/09/2024",
            "28/04/2025","23/09/2025"],
    "CRP":[None,None,None,None,0.91,0.20,3.26,1.31,0.96,2.63,0.20],
    "HbA1c":[None,None,None,None,None,None,None,5.2,5.1,None,5.0]
})
abnormal_rules_cv = {
    "CRP": (None,5.0),
    "HbA1c": (None,6.5)
}
add_table(pdf, cv_df, abnormal_rules=abnormal_rules_cv, col_widths=[30,30,30])
pdf.ln(5)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="CRP", data=cv_df, marker="o", label="CRP (mg/L)")
plt.axhline(5, color="red", linestyle="--", label="CRP Upper Limit 5 mg/L")
plt.xticks(rotation=45)
plt.title("CRP Inflammation Trends")
plt.tight_layout()
plt.savefig("cv_trends.png")
plt.close()
pdf.image("cv_trends.png", x=15, w=170)
pdf.ln(80)

# =============================
# Section 3: Biochemical Profile
# =============================
pdf.add_page()
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "3. Whole Blood Biochemical Profile", ln=True)
pdf.set_font("Arial", '', 11)

bio_text = (
    "• Liver enzymes normalized after 2017, but bilirubin levels remain chronically high (>1.5 mg/dL), "
    "recently nearing 4.0 mg/dL.\n"
    "• Ferritin spiked >500 ng/mL in 2018, 2022, and 2023 — now decreased to ~245 ng/mL (Sept 2025).\n"
    "• TSH remained stable across years, indicating normal thyroid function.\n"
)
pdf.multi_cell(0, 8, bio_text)

bio_df = pd.DataFrame({
    "Date":["21/12/2017","25/05/2018","24/06/2019","02/04/2022","11/04/2023",
            "18/09/2023","01/04/2024","18/09/2024","23/09/2025"],
    "Bilirubin":[None,None,None,None,2.26,2.13,2.58,1.83,3.99],
    "Ferritin":[None,531.8,364.1,512,546,None,258.2,289.6,245.3]
})
abnormal_rules_bio = {
    "Bilirubin": (None,1.5),
    "Ferritin": (None,300)
}
add_table(pdf, bio_df, abnormal_rules=abnormal_rules_bio, col_widths=[30,30,30])
pdf.ln(5)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Bilirubin", data=bio_df, marker="o", label="Total Bilirubin (mg/dL)")
plt.axhline(1.5, color="red", linestyle="--", label="Normal Limit 1.5")
plt.xticks(rotation=45)
plt.title("Total Bilirubin Trends")
plt.tight_layout()
plt.savefig("bil_trends.png")
plt.close()
pdf.image("bil_trends.png", x=15, w=170)
pdf.ln(70)

plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Ferritin", data=bio_df, marker="o", label="Ferritin (ng/mL)")
plt.axhline(300, color="red", linestyle="--", label="Upper Normal Limit 300")
plt.xticks(rotation=45)
plt.title("Ferritin Trends")
plt.tight_layout()
plt.savefig("fer_trends.png")
plt.close()
pdf.image("fer_trends.png", x=15, w=170)

# ---------------------------------------------------
# Final Save
# ---------------------------------------------------
pdf.output("Health_Profile_Report_v3.pdf")
