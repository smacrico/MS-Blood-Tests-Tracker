"""
Blood Test Results Visualization Script
Generates comprehensive visualizations from results_complete.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
print("Loading data...")
df = pd.read_csv('results_complete.csv')

# Convert test_date to datetime
df['test_date'] = pd.to_datetime(df['test_date'])

# Convert result_value to numeric (handle non-numeric values)
df['result_value_numeric'] = pd.to_numeric(df['result_value'], errors='coerce')

print(f"Total records: {len(df)}")
print(f"Date range: {df['test_date'].min()} to {df['test_date'].max()}")
print(f"\nData preview:")
print(df.head())

# Create figure directory
import os
os.makedirs('visualizations', exist_ok=True)

# =============================================================================
# 1. Test Status Distribution
# =============================================================================
print("\n1. Creating Test Status Distribution...")
fig, ax = plt.subplots(figsize=(10, 7))
status_counts = df['flag'].value_counts()
colors = {'Normal': '#4CAF50', 'High': '#F44336', 'Low': '#FF9800', 'Unknown': '#9E9E9E'}
status_colors = [colors.get(status, '#9E9E9E') for status in status_counts.index]

wedges, texts, autotexts = ax.pie(status_counts.values, 
                                    labels=status_counts.index,
                                    autopct='%1.1f%%',
                                    colors=status_colors,
                                    startangle=90,
                                    textprops={'fontsize': 12})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax.set_title('Blood Test Results Status Distribution', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('visualizations/01_status_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: visualizations/01_status_distribution.png")
plt.close()

# =============================================================================
# 2. Category-wise Test Count
# =============================================================================
print("2. Creating Category-wise Test Count...")
fig, ax = plt.subplots(figsize=(12, 6))
category_counts = df['category_name'].value_counts().head(10)
bars = ax.barh(range(len(category_counts)), category_counts.values, color='steelblue')
ax.set_yticks(range(len(category_counts)))
ax.set_yticklabels(category_counts.index)
ax.set_xlabel('Number of Tests', fontsize=12)
ax.set_title('Top 10 Test Categories by Count', fontsize=16, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, v in enumerate(category_counts.values):
    ax.text(v + 5, i, str(v), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/02_category_counts.png', dpi=300, bbox_inches='tight')
print("   Saved: visualizations/02_category_counts.png")
plt.close()

# =============================================================================
# 3. Abnormal Results Over Time
# =============================================================================
print("3. Creating Abnormal Results Timeline...")
abnormal_df = df[df['flag'].isin(['High', 'Low'])].copy()
abnormal_df['year_month'] = abnormal_df['test_date'].dt.to_period('M')

fig, ax = plt.subplots(figsize=(14, 6))
abnormal_by_month = abnormal_df.groupby(['year_month', 'flag']).size().unstack(fill_value=0)

if len(abnormal_by_month) > 0:
    abnormal_by_month.plot(kind='bar', ax=ax, color=['#F44336', '#FF9800'], width=0.8)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Abnormal Test Results Over Time', fontsize=16, fontweight='bold', pad=20)
    ax.legend(title='Status', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('visualizations/03_abnormal_timeline.png', dpi=300, bbox_inches='tight')
    print("   Saved: visualizations/03_abnormal_timeline.png")
else:
    print("   No abnormal results to plot")
plt.close()

# =============================================================================
# 4. Most Common Abnormal Tests
# =============================================================================
print("4. Creating Most Common Abnormal Tests...")
fig, ax = plt.subplots(figsize=(12, 8))
abnormal_tests = abnormal_df['test_name'].value_counts().head(15)
bars = ax.barh(range(len(abnormal_tests)), abnormal_tests.values, color='coral')
ax.set_yticks(range(len(abnormal_tests)))
ax.set_yticklabels(abnormal_tests.index, fontsize=10)
ax.set_xlabel('Abnormal Count', fontsize=12)
ax.set_title('Top 15 Tests with Abnormal Results', fontsize=16, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, v in enumerate(abnormal_tests.values):
    ax.text(v + 0.3, i, str(v), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/04_abnormal_tests.png', dpi=300, bbox_inches='tight')
print("   Saved: visualizations/04_abnormal_tests.png")
plt.close()

# =============================================================================
# 5. Key Health Markers Trends (if numeric data available)
# =============================================================================
print("5. Creating Key Health Markers Trends...")

# Define key markers to track (common blood test names)
key_markers = [
    'Χοληστερίνη',  # Cholesterol
    'Γλυκόζη',  # Glucose
    'Αιμοσφαιρίνη',  # Hemoglobin
    'Λευκά Αιμοσφαίρια',  # White blood cells
    'Ουρία',  # Urea
    'Κρεατινίνη'  # Creatinine
]

# Find available key markers
available_markers = []
for marker in key_markers:
    marker_data = df[df['test_name'].str.contains(marker, case=False, na=False)]
    if len(marker_data) > 0 and marker_data['result_value_numeric'].notna().sum() > 0:
        available_markers.append(marker)

if available_markers:
    # Create subplots for each available marker
    n_markers = len(available_markers)
    n_cols = 2
    n_rows = (n_markers + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    
    for idx, marker in enumerate(available_markers):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]
        
        marker_data = df[df['test_name'].str.contains(marker, case=False, na=False)].copy()
        marker_data = marker_data.dropna(subset=['result_value_numeric'])
        marker_data = marker_data.sort_values('test_date')
        
        if len(marker_data) > 0:
            # Plot trend line
            ax.plot(marker_data['test_date'], marker_data['result_value_numeric'], 
                   marker='o', linestyle='-', linewidth=2, markersize=8)
            
            # Color code by status
            for flag, color in zip(['Normal', 'High', 'Low'], ['green', 'red', 'orange']):
                flag_data = marker_data[marker_data['flag'] == flag]
                if len(flag_data) > 0:
                    ax.scatter(flag_data['test_date'], flag_data['result_value_numeric'],
                             color=color, s=100, alpha=0.6, label=flag, zorder=5)
            
            ax.set_xlabel('Date', fontsize=10)
            ax.set_ylabel('Value', fontsize=10)
            ax.set_title(f'{marker}', fontsize=12, fontweight='bold')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Hide empty subplots
    for idx in range(n_markers, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig('visualizations/05_key_markers_trends.png', dpi=300, bbox_inches='tight')
    print("   Saved: visualizations/05_key_markers_trends.png")
else:
    print("   No numeric data available for key markers")
plt.close()

# =============================================================================
# 6. Test Frequency Heatmap
# =============================================================================
print("6. Creating Test Frequency Heatmap...")
df['year'] = df['test_date'].dt.year
df['month'] = df['test_date'].dt.month

heatmap_data = df.groupby(['year', 'month']).size().unstack(fill_value=0)

if len(heatmap_data) > 0:
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax, 
                cbar_kws={'label': 'Number of Tests'})
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Year', fontsize=12)
    ax.set_title('Test Frequency Heatmap (by Month and Year)', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/06_test_frequency_heatmap.png', dpi=300, bbox_inches='tight')
    print("   Saved: visualizations/06_test_frequency_heatmap.png")
else:
    print("   Not enough data for heatmap")
plt.close()

# =============================================================================
# 7. Flag Distribution by Category
# =============================================================================
print("7. Creating Flag Distribution by Category...")
fig, ax = plt.subplots(figsize=(14, 8))

# Get top categories
top_categories = df['category_name'].value_counts().head(8).index
category_flag_data = df[df['category_name'].isin(top_categories)]

# Create stacked bar chart
flag_pivot = category_flag_data.groupby(['category_name', 'flag']).size().unstack(fill_value=0)
flag_pivot = flag_pivot.reindex(top_categories)

flag_pivot.plot(kind='barh', stacked=True, ax=ax, 
               color=['#F44336', '#FF9800', '#4CAF50', '#9E9E9E'])
ax.set_xlabel('Number of Tests', fontsize=12)
ax.set_ylabel('Category', fontsize=12)
ax.set_title('Test Results Distribution by Category', fontsize=16, fontweight='bold', pad=20)
ax.legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/07_flag_by_category.png', dpi=300, bbox_inches='tight')
print("   Saved: visualizations/07_flag_by_category.png")
plt.close()

# =============================================================================
# 8. Summary Dashboard
# =============================================================================
print("8. Creating Summary Dashboard...")
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Panel 1: Status pie chart
ax1 = fig.add_subplot(gs[0, 0])
status_counts = df['flag'].value_counts()
colors = {'Normal': '#4CAF50', 'High': '#F44336', 'Low': '#FF9800', 'Unknown': '#9E9E9E'}
status_colors = [colors.get(status, '#9E9E9E') for status in status_counts.index]
ax1.pie(status_counts.values, labels=status_counts.index, autopct='%1.0f%%',
        colors=status_colors, startangle=90)
ax1.set_title('Results Status', fontweight='bold')

# Panel 2: Tests over time
ax2 = fig.add_subplot(gs[0, 1:])
tests_by_date = df.groupby(df['test_date'].dt.to_period('M')).size()
ax2.plot(range(len(tests_by_date)), tests_by_date.values, marker='o', linewidth=2)
ax2.set_xlabel('Time Period')
ax2.set_ylabel('Number of Tests')
ax2.set_title('Test Frequency Over Time', fontweight='bold')
ax2.grid(True, alpha=0.3)

# Panel 3: Top abnormal tests
ax3 = fig.add_subplot(gs[1, :])
abnormal_df = df[df['flag'].isin(['High', 'Low'])]
top_abnormal = abnormal_df['test_name'].value_counts().head(10)
ax3.barh(range(len(top_abnormal)), top_abnormal.values, color='coral')
ax3.set_yticks(range(len(top_abnormal)))
ax3.set_yticklabels(top_abnormal.index, fontsize=9)
ax3.set_xlabel('Abnormal Count')
ax3.set_title('Top 10 Tests with Abnormal Results', fontweight='bold')
ax3.invert_yaxis()

# Panel 4: Category distribution
ax4 = fig.add_subplot(gs[2, :])
top_categories = df['category_name'].value_counts().head(8)
ax4.bar(range(len(top_categories)), top_categories.values, color='steelblue')
ax4.set_xticks(range(len(top_categories)))
ax4.set_xticklabels(top_categories.index, rotation=45, ha='right', fontsize=9)
ax4.set_ylabel('Count')
ax4.set_title('Test Distribution by Category', fontweight='bold')

# Main title
fig.suptitle('Blood Test Results - Summary Dashboard', fontsize=20, fontweight='bold', y=0.995)

plt.savefig('visualizations/08_summary_dashboard.png', dpi=300, bbox_inches='tight')
print("   Saved: visualizations/08_summary_dashboard.png")
plt.close()

# =============================================================================
# Generate Summary Report
# =============================================================================
print("\n" + "="*60)
print("VISUALIZATION SUMMARY REPORT")
print("="*60)
print(f"\nTotal Records: {len(df)}")
print(f"Date Range: {df['test_date'].min().strftime('%Y-%m-%d')} to {df['test_date'].max().strftime('%Y-%m-%d')}")
print(f"Unique Tests: {df['test_name'].nunique()}")
print(f"Unique Categories: {df['category_name'].nunique()}")

print("\n--- Status Distribution ---")
for status, count in status_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{status:10s}: {count:4d} ({percentage:5.1f}%)")

print("\n--- Top 5 Categories ---")
for cat, count in df['category_name'].value_counts().head(5).items():
    print(f"{cat}: {count}")

print("\n--- Abnormal Results Summary ---")
print(f"Total Abnormal: {len(abnormal_df)}")
print(f"High: {len(df[df['flag'] == 'High'])}")
print(f"Low: {len(df[df['flag'] == 'Low'])}")

print("\n" + "="*60)
print("All visualizations saved to 'visualizations/' directory")
print("="*60)
