import streamlit as st
import pandas as pd

# Define conversion table
conversion_table = {
    "Glucose": ("mmol/L", "mg/dL", 18.0182),
    "Cholesterol": ("mmol/L", "mg/dL", 38.67),
    "Creatinine": ("mg/dL", "µmol/L", 88.4),
    "Calcium": ("mmol/L", "mg/dL", 4.0),
    # Add more if needed
}

# Function to convert lab values
def convert_lab_value(lab_name, value, from_unit):
    if lab_name in conversion_table:
        expected_unit, target_unit, multiplier = conversion_table[lab_name]
        if from_unit == expected_unit:
            return round(value * multiplier, 2), target_unit
        elif from_unit == target_unit:
            return round(value / multiplier, 2), expected_unit
        else:
            return None, f"Unit mismatch"
    return None, "Unknown lab"

# Streamlit UI
st.title("Lab Value Unit Converter")

st.write("Convert lab test results between different units (e.g., mmol/L ↔ mg/dL)")

# Upload CSV or manual input
input_mode = st.radio("Choose input method:", ["Manual Entry", "Upload CSV"])

if input_mode == "Manual Entry":
    lab = st.selectbox("Select Lab Test", list(conversion_table.keys()))
    value = st.number_input("Enter Lab Value", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("Select Unit", [conversion_table[lab][0], conversion_table[lab][1]])

    if st.button("Convert"):
        converted_value, unit = convert_lab_value(lab, value, from_unit)
        if converted_value is not None:
            st.success(f"Converted Value: {converted_value} {unit}")
        else:
            st.error(f"Error: {unit}")

else:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if all(col in df.columns for col in ["Lab", "Value", "Unit"]):
            converted = df.apply(lambda row: convert_lab_value(row["Lab"], row["Value"], row["Unit"]), axis=1)
            df[["Converted_Value", "Converted_Unit"]] = pd.DataFrame(converted.tolist(), index=df.index)
            st.dataframe(df)

            # Option to download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Converted CSV", csv, "converted_labs.csv", "text/csv")
        else:
            st.error("CSV must have columns: Lab, Value, Unit")
