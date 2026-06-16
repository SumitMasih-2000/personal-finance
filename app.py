import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import datetime
import io

# =====================================================================
# 1. PAGE CONFIGURATION & PREMIUM CONFIG THEME
# =====================================================================
st.set_page_config(
    page_title="VanguardAI | Personal Finance Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Fintech Theme Palette Constants
COLOR_PRIMARY = "#2563EB"    # Blue
COLOR_SECONDARY = "#10B981"  # Green
COLOR_ACCENT = "#F59E0B"     # Gold
COLOR_DANGER = "#EF4444"     # Red
COLOR_MUTED = "#64748B"      # Gray

def apply_custom_css():
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #F8FAFC;
        }

        /* Top Header Styling */
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.5rem;
        }
        
        .sub-header {
            font-size: 1rem;
            color: #64748B;
            margin-bottom: 2rem;
        }

        /* Premium Card UI Container */
        .metric-card {
            background: #FFFFFF;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #E2E8F0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 1rem;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        .metric-title {
            font-size: 0.875rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #0F172A;
        }

        .metric-delta {
            font-size: 0.875rem;
            margin-top: 0.5rem;
            font-weight: 500;
        }
        
        .delta-positive { color: #10B981; }
        .delta-negative { color: #EF4444; }

        /* AI Insights block styling */
        .ai-card {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 5px solid #2563EB;
            padding: 1.25rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

apply_custom_css()

# =====================================================================
# 2. DATA LAYER & REALISTIC SAMPLE ENGINE
# =====================================================================
def generate_sample_data():
    """Generates an extensive, highly realistic 12-month financial dataset matching specification blueprints."""
    np.random.seed(42)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = []
    income_sources = ['Primary Salary', 'Freelance/Consulting', 'Dividends']
    categories = {
        'Housing': ['Rent', 'Mortgage', 'Utilities', 'Maintenance'],
        'Food': ['Groceries', 'Restaurants', 'Delivery'],
        'Transportation': ['Fuel', 'Public Transit', 'Uber/Lyft', 'Car Insurance'],
        'Entertainment': ['Streaming', 'Movies', 'Concerts', 'Gaming'],
        'Shopping': ['Clothing', 'Electronics', 'Home Goods'],
        'Healthcare': ['Insurance', 'Pharmacy', 'Doctor Visit']
    }
    investment_types = ['Stocks (S&P 500)', 'Crypto', 'Real Estate (REITs)', 'Bonds']
    goals = ['Emergency Fund', 'New Vehicle Fund', 'Retirement', 'House Down-payment']
    
    for date in dates:
        # 1. Income Generation (Monthly recurring & random freelance)
        if date.day == 1:
            data.append([date, 'Income', 'Salary', 'Primary', 'Monthly Paycheck', 6500.00, 'Primary Salary', 0, 'None', 'None'])
        if date.day == 15 and np.random.rand() > 0.4:
            data.append([date, 'Income', 'Freelance', 'Consulting', 'Client Project Milestone', np.random.uniform(800, 2200), 'Freelance/Consulting', 0, 'None', 'None'])
        if date.day == 28:
            data.append([date, 'Income', 'Investments', 'Dividends', 'Quarterly Dividend Payout', np.random.uniform(150, 400), 'Dividends', 0, 'None', 'None'])
            
        # 2. Expense Generation
        if date.day == 2:
            data.append([date, 'Expense', 'Housing', 'Rent', 'Monthly Housing Payment', 1800.00, 'None', 1800.00, 'None', 'None'])
            data.append([date, 'Expense', 'Housing', 'Utilities', 'Electric & Water Bills', 220.00, 'None', 250.00, 'None', 'None'])
            
        if np.random.rand() > 0.3:  # 70% daily variable expense footprint
            cat = np.random.choice(list(categories.keys()))
            sub_cat = np.random.choice(categories[cat])
            amt = np.round(np.random.exponential(scale=45.0) + 5, 2)
            budget_limit = 600.00 if cat in ['Food', 'Shopping'] else 300.00
            data.append([date, 'Expense', cat, sub_cat, f"Purchase at {sub_cat} vendor", amt, 'None', budget_limit, 'None', 'None'])
            
        # 3. Monthly Savings / Investment allocations
        if date.day == 5:
            inv_type = np.random.choice(investment_types)
            inv_amt = np.random.uniform(500, 1200)
            data.append([date, 'Investment', 'Investing', inv_type, f"Automated Buy: {inv_type}", inv_amt, 'None', 0, inv_type, 'None'])
            
        if date.day == 10:
            goal = np.random.choice(goals)
            goal_amt = np.random.uniform(250, 600)
            data.append([date, 'Savings', 'Goal Transfer', goal, f"Contribution to {goal}", goal_amt, 'None', 0, 'None', goal])

    df = pd.DataFrame(data, columns=[
        'Date', 'Transaction Type', 'Category', 'Sub Category', 
        'Description', 'Amount', 'Income Source', 'Budget', 'Investment Type', 'Goal Name'
    ])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def validate_and_process_upload(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        required_cols = ['Date', 'Transaction Type', 'Category', 'Amount']
        for col in required_cols:
            if col not in df.columns:
                return None, f"Missing critical column: {col}"
                
        df['Date'] = pd.to_datetime(df['Date'])
        return df, "Success"
    except Exception as e:
        return None, str(e)

# Initialize Session State
if 'fin_data' not in st.session_state:
    st.session_state['fin_data'] = generate_sample_data()

# =====================================================================
# 3. SIDEBAR NAVIGATION & FILTERS
# =====================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#2563EB; font-weight:700;'>💼 VanguardAI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#64748B;'>Premium Financial Hub</p>", unsafe_allow_html=True)
    st.hr()
    
    menu = st.radio(
        "Navigation Menu",
        [
            "Executive Summary", 
            "Expense Deep-dive", 
            "Income Portfolio", 
            "Budget & Alerts", 
            "Savings & Allocations", 
            "Investments Workspace", 
            "Goal Milestones", 
            "AI Advisory & Engine", 
            "Data Export Hub"
        ]
    )
    
    st.hr()
    st.markdown("### Data Upload Engine")
    uploaded_file = st.file_uploader("Upload CSV/Excel Statements", type=['csv', 'xlsx'])
    if uploaded_file:
        df, msg = validate_and_process_upload(uploaded_file)
        if df is not None:
            st.session_state['fin_data'] = df
            st.sidebar.success("Database sync initialized successfully!")
        else:
            st.sidebar.error(f"Synchronization failure: {msg}")

# Setup data manipulation references
df_main = st.session_state['fin_data'].copy()

st.sidebar.markdown("### Global Range Filter")
min_date = df_main['Date'].min().to_pydatetime()
max_date = df_main['Date'].max().to_pydatetime()
date_range = st.sidebar.date_input("Select Analysis Window", [min_date, max_date], min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start_dt, end_dt = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df_filtered = df_main[(df_main['Date'] >= start_dt) & (df_main['Date'] <= end_dt)]
else:
    df_filtered = df_main

search_query = st.sidebar.text_input("🔍 Omni-Search Transactions", "")
if search_query:
    df_filtered = df_filtered[
        df_filtered['Description'].str.contains(search_query, case=False, na=False) |
        df_filtered['Category'].str.contains(search_query, case=False, na=False)
    ]

# Helper function to generate cards
def build_custom_card(title, value, delta_text="", is_positive=True):
    delta_class = "delta-positive" if is_positive else "delta-negative"
    sign = "+" if is_positive and delta_text else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta {delta_class}">{sign}{delta_text}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# 4. DASHBOARD VIEW CONTROLLERS
# =====================================================================

# --- EXECUTIVE SUMMARY ---
if menu == "Executive Summary":
    st.markdown('<div class="main-header">Executive Financial Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Holistic high-level diagnostics of aggregate system inflows, structural burns, and equity indices.</div>', unsafe_allow_html=True)
    
    inc = df_filtered[df_filtered['Transaction Type'] == 'Income']['Amount'].sum()
    exp = df_filtered[df_filtered['Transaction Type'] == 'Expense']['Amount'].sum()
    inv = df_filtered[df_filtered['Transaction Type'] == 'Investment']['Amount'].sum()
    sav = inc - exp
    sav_rate = (sav / inc * 100) if inc > 0 else 0
    net_worth = inc + inv - exp
    health_score = int(max(30, min(100, (sav_rate * 1.5) + (70 if exp < inc else 20))))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        build_custom_card("Total Aggregate Income", f"${inc:,.2f}", "vs prior month up 4.2%", True)
    with col2:
        build_custom_card("Total Structural Burn", f"${exp:,.2f}", "vs prior month down 1.1%", True)
    with col3:
        build_custom_card("Net Capital Savings", f"${sav:,.2f}", f"Savings Rate: {sav_rate:.1f}%", sav_rate > 20)
    with col4:
        build_custom_card("Calculated Net Worth Asset Class", f"${net_worth:,.2f}", f"Health Score Index: {health_score}/100", health_score > 70)

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("### Liquidity Cash Flow Analysis & Structural Burns")
        df_cf = df_filtered[df_filtered['Transaction Type'].isin(['Income', 'Expense'])].groupby([pd.Grouper(key='Date', freq='ME'), 'Transaction Type'])['Amount'].sum().unstack().fillna(0)
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Scatter(x=df_cf.index, y=df_cf['Income'], name='Inflow Portfolio', line=dict(color=COLOR_SECONDARY, width=3), stackgroup='one'))
        fig_cf.add_trace(go.Scatter(x=df_cf.index, y=df_cf['Expense'], name='Outflow Portfolio', line=dict(color=COLOR_DANGER, width=3)))
        fig_cf.update_layout(template='plotly_white', margin=dict(l=20,r=20,t=20,b=20), height=350)
        st.plotly_chart(fig_cf, use_container_width=True)
        
    with col_right:
        st.markdown("### Operational Scorecard")
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Financial Health Matrix", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': COLOR_PRIMARY},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#FFE4E6'},
                    {'range': [50, 80], 'color': '#FEF3C7'},
                    {'range': [80, 100], 'color': '#D1FAE5'}],
            }
        ))
        fig_g.update_layout(margin=dict(l=20,r=20,t=40,b=20), height=320)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("### Enterprise System Inflows and Outflows (Sankey Matrix)")
    df_exp_cat = df_filtered[df_filtered['Transaction Type'] == 'Expense'].groupby('Category')['Amount'].sum().reset_index()
    df_inc_cat = df_filtered[df_filtered['Transaction Type'] == 'Income'].groupby('Category')['Amount'].sum().reset_index()
    
    nodes = ["Total Budget Inflow"] + list(df_inc_cat['Category']) + ["Operational Wallet"] + list(df_exp_cat['Category']) + ["Retained Capital"]
    links = []
    
    for idx, row in df_inc_cat.iterrows():
        links.append({'source': nodes.index(row['Category']), 'target': nodes.index("Operational Wallet"), 'value': row['Amount']})
    for idx, row in df_exp_cat.iterrows():
        links.append({'source': nodes.index("Operational Wallet"), 'target': nodes.index(row['Category']), 'value': row['Amount']})
    if sav > 0:
        links.append({'source': nodes.index("Operational Wallet"), 'target': nodes.index("Retained Capital"), 'value': sav})
        
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes, color=COLOR_PRIMARY),
        link=dict(source=[l['source'] for l in links], target=[l['target'] for l in links], value=[l['value'] for l in links], color="#E2E8F0")
    )])
    fig_sankey.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=400)
    st.plotly_chart(fig_sankey, use_container_width=True)

# --- EXPENSE DEEP-DIVE ---
elif menu == "Expense Deep-dive":
    st.markdown('<div class="main-header">Expense Analytics Engines</div>', unsafe_allow_html=True)
    df_exp = df_filtered[df_filtered['Transaction Type'] == 'Expense']
    
    selected_cats = st.multiselect("Filter Analysis Categories", options=df_exp['Category'].unique(), default=df_exp['Category'].unique()[:3])
    if selected_cats:
        df_exp = df_exp[df_exp['Category'].isin(selected_cats)]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Category Distribution Weights")
        fig_don = px.pie(df_exp, values='Amount', names='Category', hole=0.5, color_discrete_sequence=px.colors.qualitative.Safe)
        fig_don.update_layout(margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_don, use_container_width=True)
    with col2:
        st.markdown("### Structural Allocation Breakdown (Treemap Matrix)")
        fig_tree = px.treemap(df_exp, path=['Category', 'Sub Category'], values='Amount', color='Amount', color_continuous_scale='Blues')
        fig_tree.update_layout(margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")
    st.markdown("### Temporal System Outflow Density Heatmap")
    df_exp = df_exp.copy()
    df_exp['DayOfWeek'] = df_exp['Date'].dt.day_name()
    df_exp['Month'] = df_exp['Date'].dt.strftime('%b %Y')
    df_hm = df_exp.groupby(['DayOfWeek', 'Month'])['Amount'].sum().unstack().fillna(0)
    
    fig_hm = px.imshow(df_hm, labels=dict(x="Timeline Window", y="Weekday Framework", color="Scale Value ($)"), color_continuous_scale='YlOrRd')
    fig_hm.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=350)
    st.plotly_chart(fig_hm, use_container_width=True)

# --- INCOME PORTFOLIO ---
elif menu == "Income Portfolio":
    st.markdown('<div class="main-header">Inflow Channels & Growth Analysis</div>', unsafe_allow_html=True)
    df_inc = df_filtered[df_filtered['Transaction Type'] == 'Income']
    
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown("### Inflow Core Contributors")
        fig_inc_pie = px.pie(df_inc, values='Amount', names='Income Source', color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT])
        st.plotly_chart(fig_inc_pie, use_container_width=True)
        
    with col_r:
        st.markdown("### Monthly Inflow Streams Stack Structure")
        df_inc_m = df_inc.groupby([pd.Grouper(key='Date', freq='ME'), 'Income Source'])['Amount'].sum().unstack().fillna(0)
        fig_inc_bar = px.bar(df_inc_m, x=df_inc_m.index, y=df_inc_m.columns, color_discrete_sequence=px.colors.qualitative.Prism)
        fig_inc_bar.update_layout(template='plotly_white', barmode='stack', margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_inc_bar, use_container_width=True)

# --- BUDGET & ALERTS ---
elif menu == "Budget & Alerts":
    st.markdown('<div class="main-header">Operational Budget Engine Matrix</div>', unsafe_allow_html=True)
    
    df_budget = df_filtered[df_filtered['Transaction Type'] == 'Expense'].groupby('Category').agg({'Amount':'sum', 'Budget':'first'}).reset_index()
    df_budget['Budget'] = df_budget['Budget'].apply(lambda x: x if x > 0 else 1200.0)
    df_budget['Utilization (%)'] = (df_budget['Amount'] / df_budget['Budget']) * 100
    df_budget['Remaining Balance'] = df_budget['Budget'] - df_budget['Amount']
    
    st.markdown("### Core Threshold Allocations vs Actual Footprints")
    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(name='Target Budget Constraint', x=df_budget['Category'], y=df_budget['Budget'], marker_color='#CBD5E1'))
    fig_b.add_trace(go.Bar(name='Realized Spending', x=df_budget['Category'], y=df_budget['Amount'], marker_color=COLOR_PRIMARY))
    fig_b.update_layout(barmode='group', template='plotly_white', margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fig_b, use_container_width=True)
    
    st.markdown("### System Alert Notifications")
    for idx, row in df_budget.iterrows():
        if row['Utilization (%)'] > 100:
            st.error(f"🚨 **Critical Overrun Alert**: The category **{row['Category']}** has exceeded constraints by **{row['Utilization (%)']-100:.1f}%** (Deficit: ${abs(row['Remaining Balance']):,.2f})")
        elif row['Utilization (%)'] > 85:
            st.warning(f"⚠️ **Pre-Overrun Buffer Reached**: **{row['Category']}** utilization index is tracking high at **{row['Utilization (%)']:.1f}%** (Remaining: ${row['Remaining Balance']:,.2f})")
            
    st.dataframe(df_budget.style.format({'Amount': '${:,.2f}', 'Budget': '${:,.2f}', 'Utilization (%)': '{:.1f}%', 'Remaining Balance': '${:,.2f}'}), use_container_width=True)

# --- SAVINGS & ALLOCATIONS ---
elif menu == "Savings & Allocations":
    st.markdown('<div class="main-header">Capital Savings & Projections</div>', unsafe_allow_html=True)
    
    df_sav = df_filtered[df_filtered['Transaction Type'] == 'Savings']
    df_sav_m = df_sav.groupby(pd.Grouper(key='Date', freq='ME'))['Amount'].sum().reset_index()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Temporal Accumulated Savings Trajectory")
        df_sav_m['Cumulative'] = df_sav_m['Amount'].cumsum()
        fig_cum = px.area(df_sav_m, x='Date', y='Cumulative', color_discrete_sequence=[COLOR_SECONDARY])
        fig_cum.update_layout(template='plotly_white')
        st.plotly_chart(fig_cum, use_container_width=True)
    with col2:
        st.markdown("### Emergency Guardrails")
        current_reserve = df_sav_m['Amount'].sum()
        target_reserve = 25000.00
        progress_pct = min(100.0, (current_reserve / target_reserve) * 100)
        
        st.metric("Total Liquid Emergency Capital", f"${current_reserve:,.2f}")
        st.metric("Target Guardrail Reserve Index", f"${target_reserve:,.2f}")
        st.progress(progress_pct / 100.0)
        st.markdown(f"**{progress_pct:.1f}%** of core 6-month structural protection asset target reached.")

# --- INVESTMENTS WORKSPACE ---
elif menu == "Investments Workspace":
    st.markdown('<div class="main-header">Investment Portfolio Management</div>', unsafe_allow_html=True)
    df_inv = df_filtered[df_filtered['Transaction Type'] == 'Investment']
    df_inv_group = df_inv.groupby('Investment Type')['Amount'].sum().reset_index()
    
    cl, cr = st.columns(2)
    with cl:
        st.markdown("### Asset Allocation Footprint")
        fig_inv_p = px.pie(df_inv_group, values='Amount', names='Investment Type', color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig_inv_p, use_container_width=True)
    with cr:
        st.markdown("### Portfolio Growth Footprint")
        df_inv_t = df_inv.groupby([pd.Grouper(key='Date', freq='ME'), 'Investment Type'])['Amount'].sum().unstack().fillna(0).cumsum()
        fig_inv_l = px.line(df_inv_t, x=df_inv_t.index, y=df_inv_t.columns)
        fig_inv_l.update_layout(template='plotly_white')
        st.plotly_chart(fig_inv_l, use_container_width=True)

# --- GOAL MILESTONES ---
elif menu == "Goal Milestones":
    st.markdown('<div class="main-header">Target Goal Trackers & Milestone Engine</div>', unsafe_allow_html=True)
    df_goals = df_filtered[df_filtered['Transaction Type'] == 'Savings'].groupby('Goal Name')['Amount'].sum().reset_index()
    df_goals = df_goals[df_goals['Goal Name'] != 'None']
    
    targets = {'Emergency Fund': 20000, 'New Vehicle Fund': 15000, 'Retirement': 100000, 'House Down-payment': 75000}
    df_goals['Target Mapping'] = df_goals['Goal Name'].map(targets).fillna(50000)
    df_goals['Progress Scale (%)'] = (df_goals['Amount'] / df_goals['Target Mapping']) * 100
    
    for idx, row in df_goals.iterrows():
        st.markdown(f"#### 🎯 {row['Goal Name']}")
        st.progress(min(1.0, row['Progress Scale (%)']/100.0))
        st.markdown(f"Allocated: **${row['Amount']:,.2f}** / Target Threshold: **${row['Target Mapping']:,.2f}** ({row['Progress Scale (%)']:.1f}% Completed)")
        st.markdown("---")

# --- AI ADVISORY ENGINE & PREDICTIONS ---
elif menu == "AI Advisory & Engine":
    st.markdown('<div class="main-header">Predictive Modeling & AI Core Advisory</div>', unsafe_allow_html=True)
    
    st.markdown("### 📈 Machine Learning Future Projections (180-Day Linear Model)")
    df_cf_m = df_filtered[df_filtered['Transaction Type'] == 'Expense'].groupby(pd.Grouper(key='Date', freq='ME'))['Amount'].sum().reset_index()
    
    if len(df_cf_m) > 3:
        df_cf_m['Ordinal_Date'] = df_cf_m['Date'].map(datetime.date.toordinal)
        X = df_cf_m[['Ordinal_Date']].values
        y = df_cf_m['Amount'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_dates = pd.date_range(df_cf_m['Date'].max(), periods=6, freq='ME')
        future_ordinals = np.array([d.to_pydatetime().toordinal() for d in future_dates]).reshape(-1, 1)
        predictions = model.predict(future_ordinals)
        
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=df_cf_m['Date'], y=y, name='Historical Realized Spending', line=dict(color=COLOR_PRIMARY, width=3)))
        fig_pred.add_trace(go.Scatter(x=future_dates, y=predictions, name='ML Regressive Trend Projection', line=dict(color=COLOR_ACCENT, dash='dash', width=3)))
        fig_pred.update_layout(template='plotly_white', margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_pred, use_container_width=True)
    else:
        st.info("Insufficient chronological timeline steps available to execute predictive regression algorithms. Broaden global dates via the sidebar context framework.")

    st.markdown("### 🤖 Diagnostic System Audit Logs")
    inc_sum = df_filtered[df_filtered['Transaction Type'] == 'Income']['Amount'].sum()
    exp_sum = df_filtered[df_filtered['Transaction Type'] == 'Expense']['Amount'].sum()
    dining_burn = df_filtered[(df_filtered['Category'] == 'Food') & (df_filtered['Transaction Type'] == 'Expense')]['Amount'].sum()
    
    st.markdown("""
    <div class="ai-card">
        <h4>💡 System Diagnostic Audit Portfolio</h4>
        <p>Our analytics engine compiled system vectors against typical optimizing parameters to form immediate directives:</p>
    </div>
    """, unsafe_allow_html=True)
    
    if dining_burn > (0.15 * inc_sum):
        st.markdown(f"* 🚨 **Outflow Optimization Warning**: Food & Restaurant structural burn accounts for **{(dining_burn/inc_sum)*100:.1f}%** of absolute systems incoming equity. Scaledown parameters target a saving velocity boost of ${dining_burn*0.2:,.2f} per calendar block.")
    if exp_sum > (inc_sum * 0.8):
        st.markdown("* ⚠️ **High Burn Runway Matrix**: Current operational frameworks burn over 80% of top-line velocity. Consider pausing alternative non-essential channels.")
    else:
        st.markdown(f"* 💎 **Capital Efficiency Status Verified**: Asset capture metrics are highly resilient. Remaining liquidity engine metrics suggest transferring additional buffer fields into active dividend systems.")

# --- DATA EXPORT HUB ---
elif menu == "Data Export Hub":
    st.markdown('<div class="main-header">System Extraction & Ledger Reports</div>', unsafe_allow_html=True)
    st.markdown("Export active transactional frameworks across compliance formats below.")
    
    st.markdown("### Ledger Data view")
    st.dataframe(df_filtered, use_container_width=True)
    
    csv_buffer = io.StringIO()
    df_filtered.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    
    st.download_button(
        label="📥 Download Certified CSV Ledger",
        data=csv_bytes,
        file_name="VanguardAI_Ledger_Export.csv",
        mime="text/csv"
    )
