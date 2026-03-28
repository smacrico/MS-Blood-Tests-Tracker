def lipid_profile_calculator(total_cholesterol, hdl, triglycerides):
    """
    Calculate lipid profile components and key ratios.

    :param total_cholesterol: Total cholesterol in mg/dL
    :param hdl: HDL cholesterol in mg/dL
    :param triglycerides: Triglycerides in mg/dL

    :return: Dictionary with LDL, non-HDL cholesterol, cholesterol ratios, and triglyceride interpretation
    """
    # Calculate LDL cholesterol using Friedewald formula
    # Valid only if triglycerides < 400 mg/dL
    if triglycerides < 400:
        ldl = total_cholesterol - hdl - (triglycerides / 5)
    else:
        ldl = None # Cannot calculate accurately if triglycerides too high
    
    # Calculate non-HDL cholesterol
    non_hdl = total_cholesterol - hdl
    
    # Calculate total cholesterol to HDL ratio
    try:
        tc_hdl_ratio = total_cholesterol / hdl
    except ZeroDivisionError:
        tc_hdl_ratio = None
    
    # Interpret triglycerides levels
    if triglycerides < 150:
        tg_status = "Normal"
    elif triglycerides < 199:
        tg_status = "Borderline High"
    elif triglycerides < 499:
        tg_status = "High"
    else:
        tg_status = "Very High"
    
    return {
        "LDL Cholesterol (mg/dL)": round(ldl, 2) if ldl is not None else "Cannot calculate - triglycerides too high",
        "Non-HDL Cholesterol (mg/dL)": round(non_hdl, 2),
        "Total Cholesterol to HDL Ratio": round(tc_hdl_ratio, 2) if tc_hdl_ratio is not None else "Undefined (HDL=0)",
        "Triglycerides Status": tg_status
    }

# Example usage
result = lipid_profile_calculator(total_cholesterol=2000, hdl=50, triglycerides=150)
for k, v in result.items():
    print(f"{k}: {v}")
