import streamlit as st
import pandas as pd

# Simulate Data (Fake Data for Demonstration Purposes)
cip_data = {
    'CIP Code': ['01.0000', '01.0308', '01.1004', '01.1101', '01.1102'],
    'CIP Title': [
        'Agriculture, General', 
        'Agroecology and Sustainable Agriculture', 
        'Viticulture and Enology', 
        'Plant Sciences, General', 
        'Agronomy and Crop Science'
    ],
    'Graduates': [120, 45, 35, 50, 70]
}

soc_data = {
    'SOC Code': ['19-1011', '19-1012', '19-1013', '19-4012', '25-1041'],
    'SOC Title': [
        'Animal Scientists', 
        'Food Scientists and Technologists', 
        'Soil and Plant Scientists', 
        'Agricultural Technicians', 
        'Agricultural Sciences Teachers, Postsecondary'
    ],
    'Total Openings': [10, 15, 50, 40, 20],
    'ONET % Doctoral': [43, 29, 19, 18, 55],
    'ONET % Master': [22, 24, 29, 32, 14],
    'ONET % Bachelor': [13, 19, 24, 29, 27]
}

cip_df = pd.DataFrame(cip_data)
soc_df = pd.DataFrame(soc_data)

# Streamlit App
st.title('Program Supply-Demand Gap Analysis Tool')

# Step 1: Select CIP
st.sidebar.header('Select CIP and Parameters')
selected_cip = st.sidebar.selectbox('Select a CIP:', cip_df['CIP Title'])
selected_degree_type = st.sidebar.selectbox('Select Degree Type:', ['Doctoral', 'Master', 'Bachelor'])

# Display Selected CIP Information
cip_info = cip_df[cip_df['CIP Title'] == selected_cip]
st.write(f"### Selected CIP: {selected_cip}")
st.write(cip_info)

# Calculate Gap Ratio
def calculate_gap_ratio(cip, degree_type):
    total_graduates = cip['Graduates'].values[0]
    adjusted_demands = []
    soc_demands = soc_df['Total Openings']
    degree_column = f'ONET % {degree_type}'
    
    for soc_index, soc_row in soc_df.iterrows():
        percent_by_degree = soc_row[degree_column] / 100
        adjusted_demand = soc_row['Total Openings'] * (total_graduates / cip_df['Graduates'].sum()) * percent_by_degree
        adjusted_demands.append(adjusted_demand)
    
    gap_ratio = total_graduates / sum(adjusted_demands)
    return gap_ratio, adjusted_demands

gap_ratio, calculations = calculate_gap_ratio(cip_info, selected_degree_type)

# Display Results
st.write(f"### Calculated Gap Ratio: {gap_ratio:.2f}")
st.write("### Breakdown of Calculations:")
for i, soc in enumerate(soc_df['SOC Title']):
    st.write(f"{soc}: Adjusted Demand = {calculations[i]:.2f}")

# Allow Pop-Out of Detailed Calculations
if st.button("Show Detailed Calculations"):
    st.write("### Detailed Calculations")
    for i, soc in enumerate(soc_df['SOC Title']):
        st.write(f"{soc}: {calculations[i]:.2f}")