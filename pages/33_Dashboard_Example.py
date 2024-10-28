import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the dashboard
st.title("📊 Interactive Streamlit Dashboard")

# Sidebar - User input
st.title("⚙️ Control Panel")
st.markdown("Use the options below to customize your view.")

# Data selection dropdown
data_type = st.selectbox("Select Dataset", ["Sample Data 1", "Sample Data 2", "Upload Your Data"])

# Upload data section
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Data processing and display
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if data_type == "Upload Your Data" and uploaded_file is not None:
    data = load_data(uploaded_file)
else:
    # Sample datasets
    data = pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Values": [23, 45, 56, 78]
    })

# Display the dataset
st.write("### 📈 Data Overview")
st.dataframe(data)

# Chart selection and display
st.write("### 📊 Data Visualization")

chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"])

if chart_type == "Bar Chart":
    fig, ax = plt.subplots()
    ax.bar(data["Category"], data["Values"], color='skyblue')
    st.pyplot(fig)
elif chart_type == "Line Chart":
    fig, ax = plt.subplots()
    ax.plot(data["Category"], data["Values"], marker='o')
    st.pyplot(fig)
elif chart_type == "Pie Chart":
    fig, ax = plt.subplots()
    ax.pie(data["Values"], labels=data["Category"], autopct='%1.1f%%')
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Created with 💻 by [Your Name]")

st.markdown("**Note:** This dashboard is an interactive tool. Use the sidebar to explore the data!")
