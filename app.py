import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import requests
import time
from streamlit_lottie import st_lottie

# Lottie loader function
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page configuration
st.set_page_config(
    page_title="FarmerPay Profitability Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lottie animation at top
lottie_url = "https://assets8.lottiefiles.com/packages/lf20_4hwj9g4z.json"
lottie_json = load_lottieurl(lottie_url)
if lottie_json:
    st_lottie(lottie_json, speed=1, height=160, key="header_animation")

# Custom CSS for better styling and animations
st.markdown("""
<style>
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(-20px);}
  100% { opacity: 1; transform: translateY(0);}
}
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
    animation: fadeIn 1s ease-in;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
    animation: fadeIn 0.7s ease-in;
}
.improvement-positive {
    color: #28a745;
    font-weight: bold;
}
.improvement-negative {
    color: #dc3545;
    font-weight: bold;
}
.phase-header {
    background: linear-gradient(45deg, #2E8B57, #98FB98);
    padding: 1rem;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    margin: 1rem 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚀 FarmerPay Profitability Optimizer-By B.V.R.C.Purushottam</h1>', unsafe_allow_html=True)
st.markdown("### Advanced Business Intelligence & Strategy Platform")
st.markdown("Optimize FarmerPay's profitability through data-driven insights and strategic planning")

# Animated GIF for section transition
st.image("https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", caption="Business Intelligence in Action")

# Sidebar Configuration
st.sidebar.header("🎯 Strategic Configuration")

# Business Model Selection
business_model = st.sidebar.selectbox(
    "Business Model",
    ["Current Model", "Optimized Model", "Custom Strategy"],
    help="Select the business model to analyze"
)

# Market Scenario
market_scenario = st.sidebar.selectbox(
    "Market Scenario",
    ["Conservative", "Realistic", "Aggressive", "Custom"],
    index=1,
    help="Choose market growth assumptions"
)

# Time Horizon
time_horizon = st.sidebar.selectbox(
    "Analysis Period",
    ["1 Year", "3 Years", "5 Years", "10 Years"],
    index=1,
    help="Select analysis time horizon"
)

st.sidebar.markdown("---")
st.sidebar.header("📊 Business Parameters")

# Core Business Inputs
num_farmers = st.sidebar.number_input(
    "Number of Farmers",
    min_value=1000,
    max_value=10000000,
    value=50000,
    step=5000,
    help="Current or target number of farmers"
)

base_fee = st.sidebar.slider(
    "Base Service Fee (₹)",
    min_value=400,
    max_value=2000,
    value=800,
    step=50,
    help="Annual fee per farmer"
)

# Advanced Strategy Toggles
st.sidebar.markdown("---")
st.sidebar.header("🚀 Strategy Enablers")

enable_tiered_pricing = st.sidebar.checkbox("Tiered Pricing Strategy", value=True)
enable_additional_services = st.sidebar.checkbox("Additional Revenue Streams", value=True)
enable_cost_optimization = st.sidebar.checkbox("Cost Optimization", value=True)
enable_partnership_optimization = st.sidebar.checkbox("Partnership Optimization", value=True)
enable_scale_benefits = st.sidebar.checkbox("Economies of Scale", value=True)

# Scenario-based parameters
if market_scenario == "Conservative":
    growth_rate = 0.25
    market_penetration = 0.08
    churn_rate = 0.15
elif market_scenario == "Realistic":
    growth_rate = 0.50
    market_penetration = 0.15
    churn_rate = 0.10
elif market_scenario == "Aggressive":
    growth_rate = 1.0
    market_penetration = 0.25
    churn_rate = 0.05
else:  # Custom
    growth_rate = st.sidebar.slider("Annual Growth Rate", 0.1, 2.0, 0.5, 0.1)
    market_penetration = st.sidebar.slider("Market Penetration %", 0.05, 0.50, 0.15, 0.01)
    churn_rate = st.sidebar.slider("Churn Rate %", 0.02, 0.30, 0.10, 0.01)

# Business Logic Functions
def calculate_cost_structure(farmers, enable_optimization=False, scale_benefits=False):
    """Calculate cost per farmer based on optimizations"""
    base_service_cost = 400
    base_tech_cost = 100
    
    if enable_optimization:
        # Cost optimization strategies
        service_cost = base_service_cost * 0.75  # 25% reduction through automation
        tech_cost = base_tech_cost * 0.80  # 20% reduction through efficiency
    else:
        service_cost = base_service_cost
        tech_cost = base_tech_cost
    
    if scale_benefits:
        # Economies of scale
        if farmers >= 100000:
            service_cost *= 0.85
            tech_cost *= 0.80
        elif farmers >= 50000:
            service_cost *= 0.90
            tech_cost *= 0.85
        elif farmers >= 25000:
            service_cost *= 0.95
            tech_cost *= 0.90
    
    return service_cost + tech_cost

def calculate_revenue_per_farmer(base_fee, enable_tiered=False, enable_additional=False):
    """Calculate total revenue per farmer"""
    if enable_tiered:
        # Tiered pricing: 60% basic, 30% premium, 10% enterprise
        basic_fee = base_fee * 0.75
        premium_fee = base_fee * 1.25
        enterprise_fee = base_fee * 1.875
        
        weighted_fee = (0.6 * basic_fee) + (0.3 * premium_fee) + (0.1 * enterprise_fee)
    else:
        weighted_fee = base_fee
    
    additional_revenue = 0
    if enable_additional:
        # Additional revenue streams
        insurance_commission = 150
        marketplace_commission = 200
        data_services = 100
        credit_scoring = 80
        weather_services = 50
        training_programs = 120
        
        additional_revenue = (insurance_commission + marketplace_commission + 
                            data_services + credit_scoring + weather_services + training_programs)
    
    return weighted_fee + additional_revenue

def calculate_partnership_rate(enable_optimization=False, farmers=10000):
    """Calculate intermediary payment rate"""
    base_rate = 0.30
    
    if enable_optimization:
        if farmers >= 100000:
            return 0.18  # Strategic partnerships
        elif farmers >= 50000:
            return 0.20  # Tiered model
        elif farmers >= 25000:
            return 0.22  # Performance-based
        else:
            return 0.25  # Improved terms
    
    return base_rate

def calculate_business_metrics(farmers, revenue_per_farmer, cost_per_farmer, partnership_rate):
    """Calculate all business metrics"""
    total_revenue = farmers * revenue_per_farmer
    total_costs = farmers * cost_per_farmer
    gross_profit = total_revenue - total_costs
    intermediary_payment = gross_profit * partnership_rate
    net_profit = gross_profit - intermediary_payment
    
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_costs': total_costs,
        'gross_profit': gross_profit,
        'intermediary_payment': intermediary_payment,
        'net_profit': net_profit,
        'profit_margin': profit_margin,
        'revenue_per_farmer': revenue_per_farmer,
        'cost_per_farmer': cost_per_farmer
    }

def project_multi_year_growth(base_farmers, growth_rate, years, churn_rate):
    """Project farmer growth over multiple years"""
    farmers_projection = []
    current_farmers = base_farmers
    
    for year in range(years + 1):
        if year == 0:
            farmers_projection.append(current_farmers)
        else:
            # Apply growth and subtract churn
            new_farmers = current_farmers * (1 + growth_rate) * (1 - churn_rate)
            farmers_projection.append(int(new_farmers))
            current_farmers = new_farmers
    
    return farmers_projection

# Heavy calculation spinner
with st.spinner("Calculating optimized metrics..."):
    # Calculate Current State
    current_cost_per_farmer = calculate_cost_structure(num_farmers)
    current_revenue_per_farmer = calculate_revenue_per_farmer(base_fee)
    current_partnership_rate = calculate_partnership_rate()
    current_metrics = calculate_business_metrics(num_farmers, current_revenue_per_farmer, 
                                               current_cost_per_farmer, current_partnership_rate)

    # Calculate Optimized State
    optimized_cost_per_farmer = calculate_cost_structure(
        num_farmers, enable_cost_optimization, enable_scale_benefits
    )
    optimized_revenue_per_farmer = calculate_revenue_per_farmer(
        base_fee, enable_tiered_pricing, enable_additional_services
    )
    optimized_partnership_rate = calculate_partnership_rate(enable_partnership_optimization, num_farmers)
    optimized_metrics = calculate_business_metrics(
        num_farmers, optimized_revenue_per_farmer, optimized_cost_per_farmer, optimized_partnership_rate
    )

# Success Lottie animation after optimization
success_lottie_url = "https://assets2.lottiefiles.com/private_files/lf30_ydo1amjm.json"
success_lottie = load_lottieurl(success_lottie_url)
if success_lottie:
    st_lottie(success_lottie, speed=1, height=100, key="success_animation")
st.success("Optimizations applied successfully!")

# Main Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Business Performance Dashboard")
    
    # Key Metrics Comparison
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        profit_improvement = optimized_metrics['net_profit'] - current_metrics['net_profit']
        st.metric(
            "Net Profit",
            f"₹{optimized_metrics['net_profit']/10000000:.1f} Cr",
            delta=f"₹{profit_improvement/10000000:.1f} Cr",
            help="Annual net profit with optimizations"
        )
    
    with metrics_col2:
        margin_improvement = optimized_metrics['profit_margin'] - current_metrics['profit_margin']
        st.metric(
            "Profit Margin",
            f"{optimized_metrics['profit_margin']:.1f}%",
            delta=f"{margin_improvement:.1f}%",
            help="Profit as percentage of revenue"
        )
    
    with metrics_col3:
        revenue_improvement = optimized_metrics['total_revenue'] - current_metrics['total_revenue']
        st.metric(
            "Total Revenue",
            f"₹{optimized_metrics['total_revenue']/10000000:.1f} Cr",
            delta=f"₹{revenue_improvement/10000000:.1f} Cr",
            help="Annual revenue with all strategies"
        )
    
    with metrics_col4:
        partnership_improvement = (current_partnership_rate - optimized_partnership_rate) * 100
        st.metric(
            "Partnership Rate",
            f"{optimized_partnership_rate*100:.1f}%",
            delta=f"-{partnership_improvement:.1f}%",
            help="Intermediary payment rate"
        )

with col2:
    st.subheader("🎯 Strategy Impact")
    
    # Strategy impact breakdown
    impact_data = []
    
    if enable_cost_optimization:
        cost_savings = (current_cost_per_farmer - optimized_cost_per_farmer) * num_farmers
        impact_data.append({"Strategy": "Cost Optimization", "Impact": cost_savings/10000000})
    
    if enable_tiered_pricing or enable_additional_services:
        revenue_increase = (optimized_revenue_per_farmer - current_revenue_per_farmer) * num_farmers
        impact_data.append({"Strategy": "Revenue Enhancement", "Impact": revenue_increase/10000000})
    
    if enable_partnership_optimization:
        partnership_savings = (current_partnership_rate - optimized_partnership_rate) * optimized_metrics['gross_profit']
        impact_data.append({"Strategy": "Partnership Optimization", "Impact": partnership_savings/10000000})
    
    if impact_data:
        impact_df = pd.DataFrame(impact_data)
        fig_impact = px.bar(impact_df, x="Strategy", y="Impact", 
                           title="Strategy Impact (₹ Cr)",
                           color="Impact",
                           color_continuous_scale="viridis")
        fig_impact.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_impact, use_container_width=True)

# Detailed Analysis Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Financial Analysis", 
    "🚀 Strategic Roadmap", 
    "📊 Market Scenarios", 
    "💰 Investment Analysis",
    "🎯 Competitive Intelligence"
])

with tab1:
    st.subheader("📈 Comprehensive Financial Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue breakdown
        revenue_data = {
            'Component': ['Base Fees', 'Premium Tiers', 'Additional Services'],
            'Current': [
                current_revenue_per_farmer * num_farmers,
                0,
                0
            ],
            'Optimized': [
                base_fee * num_farmers * (0.6 * 0.75 + 0.3 * 1.25 + 0.1 * 1.875) if enable_tiered_pricing else base_fee * num_farmers,
                0 if not enable_tiered_pricing else (base_fee * num_farmers * 0.4 * 0.5),
                0 if not enable_additional_services else num_farmers * 700
            ]
        }
        
        revenue_df = pd.DataFrame(revenue_data)
        fig_revenue = px.bar(revenue_df, x='Component', y=['Current', 'Optimized'],
                           title="Revenue Breakdown (₹)",
                           barmode='group')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Cost breakdown
        cost_data = {
            'Component': ['Service Costs', 'Technology Costs', 'Partnership Payments'],
            'Current': [
                400 * num_farmers,
                100 * num_farmers,
                current_metrics['intermediary_payment']
            ],
            'Optimized': [
                (400 * 0.75 if enable_cost_optimization else 400) * num_farmers,
                (100 * 0.80 if enable_cost_optimization else 100) * num_farmers,
                optimized_metrics['intermediary_payment']
            ]
        }
        
        cost_df = pd.DataFrame(cost_data)
        fig_costs = px.bar(cost_df, x='Component', y=['Current', 'Optimized'],
                          title="Cost Breakdown (₹)",
                          barmode='group',
                          color_discrete_map={'Current': '#ff7f7f', 'Optimized': '#90EE90'})
        st.plotly_chart(fig_costs, use_container_width=True)
    
    # Financial projection table
    st.subheader("📋 Financial Summary")
    
    financial_summary = {
        'Metric': [
            'Revenue per Farmer',
            'Cost per Farmer',
            'Gross Profit per Farmer',
            'Net Profit per Farmer',
            'Total Revenue',
            'Total Costs',
            'Total Net Profit',
            'Profit Margin',
            'ROI on Investment'
        ],
        'Current Model': [
            f"₹{current_revenue_per_farmer:,.0f}",
            f"₹{current_cost_per_farmer:,.0f}",
            f"₹{current_revenue_per_farmer - current_cost_per_farmer:,.0f}",
            f"₹{current_metrics['net_profit']/num_farmers:,.0f}",
            f"₹{current_metrics['total_revenue']/10000000:.1f} Cr",
            f"₹{current_metrics['total_costs']/10000000:.1f} Cr",
            f"₹{current_metrics['net_profit']/10000000:.1f} Cr",
            f"{current_metrics['profit_margin']:.1f}%",
            f"{(current_metrics['net_profit']/100000000)*100:.1f}%"
        ],
        'Optimized Model': [
            f"₹{optimized_revenue_per_farmer:,.0f}",
            f"₹{optimized_cost_per_farmer:,.0f}",
            f"₹{optimized_revenue_per_farmer - optimized_cost_per_farmer:,.0f}",
            f"₹{optimized_metrics['net_profit']/num_farmers:,.0f}",
            f"₹{optimized_metrics['total_revenue']/10000000:.1f} Cr",
            f"₹{optimized_metrics['total_costs']/10000000:.1f} Cr",
            f"₹{optimized_metrics['net_profit']/10000000:.1f} Cr",
            f"{optimized_metrics['profit_margin']:.1f}%",
            f"{(optimized_metrics['net_profit']/100000000)*100:.1f}%"
        ],
        'Improvement': [
            f"₹{optimized_revenue_per_farmer - current_revenue_per_farmer:+,.0f}",
            f"₹{optimized_cost_per_farmer - current_cost_per_farmer:+,.0f}",
            f"₹{(optimized_revenue_per_farmer - optimized_cost_per_farmer) - (current_revenue_per_farmer - current_cost_per_farmer):+,.0f}",
            f"₹{(optimized_metrics['net_profit'] - current_metrics['net_profit'])/num_farmers:+,.0f}",
            f"₹{(optimized_metrics['total_revenue'] - current_metrics['total_revenue'])/10000000:+.1f} Cr",
            f"₹{(optimized_metrics['total_costs'] - current_metrics['total_costs'])/10000000:+.1f} Cr",
            f"₹{(optimized_metrics['net_profit'] - current_metrics['net_profit'])/10000000:+.1f} Cr",
            f"{optimized_metrics['profit_margin'] - current_metrics['profit_margin']:+.1f}%",
            f"{((optimized_metrics['net_profit'] - current_metrics['net_profit'])/100000000)*100:+.1f}%"
        ]
    }
    
    summary_df = pd.DataFrame(financial_summary)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("🚀 Strategic Implementation Roadmap")
    
    # Implementation phases
    years = int(time_horizon.split()[0])
    
    st.markdown('<div class="phase-header">Phase 1: Quick Wins (0-6 months)</div>', unsafe_allow_html=True)
    
    phase1_col1, phase1_col2, phase1_col3 = st.columns(3)
    
    with phase1_col1:
        st.metric("Target Farmers", f"{num_farmers:,}")
        st.metric("Expected Revenue", f"₹{optimized_metrics['total_revenue']/10000000:.1f} Cr")
    
    with phase1_col2:
        st.metric("Investment Required", "₹2.0 Cr")
        st.metric("Payback Period", "8.5 months")
    
    with phase1_col3:
        st.metric("ROI", "47.1%")
        st.metric("Risk Level", "Low")
    
    # Phase initiatives
    st.markdown("**Key Initiatives:**")
    initiatives = [
        "✅ Deploy AI-powered customer service automation",
        "✅ Implement tiered pricing strategy",
        "✅ Renegotiate partnership terms",
        "✅ Launch additional revenue streams",
        "✅ Optimize operational costs"
    ]
    
    for initiative in initiatives:
        st.markdown(initiative)
    
    st.markdown('<div class="phase-header">Phase 2: Scale & Diversify (6-18 months)</div>', unsafe_allow_html=True)
    
    phase2_farmers = int(num_farmers * 2.5)
    phase2_metrics = calculate_business_metrics(
        phase2_farmers, 
        optimized_revenue_per_farmer * 1.1,  # 10% premium for scale
        optimized_cost_per_farmer * 0.95,    # 5% cost reduction
        optimized_partnership_rate * 0.9     # 10% better terms
    )
    
    phase2_col1, phase2_col2, phase2_col3 = st.columns(3)
    
    with phase2_col1:
        st.metric("Target Farmers", f"{phase2_farmers:,}")
        st.metric("Expected Revenue", f"₹{phase2_metrics['total_revenue']/10000000:.1f} Cr")
    
    with phase2_col2:
        st.metric("Investment Required", "₹5.0 Cr")
        st.metric("Expected Profit", f"₹{phase2_metrics['net_profit']/10000000:.1f} Cr")
    
    with phase2_col3:
        st.metric("Market Share", f"{phase2_farmers/7000000*100:.1f}%")
        st.metric("Risk Level", "Medium")
    
    st.markdown('<div class="phase-header">Phase 3: Market Leadership (18-36 months)</div>', unsafe_allow_html=True)
    
    phase3_farmers = int(num_farmers * 5)
    phase3_metrics = calculate_business_metrics(
        phase3_farmers,
        optimized_revenue_per_farmer * 1.3,  # 30% premium for advanced services
        optimized_cost_per_farmer * 0.85,    # 15% cost reduction through scale
        optimized_partnership_rate * 0.8     # 20% better terms
    )
    
    phase3_col1, phase3_col2, phase3_col3 = st.columns(3)
    
    with phase3_col1:
        st.metric("Target Farmers", f"{phase3_farmers:,}")
        st.metric("Expected Revenue", f"₹{phase3_metrics['total_revenue']/10000000:.1f} Cr")
    
    with phase3_col2:
        st.metric("Investment Required", "₹15.0 Cr")
        st.metric("Expected Profit", f"₹{phase3_metrics['net_profit']/10000000:.1f} Cr")
    
    with phase3_col3:
        st.metric("Market Share", f"{phase3_farmers/7000000*100:.1f}%")
        st.metric("Valuation Target", f"₹{phase3_metrics['total_revenue']*8/10000000:.0f} Cr")

with tab3:
    st.subheader("📊 Market Scenario Analysis")
    
    # Multi-year projections
    farmer_projections = project_multi_year_growth(num_farmers, growth_rate, years, churn_rate)
    projection_data = []
    cumulative_investment = 0
    investment_schedule = [0, 20000000, 50000000, 150000000, 200000000]  # Investment by year
    
    for year, farmers in enumerate(farmer_projections):
        if year < len(investment_schedule):
            cumulative_investment += investment_schedule[year]
        
        year_revenue_per_farmer = optimized_revenue_per_farmer * (1.05 ** year)  # 5% annual increase
        year_cost_per_farmer = optimized_cost_per_farmer * (0.98 ** year)  # 2% annual decrease
        year_partnership_rate = max(0.15, optimized_partnership_rate * (0.95 ** year))  # Improving terms
        
        year_metrics = calculate_business_metrics(farmers, year_revenue_per_farmer, 
                                                year_cost_per_farmer, year_partnership_rate)
        
        projection_data.append({
            'Year': year,
            'Farmers': farmers,
            'Revenue': year_metrics['total_revenue'],
            'Profit': year_metrics['net_profit'],
            'Profit_Margin': year_metrics['profit_margin'],
            'Cumulative_Investment': cumulative_investment,
            'ROI': (year_metrics['net_profit'] / cumulative_investment * 100) if cumulative_investment > 0 else 0
        })
    
    projection_df = pd.DataFrame(projection_data)
    
    # Animated Plotly Farmer Growth Chart
    farmer_projection_df = pd.DataFrame({
        'Year': list(range(years+1)),
        'Farmers': farmer_projections,
    })

    fig = px.bar(
        farmer_projection_df,
        x="Year",
        y="Farmers",
        animation_frame="Year",
        range_y=[0, max(farmer_projections)*1.2],
        title="Animated Farmer Growth"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Growth charts (financial)
    col1, col2 = st.columns(2)
    with col1:
        fig_financial = go.Figure()
        fig_financial.add_trace(go.Scatter(x=projection_df['Year'], y=projection_df['Revenue']/10000000,
                                         mode='lines+markers', name='Revenue (₹ Cr)',
                                         line=dict(color='green', width=3)))
        fig_financial.add_trace(go.Scatter(x=projection_df['Year'], y=projection_df['Profit']/10000000,
                                         mode='lines+markers', name='Profit (₹ Cr)',
                                         line=dict(color='orange', width=3)))
        fig_financial.update_layout(title="Financial Growth Projection",
                                   xaxis_title="Year", yaxis_title="Amount (₹ Cr)")
        st.plotly_chart(fig_financial, use_container_width=True)
    
    # Scenario comparison table
    st.subheader("🔍 Scenario Comparison")
    
    scenarios = ['Conservative', 'Realistic', 'Aggressive']
    scenario_params = {
        'Conservative': {'growth': 0.25, 'penetration': 0.08, 'churn': 0.15},
        'Realistic': {'growth': 0.50, 'penetration': 0.15, 'churn': 0.10},
        'Aggressive': {'growth': 1.0, 'penetration': 0.25, 'churn': 0.05}
    }
    
    scenario_results = []
    for scenario in scenarios:
        params = scenario_params[scenario]
        final_farmers = num_farmers * ((1 + params['growth']) ** years) * (1 - params['churn'])
        final_revenue = final_farmers * optimized_revenue_per_farmer * (1.05 ** years)
        final_profit = final_revenue * (optimized_metrics['profit_margin'] / 100)
        market_share = final_farmers / 70000000  # Total addressable market
        
        scenario_results.append({
            'Scenario': scenario,
            'Final_Farmers': f"{final_farmers:,.0f}",
            'Final_Revenue': f"₹{final_revenue/10000000:.1f} Cr",
            'Final_Profit': f"₹{final_profit/10000000:.1f} Cr",
            'Market_Share': f"{market_share*100:.1f}%",
            'Valuation': f"₹{final_revenue*8/10000000:.0f} Cr"
        })
    
    scenario_df = pd.DataFrame(scenario_results)
    st.dataframe(scenario_df, use_container_width=True, hide_index=True)

# ... [the rest of the tabs and dashboard as in your original code, unchanged] ...

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-style: italic;">
    <p>🚀 FarmerPay Profitability Optimizer v2.0 | Advanced Business Intelligence Platform</p>
    <p>Built with ❤️ for Agricultural FinTech Innovation</p>
    <p><em>This analysis provides strategic insights based on market data and business modeling. 
    Results may vary based on execution and market conditions.</em></p>
</div>
""", unsafe_allow_html=True)
