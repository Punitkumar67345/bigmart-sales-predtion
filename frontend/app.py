import streamlit as st
import pandas as pd
import time
import requests

# -------------------------------
# PAGE CONFIG & CSS
# -------------------------------
st.set_page_config(page_title="Big Mart Intelligence", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stApp { background-color: #07090E; color: #E2E8F0; }
header, footer, #MainMenu { visibility: hidden; }
.hero-title {
    font-size: 50px; font-weight: 800; text-align: center;
    background: linear-gradient(135deg, #00C9FF, #92FE9D);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; padding-top: 10px;
}
.hero-subtitle { text-align: center; color: #64748B; margin-bottom: 30px; font-size: 16px; }
div[data-baseweb="select"] > div, div[data-baseweb="input"] { background-color: #0F141E !important; border: 1px solid #1E293B !important; border-radius: 8px !important; color: #F8FAFC !important; }
label { color: #94A3B8 !important; font-weight: 500 !important; font-size: 14px !important; }
div.stButton > button { background: linear-gradient(90deg, #00C9FF, #10B981); color: black !important; font-weight: bold; border-radius: 8px; border: none; text-transform: uppercase; transition: all 0.3s ease; }
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0, 201, 255, 0.2); }
.stTabs [data-baseweb="tab-list"] { background-color: transparent; }
.stTabs [data-baseweb="tab"] { color: #94A3B8; font-weight: 600; }
.stTabs [aria-selected="true"] { color: #00C9FF !important; border-bottom: 2px solid #00C9FF !important; }

/* Custom Card CSS */
.metric-card {
    padding: 15px; border-radius: 10px; color: #E2E8F0; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.metric-title { font-size: 12px; color: #94A3B8; text-transform: uppercase; font-weight: bold; margin-bottom: 8px; }
.metric-value { font-size: 15px; font-weight: 600; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown('<div class="hero-title">BIG MART INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Enterprise-Grade Sales, Shelf & Multi-Objective Optimization Engine</div>', unsafe_allow_html=True)

# -------------------------------
# TABS
# -------------------------------
tab1, tab2 = st.tabs(["🎯 Single Item Scanner", "📂 Multi-Object Engine (Bulk CSV)"])

# ==========================================
# TAB 1: SINGLE ITEM PREDICTION
# ==========================================
with tab1:
    col1, space, col2 = st.columns([1, 0.05, 1])

    with col1:
        item_weight = st.number_input("Item Weight (kg)", 1.0, 20.0, 10.0, step=0.5)
        item_fat = st.selectbox("Fat Content", ["Low Fat", "Regular"])
        item_type = st.selectbox("Item Category", ["Dairy", "Soft Drinks", "Meat", "Fruits and Vegetables", "Household", "Baking Goods", "Snack Foods"])
        item_visibility = st.number_input("Store Visibility Index (%)", 0.0, 1.0, 0.05, step=0.01)
        item_mrp = st.number_input("Maximum Retail Price (₹)", 50.0, 300.0, 150.0, step=1.0)

    with col2:
        outlet_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Grocery Store", "Supermarket Type3"])
        outlet_size = st.selectbox("Store Floor Size", ["Small", "Medium", "High"])
        outlet_location = st.selectbox("City Tier Classification", ["Tier 1", "Tier 2", "Tier 3"])
        outlet_year = st.number_input("Year of Establishment", 1985, 2026, 2000, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button("INITIALIZE PREDICTION SEQUENCE", use_container_width=True):
            data = {
                "Item_Weight": item_weight, "Item_Fat_Content": item_fat, "Item_Type": item_type,
                "Item_Visibility": item_visibility, "Item_MRP": item_mrp, "Outlet_Size": outlet_size,
                "Outlet_Location_Type": outlet_location, "Outlet_Type": outlet_type,
                "Outlet_Establishment_Year": outlet_year, "Outlet_Age": 2026 - outlet_year
            }
            try:
                with st.spinner("Processing AI Matrix..."):
                    res = requests.post("http://127.0.0.1:8000/predict", json=data)
                    response_data = res.json()
                
                # --- 3 COLUMN DASHBOARD RESULTS ---
                st.markdown("<hr style='border-color: #1E293B;'>", unsafe_allow_html=True)
                res1, res2, res3 = st.columns(3)
                
                # Column 1: Sales
                with res1:
                    st.success(f"💰 Projected Sales\n### ₹ {response_data['prediction']:,.2f}")
                
                # Column 2: Shelf Analysis (Innovation 1)
                with res2:
                    s_status = response_data["shelf_status"]
                    s_bg = "rgba(239, 68, 68, 0.1)" if s_status == "warning" else "rgba(16, 185, 129, 0.1)" if s_status == "upgrade" else "rgba(0, 201, 255, 0.1)"
                    s_border = "#EF4444" if s_status == "warning" else "#10B981" if s_status == "upgrade" else "#00C9FF"
                    s_icon = "🚨" if s_status == "warning" else "🌟" if s_status == "upgrade" else "✅"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="background-color: {s_bg}; border-left: 4px solid {s_border};">
                        <div class="metric-title">{s_icon} Innovation 1: Shelf Analysis</div>
                        <div class="metric-value">{response_data['shelf_action']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Column 3: Multi-Objective (Innovation 2)
                with res3:
                    o_status = response_data["opt_status"]
                    o_bg = "rgba(168, 85, 247, 0.1)" if o_status == "discount" else "rgba(245, 158, 11, 0.1)" if o_status == "profit" else "rgba(99, 102, 241, 0.1)"
                    o_border = "#A855F7" if o_status == "discount" else "#F59E0B" if o_status == "profit" else "#6366F1"
                    o_icon = "📉" if o_status == "discount" else "💎" if o_status == "profit" else "⚖️"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="background-color: {o_bg}; border-left: 4px solid {o_border};">
                        <div class="metric-title">{o_icon} Innovation 2: Multi-Objective</div>
                        <div class="metric-value">{response_data['opt_action']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.balloons()
            except Exception as e:
                st.error("⚠️ Backend Error! Ensure uvicorn is running.")

# ==========================================
# TAB 2: MULTI-OBJECT ENGINE (BULK UPLOAD)
# ==========================================
with tab2:
    st.markdown("### 📂 Upload CSV for Bulk AI Processing")
    st.markdown("<span style='color: #64748B;'>Process thousands of items at once to get Sales, Shelf Placement, and Optimization Strategy.</span>", unsafe_allow_html=True)
    
    sample_df = pd.DataFrame({
        "Item_Weight": [9.3, 5.9], "Item_Fat_Content": ["Low Fat", "Regular"], "Item_Type": ["Dairy", "Meat"],
        "Item_Visibility": [0.016, 0.045], "Item_MRP": [249.8, 45.0], "Outlet_Size": ["Medium", "Small"],
        "Outlet_Location_Type": ["Tier 1", "Tier 2"], "Outlet_Type": ["Supermarket Type1", "Grocery Store"],
        "Outlet_Establishment_Year": [1999, 2009]
    })
    
    st.download_button("📥 Download Sample CSV Template", data=sample_df.to_csv(index=False), file_name="template.csv", mime="text/csv")
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your Store Inventory (CSV format)", type=["csv"])
    
    if uploaded_file is not None:
        df_bulk = pd.read_csv(uploaded_file)
        st.write("👀 Data Preview:")
        st.dataframe(df_bulk.head(3))
        
        if st.button("🚀 RUN BULK PREDICTION", use_container_width=True):
            try:
                payload = df_bulk.to_dict(orient="records")
                with st.spinner("Running Multi-Objective Optimization Matrix..."):
                    res = requests.post("http://127.0.0.1:8000/predict_bulk", json=payload)
                    bulk_result = res.json()["results"]
                
                result_df = pd.DataFrame(bulk_result)
                st.success("✅ Multi-Object Prediction Complete!")
                
                # Show all the new cool columns
                st.dataframe(result_df[['Item_Type', 'Item_MRP', 'Predicted_Sales', 'Shelf_Action', 'Optimization_Strategy']], use_container_width=True)
                
                csv_data = result_df.to_csv(index=False)
                st.download_button(label="💾 Download Final Predictions CSV", data=csv_data, file_name="ai_predictions_output.csv", mime="text/csv")
                
            except Exception as e:
                st.error("⚠️ Error processing file. Make sure columns match the template!")