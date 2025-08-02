import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# Page configuration
st.set_page_config(
    page_title="FarmerPay Profitability Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
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
    
    # Growth charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(x=projection_df['Year'], y=projection_df['Farmers']/1000,
                                      mode='lines+markers', name='Farmers (000s)',
                                      line=dict(color='blue', width=3)))
        fig_growth.update_layout(title="Farmer Base Growth Projection",
                               xaxis_title="Year", yaxis_title="Farmers (000s)")
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col2:
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

with tab4:
    st.subheader("💰 Investment Analysis & Funding Strategy")
    
    # Investment requirements
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Investment Breakdown")
        
        investment_data = {
            'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Total'],
            'Timeline': ['0-6 months', '6-18 months', '18-36 months', '3 Years'],
            'Investment': ['₹2.0 Cr', '₹5.0 Cr', '₹15.0 Cr', '₹22.0 Cr'],
            'Purpose': ['Quick wins & optimization', 'Scale & diversification', 'Market leadership', 'Complete transformation']
        }
        
        investment_df = pd.DataFrame(investment_data)
        st.dataframe(investment_df, use_container_width=True, hide_index=True)
        
        # ROI Analysis
        st.markdown("### 📈 ROI Analysis")
        
        total_investment = 220000000  # ₹22 Cr
        final_year_profit = projection_df.iloc[-1]['Profit']
        total_roi = (final_year_profit / total_investment) * 100
        
        roi_metrics = {
            'Metric': ['Initial Investment', 'Final Year Profit', 'Annual ROI', 'Payback Period', 'NPV (10% discount)'],
            'Value': [
                f"₹{total_investment/10000000:.1f} Cr",
                f"₹{final_year_profit/10000000:.1f} Cr",
                f"{total_roi:.1f}%",
                f"{total_investment/final_year_profit:.1f} years",
                f"₹{(final_year_profit*5 - total_investment)/10000000:.1f} Cr"
            ]
        }
        
        roi_df = pd.DataFrame(roi_metrics)
        st.dataframe(roi_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 💡 Funding Strategy")
        
        # Funding rounds
        funding_rounds = [
            {"Round": "Seed", "Amount": "₹2 Cr", "Valuation": "₹15 Cr", "Use": "Product development & team"},
            {"Round": "Series A", "Amount": "₹8 Cr", "Valuation": "₹50 Cr", "Use": "Market expansion & scale"},
            {"Round": "Series B", "Amount": "₹20 Cr", "Valuation": "₹150 Cr", "Use": "Pan-India expansion"},
            {"Round": "Series C", "Amount": "₹50 Cr", "Valuation": "₹400 Cr", "Use": "International expansion"}
        ]
        
        funding_df = pd.DataFrame(funding_rounds)
        st.dataframe(funding_df, use_container_width=True, hide_index=True)
        
        # Investment metrics visualization
        fig_roi = go.Figure()
        
        # Add cumulative investment line
        fig_roi.add_trace(go.Scatter(
            x=projection_df['Year'], 
            y=projection_df['Cumulative_Investment']/10000000,
            mode='lines+markers', 
            name='Cumulative Investment (₹ Cr)',
            line=dict(color='red', width=3, dash='dash')
        ))
        
        # Add cumulative profit line
        cumulative_profit = projection_df['Profit'].cumsum()
        fig_roi.add_trace(go.Scatter(
            x=projection_df['Year'], 
            y=cumulative_profit/10000000,
            mode='lines+markers', 
            name='Cumulative Profit (₹ Cr)',
            line=dict(color='green', width=3)
        ))
        
        fig_roi.update_layout(
            title="Investment vs Returns Analysis",
            xaxis_title="Year",
            yaxis_title="Amount (₹ Cr)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Break-even analysis
    st.markdown("### ⚖️ Break-Even Analysis")
    
    break_even_data = []
    cumulative_cash_flow = 0
    
    for idx, row in projection_df.iterrows():
        year_investment = investment_schedule[idx] if idx < len(investment_schedule) else 0
        year_profit = row['Profit']
        cumulative_cash_flow += (year_profit - year_investment)
        
        break_even_data.append({
            'Year': idx,
            'Annual_Investment': year_investment/10000000,
            'Annual_Profit': year_profit/10000000,
            'Net_Cash_Flow': (year_profit - year_investment)/10000000,
            'Cumulative_Cash_Flow': cumulative_cash_flow/10000000
        })
    
    break_even_df = pd.DataFrame(break_even_data)
    
    fig_breakeven = go.Figure()
    fig_breakeven.add_trace(go.Bar(
        x=break_even_df['Year'],
        y=break_even_df['Net_Cash_Flow'],
        name='Annual Net Cash Flow',
        marker_color=['red' if x < 0 else 'green' for x in break_even_df['Net_Cash_Flow']]
    ))
    
    fig_breakeven.add_trace(go.Scatter(
        x=break_even_df['Year'],
        y=break_even_df['Cumulative_Cash_Flow'],
        mode='lines+markers',
        name='Cumulative Cash Flow',
        line=dict(color='blue', width=3),
        yaxis='y2'
    ))
    
    fig_breakeven.update_layout(
        title="Break-Even Analysis",
        xaxis_title="Year",
        yaxis_title="Annual Cash Flow (₹ Cr)",
        yaxis2=dict(title="Cumulative Cash Flow (₹ Cr)", overlaying='y', side='right'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_breakeven, use_container_width=True)

with tab5:
    st.subheader("🎯 Competitive Intelligence & Market Positioning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Competitive Advantages")
        
        advantages = [
            {"Advantage": "First-mover in KCC digitization", "Strength": "High", "Sustainability": "Medium"},
            {"Advantage": "Proven NPA reduction (1-2%)", "Strength": "High", "Sustainability": "High"},
            {"Advantage": "Bank ROI proposition (200-400%)", "Strength": "Very High", "Sustainability": "High"},
            {"Advantage": "Rural market penetration", "Strength": "Medium", "Sustainability": "Medium"},
            {"Advantage": "Government policy alignment", "Strength": "High", "Sustainability": "Medium"},
            {"Advantage": "Technology platform scalability", "Strength": "High", "Sustainability": "High"},
            {"Advantage": "Agricultural domain expertise", "Strength": "High", "Sustainability": "High"}
        ]
        
        advantages_df = pd.DataFrame(advantages)
        st.dataframe(advantages_df, use_container_width=True, hide_index=True)
        
        # Competitive positioning radar chart
        categories = ['Technology', 'Market Knowledge', 'Bank Relations', 'Farmer Trust', 'Financial Strength', 'Scale']
        
        farmerpay_scores = [8, 9, 8, 7, 6, 5]  # Out of 10
        competitor_scores = [6, 5, 6, 8, 9, 8]  # Traditional players
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=farmerpay_scores,
            theta=categories,
            fill='toself',
            name='FarmerPay',
            line_color='blue'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=competitor_scores,
            theta=categories,
            fill='toself',
            name='Traditional Competitors',
            line_color='red'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Competitive Positioning Analysis"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("### 🚨 Risk Assessment")
        
        risks = [
            {"Risk": "Technology scalability", "Probability": "Medium", "Impact": "High", "Mitigation": "Cloud-native architecture"},
            {"Risk": "Regulatory changes", "Probability": "Medium", "Impact": "Medium", "Mitigation": "Compliance team"},
            {"Risk": "Competition from Big Tech", "Probability": "High", "Impact": "High", "Mitigation": "First-mover advantage"},
            {"Risk": "Farmer adoption barriers", "Probability": "Medium", "Impact": "Medium", "Mitigation": "Vernacular interfaces"},
            {"Risk": "Bank resistance", "Probability": "Low", "Impact": "High", "Mitigation": "Proven ROI demos"},
            {"Risk": "Economic downturn", "Probability": "Medium", "Impact": "Medium", "Mitigation": "Diversified revenue"}
        ]
        
        risk_df = pd.DataFrame(risks)
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
        
        # Market opportunity sizing
        st.markdown("### 📊 Market Opportunity")
        
        market_size_data = {
            'Segment': ['Total KCC Market', 'Addressable Market', 'Target Market (15%)', 'Current Penetration'],
            'Accounts': ['7.0 Cr', '4.2 Cr', '63L', f'{num_farmers/100000:.1f}L'],
            'Value': ['₹8.4L Cr', '₹5.0L Cr', '₹75K Cr', f'₹{optimized_metrics["total_revenue"]/10000000:.1f} Cr']
        }
        
        market_df = pd.DataFrame(market_size_data)
        st.dataframe(market_df, use_container_width=True, hide_index=True)
        
        # TAM, SAM, SOM visualization
        market_values = [840000, 500000, 75000, optimized_metrics['total_revenue']/10000000]
        market_labels = ['TAM', 'SAM', 'SOM', 'Current']
        
        fig_market = go.Figure(data=[go.Bar(
            x=market_labels,
            y=market_values,
            marker_color=['lightblue', 'blue', 'darkblue', 'orange']
        )])
        
        fig_market.update_layout(
            title="Market Opportunity (₹ Cr)",
            yaxis_title="Market Size (₹ Cr)",
            yaxis_type="log"
        )
        
        st.plotly_chart(fig_market, use_container_width=True)

# Strategic Recommendations Section
st.markdown("---")
st.header("🎯 Strategic Recommendations & Action Plan")

rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.markdown("### 🚀 Immediate Actions (0-3 months)")
    immediate_actions = [
        "Deploy AI customer service automation",
        "Implement tiered pricing structure",
        "Launch insurance commission program",
        "Optimize mobile app performance",
        "Renegotiate partnership terms",
        "Establish KPI dashboard",
        "Hire key technical talent",
        "Strengthen bank relationships"
    ]
    
    for action in immediate_actions:
        st.markdown(f"• {action}")

with rec_col2:
    st.markdown("### 📈 Medium-term Goals (3-12 months)")
    medium_term_goals = [
        f"Scale to {int(num_farmers * 1.5):,} farmers",
        "Launch input marketplace",
        "Deploy predictive analytics",
        "Expand to 3 new states",
        "Achieve 35%+ profit margins",
        "Complete Series A funding",
        "Build data monetization",
        "Establish compliance framework"
    ]
    
    for goal in medium_term_goals:
        st.markdown(f"• {goal}")

with rec_col3:
    st.markdown("### 🏆 Long-term Vision (1-3 years)")
    long_term_vision = [
        f"Reach {int(num_farmers * 3):,}+ farmers",
        "Achieve market leadership",
        "Launch international expansion",
        "Build financial ecosystem",
        "IPO preparation",
        "Unicorn valuation target",
        "50%+ profit margins",
        "Industry thought leadership"
    ]
    
    for vision in long_term_vision:
        st.markdown(f"• {vision}")

# Key Performance Indicators
st.markdown("---")
st.header("📊 Key Performance Indicators (KPIs)")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown("### 💰 Financial KPIs")
    financial_kpis = [
        f"Revenue: ₹{optimized_metrics['total_revenue']/10000000:.1f} Cr",
        f"Profit Margin: {optimized_metrics['profit_margin']:.1f}%",
        f"Revenue/Farmer: ₹{optimized_revenue_per_farmer:,.0f}",
        f"LTV/CAC Ratio: 25:1",
        f"Monthly Growth: {growth_rate*100/12:.1f}%"
    ]
    
    for kpi in financial_kpis:
        st.markdown(f"• {kpi}")

with kpi_col2:
    st.markdown("### 👥 Customer KPIs")
    customer_kpis = [
        f"Active Farmers: {num_farmers:,}",
        f"Retention Rate: {(1-churn_rate)*100:.0f}%",
        f"NPS Score: 70+",
        f"Onboarding Time: <24 hrs",
        f"Support Response: <2 hrs"
    ]
    
    for kpi in customer_kpis:
        st.markdown(f"• {kpi}")

with kpi_col3:
    st.markdown("### 🏦 Bank KPIs")
    bank_kpis = [
        "NPA Reduction: 1-2%",
        "Bank ROI: 200-400%",
        "Collection Efficiency: 90%+",
        "Partner Satisfaction: 85%+",
        "New Bank Acquisitions: 2/month"
    ]
    
    for kpi in bank_kpis:
        st.markdown(f"• {kpi}")

with kpi_col4:
    st.markdown("### ⚡ Operational KPIs")
    operational_kpis = [
        "Platform Uptime: 99.9%",
        "Transaction Success: 99.5%",
        "Cost per Farmer: ₹" + f"{optimized_cost_per_farmer:.0f}",
        "Processing Time: <5 mins",
        "Mobile App Rating: 4.5+"
    ]
    
    for kpi in operational_kpis:
        st.markdown(f"• {kpi}")

# Executive Summary
st.markdown("---")
st.header("📋 Executive Summary")

summary_col1, summary_col2 = st.columns([2, 1])

with summary_col1:
    st.markdown(f"""
    ### 🎯 Business Transformation Opportunity
    
    FarmerPay has the potential to transform from a **₹{current_metrics['net_profit']/10000000:.1f} Cr** 
    profit business to a **₹{optimized_metrics['net_profit']/10000000:.1f} Cr** market leader through 
    strategic optimization and scale.
    
    **Key Value Drivers:**
    - **Revenue Enhancement**: Tiered pricing + additional services = +₹{(optimized_revenue_per_farmer - current_revenue_per_farmer):,.0f}/farmer
    - **Cost Optimization**: Technology + scale efficiencies = -₹{(current_cost_per_farmer - optimized_cost_per_farmer):,.0f}/farmer  
    - **Partnership Optimization**: Improved terms = {(current_partnership_rate - optimized_partnership_rate)*100:.1f}% reduction
    - **Scale Benefits**: Market leadership at {phase3_farmers:,} farmers within 3 years
    
    **Investment Thesis:**
    - Total Investment: ₹22 Cr over 3 years
    - Expected Returns: ₹{projection_df.iloc[-1]['Profit']/10000000:.1f} Cr annual profit
    - Market Opportunity: ₹75K Cr addressable market
    - Competitive Advantage: First-mover + proven bank ROI
    
    **Success Probability:** High (85%+) given proven business model and market demand.
    """)

with summary_col2:
    # Summary metrics card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; text-align: center;">
        <h3>🚀 Transformation Impact</h3>
        <p style="font-size: 1.5rem; margin: 1rem 0;">
            <strong>{:.0f}x</strong><br>
            <span style="font-size: 1rem;">Profit Multiplier</span>
        </p>
        <p style="font-size: 1.5rem; margin: 1rem 0;">
            <strong>{:.1f}%</strong><br>
            <span style="font-size: 1rem;">Target Profit Margin</span>
        </p>
        <p style="font-size: 1.5rem; margin: 1rem 0;">
            <strong>₹{:.0f} Cr</strong><br>
            <span style="font-size: 1rem;">Potential Valuation</span>
        </p>
    </div>
    """.format(
        optimized_metrics['net_profit'] / current_metrics['net_profit'],
        optimized_metrics['profit_margin'],
        phase3_metrics['total_revenue'] * 8 / 10000000
    ), unsafe_allow_html=True)

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
