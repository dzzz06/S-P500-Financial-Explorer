# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Page Settings ----
st.set_page_config(page_title="S&P 500 Financial Explorer", layout="wide")

# ---- Title & Intro ----
st.title("📊 S&P 500 Financial Explorer")
st.markdown("""
Analyze financial indicators (P/E, EPS, Market Cap, etc.)  
to explore **valuation differences across industries** and identify **potentially overvalued or growth stocks**.
""")

# ---- Data Load ----
@st.cache_data
def load_data():
    df = pd.read_csv("financials.csv")
    # 清理列名空格，避免筛选报错
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---- Display Columns ----
st.write("📜 Columns in dataset:")
st.write(df.columns.tolist())

# ---- Sidebar ----
st.sidebar.header("🔧 Filters")

# 1️⃣ Select Sector
sector = st.sidebar.selectbox("Select Sector", sorted(df["Sector"].dropna().unique()))

# 2️⃣ Filter by P/E range
pe_min, pe_max = st.sidebar.slider("Select P/E Range", 0.0, 100.0, (0.0, 40.0))

# 3️⃣ Choose Analysis Type
analysis_type = st.sidebar.radio(
    "Choose Analysis Focus",
    ["Industry P/E Comparison", "High P/E Evaluation"]
)

# ---- Filtered Data ----
filtered = df[(df["Sector"] == sector) & (df["Price/Earnings"].between(pe_min, pe_max))]

st.subheader(f"📈 {sector} Sector Companies (P/E {pe_min:.1f}–{pe_max:.1f})")
st.write(f"Number of companies: {len(filtered)}")

# ---- Display scrollable dataframe ----
st.dataframe(
    filtered[["Name", "Price/Earnings", "Earnings/Share", "Market Cap", "Price", "Dividend Yield"]],
    height=450  # 设置表格高度，超出部分可滚动
)

# ---- Visualization ----
st.header("📊 Visual Analysis")

if analysis_type == "Industry P/E Comparison":
    st.markdown("### Comparison of Average P/E Ratios Across Sectors")
    avg_pe = df.groupby("Sector")["Price/Earnings"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=avg_pe.values, y=avg_pe.index, ax=ax, palette="viridis")
    ax.set_xlabel("Average P/E Ratio")
    ax.set_ylabel("Sector")
    st.pyplot(fig)

    st.markdown("""
    **Interpretation:**  
    - Sectors with **higher average P/E** (e.g., Technology, Health Care) may reflect **strong growth expectations**.  
    - Lower P/E sectors (e.g., Energy, Financials) often represent **mature or cyclical industries**.
    -The dataset was last updated in July 2020, right after the COVID-19 shock.The energy sector’s earnings were extremely low while stock prices started to recover, which pushed up the P/E ratio.
    Therefore, the high P/E in the Energy sector reflects temporary earnings drops, not true growth potential.
    """)

elif analysis_type == "High P/E Evaluation":
    st.markdown("### EPS vs P/E — Identifying Overvalued or Growth Stocks")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(
        data=filtered,
        x="Price/Earnings",
        y="Earnings/Share",
        hue="Sector",
        size="Market Cap",
        sizes=(20, 200),
        alpha=0.7,
        ax=ax
    )
    plt.title(f"{sector} Sector: EPS vs P/E")
    st.pyplot(fig)

    st.markdown("""
    **Interpretation:**  
    - **High P/E but low EPS** → possibly **overvalued** stocks.  
    - **High P/E and high EPS** → may indicate **true growth potential**.  
    """)

# ---- Boxplot for P/E Distribution ----
st.markdown("### P/E Distribution by Sector (Boxplot)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x="Sector", y="Price/Earnings", palette="Set3")
plt.xticks(rotation=45)
st.pyplot(fig)

# ---- Summary ----
st.header("💡 Summary Insights")
st.markdown("""
- **Technology and Healthcare sectors** often exhibit high P/E due to future growth expectations.  
- **Energy and Financials** show lower P/E values tied to steady earnings but limited expansion.  
- Comparing **EPS vs P/E** highlights whether valuation premiums are justified by real performance.
""")
