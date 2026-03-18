import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# ---------------------------------------------------
# Helper class extended from FPDF for colored cells
# ---------------------------------------------------
class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def colored_cell(self, w, h, txt, bg_color):
        self.set_fill_color(*bg_color)
        self.cell(w, h, txt, border=1, fill=True, align='C')

def color_code(value, low, high):
    # Green if normal, yellow if borderline, red if abnormal
    if value is None:
        return (255, 255, 255)  # white for missing
    if value < low:
        return (255, 200, 200)  # red for too low if applicable
    if low <= value <= high:
        return (200, 255, 200)  # green normal
    if value > high:
        # If borderline range is defined, can add yellow here (not implemented)
        return (255, 255, 150)  # yellow alert
    return (255, 255, 255)

# ---------------------------------------------------
# Create PDF Document
# ---------------------------------------------------
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", 'B', 16)

# Title
pdf.cell(0, 15, "Comprehensive Health Profile Summary (2017–2025)", ln=True, align="C")

# ---------------------------------------------------
# Executive Summary Page
# ---------------------------------------------------
pdf.add_page()
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "Executive Summary", ln=True, align="L")
pdf.ln(5)

# Define executive summary data and thresholds for color coding
summary_metrics = {
    "Measure": [
        "Triglycerides (mg/dL)",
        "HDL Cholesterol (mg/dL)",
        "LDL Cholesterol (mg/dL)",
        "Non-HDL Cholesterol (mg/dL)",
        "HbA1c (%)",
        "CRP (mg/L)",
        "Total Bilirubin (mg/dL)",
        "Ferritin (ng/mL)"
    ],
    "Latest Value": [127, 32, 94, 153, 5.0, 0.20, 3.99, 245.3],
    "Normal Range": [
        "< 150",
        "> 40",
        "< 116",
        "< 130",
        "4.0 - 5.6",
        "< 5.0",
        "< 1.5",
        "30 - 300"
    ],
    "Low": [None, 40, None, None, 4.0, None, None, 30],
    "High": [150, None, 116, 130, 5.6, 5.0, 1.5, 300]
}

summary_df = pd.DataFrame(summary_metrics)

# Render table header
pdf.set_font("Arial", 'B', 12)
col_widths = [70, 40, 50, 30]
row_height = 10
headers = ["Measure", "Latest Value", "Normal Range", "Flag"]
for i, h in enumerate(headers):
    pdf.cell(col_widths[i], row_height, h, border=1, align='C', fill=True)
pdf.ln()

pdf.set_font("Arial", '', 11)

# Render rows with colored cells based on latest value risk
for idx, row in summary_df.iterrows():
    measure = row["Measure"]
    latest_val = row["Latest Value"]
    normal_range = row["Normal Range"]
    low = row["Low"]
    high = row["High"]
    bg_color_val = color_code(latest_val, low, high)

    # Measure cell (no color)
    pdf.set_fill_color(255,255,255)
    pdf.cell(col_widths[0], row_height, measure, border=1, fill=True)
    # Latest value cell with color background
    pdf.colored_cell(col_widths[1], row_height, str(latest_val), bg_color_val)
    # Normal range cell (white)
    pdf.set_fill_color(255,255,255)
    pdf.cell(col_widths[2], row_height, normal_range, border=1, fill=True)
    # Flag text cell based on color (green/yellow/red)
    if bg_color_val == (200, 255, 200):
        flag_text = "Normal"
    elif bg_color_val == (255, 255, 150):
        flag_text = "Borderline"
    else:
        flag_text = "Abnormal"
    pdf.cell(col_widths[3], row_height, flag_text, border=1, fill=True, align='C')
    pdf.ln()

pdf.ln(10)
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8,
    "This executive summary provides a quick visual snapshot of your most critical markers with color-coded flags for easy identification of areas needing attention."
)

# ---------------------------------------------------
# Add remaining full report sections here (narrative + tables + graphs)
# Copied from Version 3.0 script below for brevity:
# ....

# (You can re-use the Version 3.0 code starting here)
# For this demo, just note: add_page, all narrative, tables with add_table function,
# graphs with plt.savefig + pdf.image... etc.

# ---------------------------------------------------
# Save final PDF file
# ---------------------------------------------------
pdf.output("Health_Profile_Report_v4.pdf")
