import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Manufacturing Efficiency Predictor", layout="wide")

st.title("🏭 Manufacturing Efficiency Analysis System")
st.markdown("Predict the efficiency score based on machine and material parameters.")

# Layout
with st.form("manufacturing_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Process Parameters")
        inj_temp = st.number_input("Injection Temperature", value=220.0)
        inj_press = st.number_input("Injection Pressure", value=120.0)
        cycle_time = st.number_input("Cycle Time", value=30.0)
        cooling_time = st.number_input("Cooling_Time", value=12.0)
        viscosity = st.number_input("Material Viscosity", value=250.0)
        amb_temp = st.number_input("Ambient Temperature", value=25.0)

    with col2:
        st.subheader("Machine & Operator")
        machine_age = st.number_input("Machine Age (Years)", value=5.0)
        op_exp = st.number_input("Operator Experience (Years)", value=5.0)
        maint_hours = st.number_input("Maintenance Hours", value=50.0)
        shift = st.selectbox("Shift", options=["Day", "Evening", "Night"])
        machine_type = st.selectbox("Machine Type", options=["Type_A", "Type_B", "Type_C"])
        material_grade = st.selectbox("Material Grade", options=["Economy", "Standard", "Premium"])

    with col3:
        st.subheader("Metrics & Time")
        day = st.selectbox("Day of Week", options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        temp_press_ratio = st.number_input("Temp/Pressure Ratio", value=1.8)
        total_cycle = st.number_input("Total Cycle Time", value=45.0)
        utilization = st.number_input("Machine Utilization", value=0.5)
        pph = st.number_input("Parts Per Hour", value=30.0)

    submit = st.form_submit_button("Analyze Efficiency")

if submit:
    payload = {
        "Injection_Temperature": inj_temp,
        "Injection_Pressure": inj_press,
        "Cycle_Time": cycle_time,
        "Cooling_Time": cooling_time,
        "Material_Viscosity": viscosity,
        "Ambient_Temperature": amb_temp,
        "Machine_Age": machine_age,
        "Operator_Experience": op_exp,
        "Maintenance_Hours": maint_hours,
        "Shift": shift,
        "Machine_Type": machine_type,
        "Material_Grade": material_grade,
        "Day_of_Week": day,
        "Temperature_Pressure_Ratio": temp_press_ratio,
        "Total_Cycle_Time": total_cycle,
        "Machine_Utilization": utilization,
        "Parts_Per_Hour": pph
    }
    
    try:
        backend_url = "http://localhost:8001/predict"
        response = requests.post(backend_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            score = result["predicted_efficiency_score"]
            
            st.divider()
            st.metric("Predicted Efficiency Score", f"{score:.4f}")
            
            if score > 0.5:
                st.success("High Efficiency Detected!")
            else:
                st.warning("Low Efficiency Detected. Check process parameters.")
        else:
            st.error("Error from backend. Ensure it is running on port 8001.")
    except Exception as e:
        st.error(f"Connection failed: {e}")

st.sidebar.info("Workflow: \n1. Train model in Colab\n2. Move `.pth` and `.pkl` to `model/` \n3. Run backend then frontend.")
