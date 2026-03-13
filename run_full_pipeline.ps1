# Complete Blood Test Tracker Pipeline
# This script runs the full workflow from scratch

Write-Host "=== MS Blood Test Tracker - Full Pipeline ===" -ForegroundColor Cyan

# Step 1: Clean previous database (optional - uncomment if you want fresh start)
# Write-Host "`n[1/3] Cleaning previous database..." -ForegroundColor Yellow
# if (Test-Path "data\ms_blood_tests.db") {
#     Remove-Item "data\ms_blood_tests.db" -Force
#     Write-Host "  ✓ Database removed" -ForegroundColor Green
# }

# Step 2: Process all PDFs
Write-Host "`n[1/3] Processing all PDFs..." -ForegroundColor Yellow
python main.py --pdf-dir data\pdfs
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ PDF processing complete" -ForegroundColor Green
} else {
    Write-Host "  ✗ PDF processing failed" -ForegroundColor Red
    exit 1
}

# Step 3: Export to CSV
Write-Host "`n[2/3] Exporting results to CSV..." -ForegroundColor Yellow
python main.py --export results_complete.csv
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Export complete: results_complete.csv" -ForegroundColor Green
} else {
    Write-Host "  ✗ Export failed" -ForegroundColor Red
    exit 1
}

# Step 4: Display summary
Write-Host "`n[3/3] Summary:" -ForegroundColor Yellow
$summaryScript = @"
import pandas as pd
df = pd.read_csv('results_complete.csv')
print(f'Total results: {len(df)}')
print(f'Unique tests: {df["test_name"].nunique()}')
print(f'Date range: {df["test_date"].min()} to {df["test_date"].max()}')
print(f'\nTop 10 tests:')
print(df['test_name'].value_counts().head(10))
"@
python -c $summaryScript

Write-Host "`n=== Pipeline Complete ===" -ForegroundColor Cyan
Write-Host "Results saved to: results_complete.csv" -ForegroundColor Green
