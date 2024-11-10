import streamlit as st

def step_1():
    st.title("Step 1: Brokerage Account Details")
    c1, c2, c3, c4 = st.columns(4)
    c5, c6, c7, c8 = st.columns(4)

    with c1:
        BA_Name = st.text_input("BrokerageAccount")
    with c2:
        BA_SnapshotDate = st.text_input("SnapshotDate")
    with c3:
        BA_TotalCostBasis = st.text_input("TotalCostBasis")
    with c4:        
        BA_TotalMarketValue = st.text_input("TotalMarketValue")
    with c5:
        BA_Cash = st.text_input("Cash")                
    with c6:
        BA_MarginDebt = st.text_input("MarginDebt")                
    with c7:
        BA_TotalProfitLoss = st.text_input("TotalProfitLoss")
    with c8:
        BA_TotalAccountValue = st.text_input("TotalAccountValue")

#        txtMarginBuyingPower = st.text_input("Margin Buying Power")

#        txtDayTradeBuyingPower = st.text_input("Day Trade Buying Power")
    return BA_Name, BA_SnapshotDate, BA_TotalCostBasis, BA_TotalMarketValue, BA_Cash, BA_MarginDebt, BA_TotalProfitLoss, BA_TotalAccountValue


def step_2():
    st.title("Step 2: Table Details")
    schema = st.text_input("Schema")
    table = st.text_input("Table Name")
    
    return schema, table

def step_3():
    st.title("Step 3: Upload CSV")
    csv_file = st.file_uploader("Choose a CSV file")
    
def reset():
    username, password, account, warehouse = "", "", "", ""
    schema, table = "", ""
    csv_file = None

def main():
    st.sidebar.title("Brokerage Account Details")
    current_step = st.sidebar.selectbox("Step", ["Step 1", "Step 2", "Step 3"])
    
    
    if current_step == "Step 1":
        BA_Name, BA_SnapshotDate, BA_TotalCostBasis, BA_TotalMarketValue, BA_Cash, BA_MarginDebt, BA_TotalProfitLoss, BA_TotalAccountValue = step_1()        
    
    elif current_step == "Step 2":
        schema, table = step_2()
        
    
    elif current_step == "Step 3":
        csv_file = step_3()
        next_step_button = st.sidebar.button("Submit")
    
    
    if st.sidebar.button("Reset", key="reset"):
        username, password, account, warehouse = "", "", "", ""
        schema, table = "", ""
        csv_file = None

main()