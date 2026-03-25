from fastapi import FastAPI
import pickle
import pandas as pd
import os
from pymongo import MongoClient
from typing import List, Dict, Any

# 1. FastAPI Initialize
app = FastAPI()

# -------------------------------
# LOAD MODEL
# -------------------------------
model_path = os.path.join(os.path.dirname(__file__), "../model/model.pkl")
model = pickle.load(open(model_path, "rb"))

# -------------------------------
# MONGODB CONNECTION
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["bigmart_db"]
collection = db["predictions"]

@app.get("/")
def home():
    return {"message": "Big Mart Intelligence Backend Running"}

# -------------------------------
# API 1: SINGLE PREDICTION
# -------------------------------
@app.post("/predict")
def predict(data: dict):
    input_df = pd.DataFrame([data])

    for col in model.feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model.feature_names_in_]

    prediction = float(model.predict(input_df)[0])
    visibility = data.get("Item_Visibility", 0)
    mrp = data.get("Item_MRP", 1)

    # -------------------------------
    # INNOVATION 1: SELF ANALYSIS
    # -------------------------------
    if visibility > 0.12 and prediction < 1500:
        self_action = "Underperforming Asset: High visibility but low conversion. Needs quality review."
        self_status = "warning"
        shelf_action = self_action
        shelf_status = self_status
    elif visibility < 0.05 and prediction > 2500:
        self_action = "High-Potential Asset: Strong organic demand despite low visibility."
        self_status = "upgrade"
        shelf_action = self_action
        shelf_status = self_status
    else:
        self_action = "Stable Asset: Item attributes and sales are perfectly balanced."
        self_status = "optimal"
        shelf_action = self_action
        shelf_status = self_status

    # -------------------------------
    # INNOVATION 2: MULTI-OBJECTIVE OPTIMIZATION
    # -------------------------------
    expected_units_sold = prediction / mrp

    if expected_units_sold < 10:
        opt_action = "Clearance Strategy: Apply 15-20% Discount to minimize excess inventory."
        opt_status = "discount"
    elif expected_units_sold >= 30:
        opt_action = "Profit Maximize: High demand. Keep 100+ units in stock. 0% Discount."
        opt_status = "profit"
    else:
        opt_action = "Balanced Strategy: Maintain regular stock. Optional 5% promotional discount."
        opt_status = "balanced"

    # MongoDB save
    try:
        collection.insert_one({
            "input": data,
            "prediction": prediction,
            "self_analysis": self_action,
            "optimization": opt_action,
            "type": "single"
        })
    except Exception:
        pass  # MongoDB na ho toh bhi app chale

    return {
        "prediction": prediction,
        "self_action": self_action,
        "self_status": self_status,
        "shelf_action": shelf_action,   # app.py ke liye
        "shelf_status": shelf_status,   # app.py ke liye
        "opt_action": opt_action,
        "opt_status": opt_status
    }

# -------------------------------
# API 2: BULK PREDICTION
# -------------------------------
@app.post("/predict_bulk")
def predict_bulk(data_list: List[Dict[str, Any]]):
    input_df = pd.DataFrame(data_list)

    if 'Outlet_Age' not in input_df.columns and 'Outlet_Establishment_Year' in input_df.columns:
        input_df['Outlet_Age'] = 2026 - input_df['Outlet_Establishment_Year']

    for col in model.feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0

    predict_df = input_df[model.feature_names_in_]
    predictions = model.predict(predict_df)
    input_df['Predicted_Sales'] = predictions

    self_actions = []
    opt_actions = []

    for index, row in input_df.iterrows():
        vis = row.get('Item_Visibility', 0)
        mrp_val = row.get('Item_MRP', 1)
        pred = row['Predicted_Sales']

        if vis > 0.12 and pred < 1500:
            self_actions.append("Underperforming Asset")
        elif vis < 0.05 and pred > 2500:
            self_actions.append("High-Potential Asset")
        else:
            self_actions.append("Stable Asset")

        units = pred / mrp_val
        if units < 10:
            opt_actions.append("Apply 15% Discount (Clearance)")
        elif units >= 30:
            opt_actions.append("Maximize Profit (High Stock, 0% Disc)")
        else:
            opt_actions.append("Balanced Stock (5% Disc)")

    input_df['Shelf_Action'] = self_actions
    input_df['Optimization_Strategy'] = opt_actions

    try:
        collection.insert_one({"type": "bulk_upload", "count": len(data_list)})
    except Exception:
        pass

    return {"results": input_df.to_dict(orient="records")}