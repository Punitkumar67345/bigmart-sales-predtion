import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# 1. Dataset load kar rahe hain 'data' folder se
df = pd.read_csv("data/train.csv")

# 2. Preprocessing - Missing values ko theek kar rahe hain
# Weight me mean (average) daal rahe hain
df['Item_Weight'] = df['Item_Weight'].fillna(df['Item_Weight'].mean())
# Size me sabse zyada aane wala (mode) daal rahe hain
df['Outlet_Size'] = df['Outlet_Size'].fillna(df['Outlet_Size'].mode()[0])

# 3. Fat content ke alag-alag naam ko ek standard 'Low Fat' aur 'Regular' me badal rahe hain
df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
    'LF': 'Low Fat',
    'low fat': 'Low Fat',
    'reg': 'Regular'
})

# 4. Agar item ki visibility 0 hai (jo ki possible nahi), toh usko average se replace kar rahe hain
df['Item_Visibility'] = df['Item_Visibility'].replace(0, df['Item_Visibility'].mean())

# 5. Outlet ki age nikal rahe hain (Kyunki abhi 2026 chal raha hai)
df['Outlet_Age'] = 2026 - df['Outlet_Establishment_Year']

# 6. Jo columns prediction ke kaam ke nahi hain (ID waghera), unko hata rahe hain
df.drop(['Item_Identifier', 'Outlet_Identifier'], axis=1, inplace=True)

# 7. Categorical data (text) ko numbers (0, 1) me badal rahe hain Model ke liye
df = pd.get_dummies(df, drop_first=True)

# 8. X me features rakhe, aur y me target (jo predict karna hai - Sales)
X = df.drop('Item_Outlet_Sales', axis=1)
y = df['Item_Outlet_Sales']

# 9. Model ko initialize karke train kar rahe hain
model = RandomForestRegressor()
model.fit(X, y)

# 10. Train kiye hue model ko 'model' folder me save kar rahe hain taaki backend use kar sake
pickle.dump(model, open("model/model.pkl", "wb"))

print("Model ekdum mast train ho gaya aur save ho gaya ✅")