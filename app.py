
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Bank Profitability Analysis Calculator",
    page_icon="🏦",
    layout="wide"
)

# Title and description
st.title("🏦 Bank Profitability Analysis Calculator")
st.markdown("### Dynamic NPA-based KCC Loan Profitability Analysis")
st.markdown("This calculator analyzes bank profitability for Kisan Credit Card (KCC) loans based on NPA rates and other financial parameters.")

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")

# Bank type selection
bank_type = st.sidebar.selectbox(
    "Select Bank Type",
    ["Scheduled Commercial Banks (SCBs)", "Regional Rural Banks (RRBs)", "Cooperative Banks"],
    help="Different bank types have different operational characteristics and baseline metrics"
)

# Input fields
npa_rate = st.sidebar.slider(
    "NPA Rate (%)",
    min_value=0.0,
    max_value=30.0,
    value=14.16 if bank_type == "Scheduled Commercial Banks (SCBs)" else 7.1 if bank_type == "Regional Rural Banks (RRBs)" else 6.5,
    step=0.1,
    help="Non-Performing Assets rate as a percentage"
)

loan_amount = st.sidebar.number_input(
    "KCC Loan Amount (₹)",
    min_value=10000,
    max_value=10000000,
    value=120000,
    step=10000,
    help="Kisan Credit Card loan amount in Indian Rupees"
)

interest_rate = st.sidebar.slider(
    "Interest Rate (%)",
    min_value=1.0,
    max_value=15.0,
    value=7.0,
    step=0.1,
    help="Annual interest rate for the KCC loan"
)

# FarmerPay Analysis Toggle
st.sidebar.markdown("---")
st.sidebar.header("🚀 FarmerPay Analysis")

include_farmerpay = st.sidebar.checkbox(
    "Include FarmerPay Analysis",
    value=True,
    help="Compare current state with FarmerPay integration benefits"
)

# Number of farmers input - moved to top
if include_farmerpay:
    num_farmers = st.sidebar.number_input(
        "Number of Farmers",
        min_value=1000,
        max_value=2500000,
        value=10000,
        step=1000,
        help="Total number of farmers using FarmerPay services"
    )
    st.sidebar.markdown("---")

if include_farmerpay:
    # Tiered Pricing Strategy
    st.sidebar.subheader("💰 Tiered Pricing Strategy")
    
    # Basic tier settings
    basic_tier_percentage = st.sidebar.slider(
        "Basic Tier (% of users)",
        min_value=40,
        max_value=80,
        value=60,
        step=5,
        help="Percentage of users in Basic tier (Core KCC services)"
    )
    
    basic_tier_price = st.sidebar.slider(
        "Basic Tier Price (₹)",
        min_value=400,
        max_value=800,
        value=600,
        step=20,
        help="Annual fee for Basic tier - Core KCC services"
    )
    
    # Premium tier settings
    premium_tier_percentage = st.sidebar.slider(
        "Premium Tier (% of users)",
        min_value=20,
        max_value=40,
        value=30,
        step=5,
        help="Percentage of users in Premium tier (Enhanced analytics + insurance)"
    )
    
    premium_tier_price = st.sidebar.slider(
        "Premium Tier Price (₹)",
        min_value=800,
        max_value=1400,
        value=1000,
        step=20,
        help="Annual fee for Premium tier - Enhanced analytics + insurance"
    )
    
    # Enterprise tier (calculated automatically)
    enterprise_tier_percentage = 100 - basic_tier_percentage - premium_tier_percentage
    
    enterprise_tier_price = st.sidebar.slider(
        "Enterprise Tier Price (₹)",
        min_value=1200,
        max_value=2000,
        value=1500,
        step=20,
        help="Annual fee for Enterprise tier - Full financial ecosystem"
    )
    
    st.sidebar.caption(f"Enterprise Tier: {enterprise_tier_percentage}% of users (auto-calculated)")
    
    # Calculate weighted average fee
    farmerpay_fee = (
        (basic_tier_percentage / 100) * basic_tier_price +
        (premium_tier_percentage / 100) * premium_tier_price +
        (enterprise_tier_percentage / 100) * enterprise_tier_price
    )
    
    st.sidebar.metric("Weighted Average Fee", f"₹{farmerpay_fee:.0f}")
    
    # Additional Revenue Streams
    st.sidebar.subheader("💼 Additional Revenue Streams")
    
    insurance_commission = st.sidebar.slider(
        "Insurance Commissions (₹/farmer)",
        min_value=100,
        max_value=200,
        value=150,
        step=20,
        help="Revenue from insurance product commissions per farmer"
    )
    
    marketplace_commission = st.sidebar.slider(
        "Input Marketplace Commissions (₹/farmer)",
        min_value=150,
        max_value=250,
        value=200,
        step=20,
        help="Revenue from agricultural input marketplace commissions"
    )
    
    data_analytics_revenue = st.sidebar.slider(
        "Data Analytics Services (₹/farmer)",
        min_value=80,
        max_value=120,
        value=100,
        step=20,
        help="Revenue from data analytics and insights services"
    )
    
    credit_scoring_revenue = st.sidebar.slider(
        "Credit Scoring Services (₹/farmer)",
        min_value=60,
        max_value=100,
        value=80,
        step=20,
        help="Revenue from credit scoring and assessment services"
    )
    
    weather_advisory_revenue = st.sidebar.slider(
        "Weather Advisory (₹/farmer)",
        min_value=30,
        max_value=70,
        value=50,
        step=20,
        help="Revenue from weather advisory and alerts services"
    )
    
    training_programs_revenue = st.sidebar.slider(
        "Training Programs (₹/farmer)",
        min_value=100,
        max_value=140,
        value=120,
        step=20,
        help="Revenue from agricultural training and education programs"
    )
    
    # Calculate total additional revenue
    additional_revenue_per_farmer = (
        insurance_commission + marketplace_commission + data_analytics_revenue +
        credit_scoring_revenue + weather_advisory_revenue + training_programs_revenue
    )
    
    st.sidebar.metric("Additional Revenue per Farmer", f"₹{additional_revenue_per_farmer:.0f}")
    
    # Total revenue per farmer (core + additional)
    total_revenue_per_farmer = farmerpay_fee + additional_revenue_per_farmer
    st.sidebar.metric("Total Revenue per Farmer", f"₹{total_revenue_per_farmer:.0f}")
else:
    # Set default values when FarmerPay analysis is not included
    farmerpay_fee = 0
    num_farmers = 0
    total_revenue_per_farmer = 0
    additional_revenue_per_farmer = 0


# Define bank-specific parameters
def get_bank_parameters(bank_type, npa_rate, with_farmerpay=False):
    """Get bank-specific parameters based on bank type and NPA rate"""
    
    if bank_type == "Scheduled Commercial Banks (SCBs)":
        if with_farmerpay:
            # FarmerPay reduces NPA by 2% and improves efficiency
            effective_npa = max(0, npa_rate - 2.0)
            base_collection_efficiency = 90  # Improved from 80%
            collection_efficiency = max(75, base_collection_efficiency - (effective_npa - 12.16) * 1.5)
            
            base_recovery_rate = 95  # Improved from 85%
            recovery_rate = max(85, base_recovery_rate - (effective_npa - 12.16) * 1.2)
            
            operational_costs = 1105  # 15% reduction due to automation
            other_revenue = 300  # Improved cross-selling
            
        else:
            # Base collection efficiency decreases as NPA increases
            base_collection_efficiency = 80
            collection_efficiency = max(60, base_collection_efficiency - (npa_rate - 14.16) * 2)
            
            # Base recovery rate decreases as NPA increases
            base_recovery_rate = 85
            recovery_rate = max(70, base_recovery_rate - (npa_rate - 14.16) * 1.5)
            
            operational_costs = 1300
            other_revenue = 248
        
    elif bank_type == "Regional Rural Banks (RRBs)":
        if with_farmerpay:
            # FarmerPay reduces NPA by 1.5%
            effective_npa = max(0, npa_rate - 1.5)
            base_collection_efficiency = 93  # Improved from 85%
            collection_efficiency = max(80, base_collection_efficiency - (effective_npa - 5.6) * 1.5)
            
            base_recovery_rate = 98  # Improved from 90%
            recovery_rate = max(88, base_recovery_rate - (effective_npa - 5.6) * 1.2)
            
            operational_costs = 900  # 10% reduction
            other_revenue = 250  # Improved services
            
        else:
            # Base collection efficiency
            base_collection_efficiency = 85
            collection_efficiency = max(70, base_collection_efficiency - (npa_rate - 7.1) * 2)
            
            # Base recovery rate
            base_recovery_rate = 90
            recovery_rate = max(75, base_recovery_rate - (npa_rate - 7.1) * 1.5)
            
            operational_costs = 1000
            other_revenue = 198
        
    else:  # Cooperative Banks
        if with_farmerpay:
            # FarmerPay reduces NPA by 1%
            effective_npa = max(0, npa_rate - 1.0)
            base_collection_efficiency = 92  # Improved from 87%
            collection_efficiency = max(77, base_collection_efficiency - (effective_npa - 5.5) * 1.5)
            
            base_recovery_rate = 100  # Perfect recovery with digital systems
            recovery_rate = min(100, max(88, base_recovery_rate - (effective_npa - 5.5) * 1.2))
            
            operational_costs = 688  # 20% reduction through technology
            other_revenue = 200  # Digital services expansion
            
        else:
            # Base collection efficiency
            base_collection_efficiency = 87
            collection_efficiency = max(72, base_collection_efficiency - (npa_rate - 6.5) * 2)
            
            # Base recovery rate
            base_recovery_rate = 88
            recovery_rate = max(73, base_recovery_rate - (npa_rate - 6.5) * 1.5)
            
            operational_costs = 860
            other_revenue = 148
    
    return {
        'collection_efficiency': collection_efficiency / 100,
        'recovery_rate': recovery_rate / 100,
        'operational_costs': operational_costs,
        'other_revenue': other_revenue,
        'effective_npa': effective_npa if with_farmerpay else npa_rate
    }

# Calculate financial metrics
def calculate_metrics(loan_amount, interest_rate, npa_rate, bank_params, farmerpay_fee=0):
    """Calculate all financial metrics based on inputs"""
    
    # Use effective NPA for provisioning calculations
    effective_npa = bank_params.get('effective_npa', npa_rate)
    
    # Interest Income
    interest_income = (interest_rate / 100) * loan_amount * bank_params['collection_efficiency']
    
    # Government Subvention (1.5% standard rate)
    govt_subvention = 0.015 * loan_amount * bank_params['recovery_rate']
    
    # Other Revenue
    other_revenue = bank_params['other_revenue']
    
    # Total Revenue
    total_revenue = interest_income + govt_subvention + other_revenue
    
    # Operational Costs
    operational_costs = bank_params['operational_costs']
    
    # NPA Provisioning (Effective NPA% × 25% × Loan Amount)
    npa_provisioning = (effective_npa / 100) * 0.25 * loan_amount
    
    # FarmerPay Fee (if applicable)
    farmerpay_cost = farmerpay_fee
    
    # Total Costs
    total_costs = operational_costs + npa_provisioning + farmerpay_cost
    
    # Net Profit
    net_profit = total_revenue - total_costs
    
    return {
        'interest_income': interest_income,
        'govt_subvention': govt_subvention,
        'other_revenue': other_revenue,
        'total_revenue': total_revenue,
        'operational_costs': operational_costs,
        'npa_provisioning': npa_provisioning,
        'farmerpay_fee': farmerpay_cost,
        'total_costs': total_costs,
        'net_profit': net_profit,
        'collection_efficiency': bank_params['collection_efficiency'] * 100,
        'recovery_rate': bank_params['recovery_rate'] * 100,
        'effective_npa': effective_npa
    }

# Get bank parameters and calculate metrics
bank_params = get_bank_parameters(bank_type, npa_rate)
metrics = calculate_metrics(loan_amount, interest_rate, npa_rate, bank_params)

# FarmerPay analysis if enabled
if include_farmerpay:
    bank_params_fp = get_bank_parameters(bank_type, npa_rate, with_farmerpay=True)
    metrics_fp = calculate_metrics(loan_amount, interest_rate, npa_rate, bank_params_fp, farmerpay_fee)
else:
    # Set default values when FarmerPay is not enabled
    farmerpay_fee = 0
    metrics_fp = None
    bank_params_fp = None

# Main content area - Two prominent sections
st.markdown("---")

# Section 1: Bank Analysis
st.header("🏦 BANK PROFITABILITY ANALYSIS")

if include_farmerpay:
    st.subheader("📊 Current vs FarmerPay Comparison")
    
    # Create comparison table
    comparison_data = {
        'Revenue/Cost Item': [
            'Interest Income',
            'Government Subvention', 
            'Other Revenue',
            'Total Revenue',
            'Operational Costs',
            'NPA Provisioning',
            'FarmerPay Fee',
            'Total Costs',
            'Net Profit per KCC'
        ],
        'Current State (₹)': [
            f"₹{metrics['interest_income']:,.0f}",
            f"₹{metrics['govt_subvention']:,.0f}",
            f"₹{metrics['other_revenue']:,.0f}",
            f"₹{metrics['total_revenue']:,.0f}",
            f"₹{metrics['operational_costs']:,.0f}",
            f"₹{metrics['npa_provisioning']:,.0f}",
            "₹0",
            f"₹{metrics['total_costs']:,.0f}",
            f"₹{metrics['net_profit']:,.0f}"
        ],
        'With FarmerPay (₹)': [
            f"₹{metrics_fp['interest_income']:,.0f}",
            f"₹{metrics_fp['govt_subvention']:,.0f}",
            f"₹{metrics_fp['other_revenue']:,.0f}",
            f"₹{metrics_fp['total_revenue']:,.0f}",
            f"₹{metrics_fp['operational_costs']:,.0f}",
            f"₹{metrics_fp['npa_provisioning']:,.0f}",
            f"₹{farmerpay_fee:,.0f}",
            f"₹{metrics_fp['total_costs']:,.0f}",
            f"₹{metrics_fp['net_profit']:,.0f}"
        ],
        'Change (₹)': [
            f"₹{metrics_fp['interest_income'] - metrics['interest_income']:+,.0f}",
            f"₹{metrics_fp['govt_subvention'] - metrics['govt_subvention']:+,.0f}",
            f"₹{metrics_fp['other_revenue'] - metrics['other_revenue']:+,.0f}",
            f"₹{metrics_fp['total_revenue'] - metrics['total_revenue']:+,.0f}",
            f"₹{metrics_fp['operational_costs'] - metrics['operational_costs']:+,.0f}",
            f"₹{metrics_fp['npa_provisioning'] - metrics['npa_provisioning']:+,.0f}",
            f"₹{farmerpay_fee:+,.0f}",
            f"₹{metrics_fp['total_costs'] - metrics['total_costs']:+,.0f}",
            f"₹{metrics_fp['net_profit'] - metrics['net_profit']:+,.0f}"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Bank Key Metrics with Profit Margins
    st.subheader("📊 Bank Key Metrics")
    
    # Calculate profit margins
    current_profit_margin = (metrics['net_profit'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] > 0 else 0
    fp_profit_margin = (metrics_fp['net_profit'] / metrics_fp['total_revenue'] * 100) if metrics_fp['total_revenue'] > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Net Profit",
            f"₹{metrics['net_profit']:,.0f}",
            help="Bank's current profit per KCC account"
        )
        st.metric(
            "Current Profit Margin",
            f"{current_profit_margin:.1f}%",
            help="Current profit as percentage of revenue"
        )
    
    with col2:
        st.metric(
            "With FarmerPay Profit",
            f"₹{metrics_fp['net_profit']:,.0f}",
            delta=f"₹{metrics_fp['net_profit'] - metrics['net_profit']:+,.0f}",
            help="Bank's profit with FarmerPay integration"
        )
        st.metric(
            "FarmerPay Profit Margin",
            f"{fp_profit_margin:.1f}%",
            delta=f"{fp_profit_margin - current_profit_margin:+.1f}%",
            help="Profit margin with FarmerPay integration"
        )
    
    with col3:
        bank_roi = ((metrics_fp['net_profit'] - metrics['net_profit']) / farmerpay_fee * 100) if farmerpay_fee > 0 else 0
        st.metric(
            "Bank ROI on FarmerPay",
            f"{bank_roi:.0f}%",
            help="Bank's return on FarmerPay investment"
        )
        
        break_even_months = farmerpay_fee / ((metrics_fp['net_profit'] - metrics['net_profit']) / 12) if (metrics_fp['net_profit'] - metrics['net_profit']) > 0 else float('inf')
        st.metric(
            "Break-Even Period",
            f"{break_even_months:.1f} months" if break_even_months < 24 else "24+ months",
            help="Time to recover FarmerPay investment"
        )
    
    with col4:
        revenue_improvement = ((metrics_fp['total_revenue'] / metrics['total_revenue'] - 1) * 100) if metrics['total_revenue'] > 0 else 0
        st.metric(
            "Revenue Improvement",
            f"{revenue_improvement:.1f}%",
            help="Percentage increase in total revenue"
        )
        
        npa_reduction = npa_rate - metrics_fp['effective_npa']
        st.metric(
            "NPA Reduction",
            f"{npa_reduction:.1f}%",
            help="Reduction in effective NPA rate"
        )
    
    # Bank's Profit Analysis with FarmerPay App
    st.subheader("🏦 Bank's Profit Analysis with FarmerPay App")
    st.caption(f"Analysis for {num_farmers:,} farmers with ₹{farmerpay_fee:,} FarmerPay fee per farmer")
    
    col1, col2, col3 = st.columns(3)
    
    # Calculate value components
    revenue_increase = metrics_fp['total_revenue'] - metrics['total_revenue']
    cost_reduction = metrics['operational_costs'] - metrics_fp['operational_costs']
    provisioning_savings = metrics['npa_provisioning'] - metrics_fp['npa_provisioning']
    net_value = metrics_fp['net_profit'] - metrics['net_profit']
    
    with col1:
        st.metric(
            "Revenue Increase", 
            f"₹{revenue_increase:,.0f}",
            help="Additional revenue from improved collection and recovery rates"
        )
        st.metric(
            "Cost Reduction", 
            f"₹{cost_reduction:,.0f}",
            help="Savings from operational efficiency and automation"
        )
    
    with col2:
        st.metric(
            "Provisioning Savings", 
            f"₹{provisioning_savings:,.0f}",
            help="Reduced NPA provisioning due to lower effective NPA rate"
        )
        st.metric(
            "FarmerPay Fee", 
            f"₹{farmerpay_fee:,.0f}",
            help="Annual service fee charged by FarmerPay"
        )
    
    with col3:
        st.metric(
            "Net Value Addition", 
            f"₹{net_value:,.0f}",
            delta=f"{((net_value / abs(metrics['net_profit'])) * 100 if metrics['net_profit'] != 0 else 0):.1f}% improvement"
        )
        
        # ROI calculation
        roi = ((net_value / farmerpay_fee) * 100) if farmerpay_fee > 0 else 0
        st.metric(
            "Bank's FarmerPay ROI", 
            f"{roi:.0f}%",
            help="Bank's Return on Investment for FarmerPay service"
        )
    
    # Break-even analysis
    st.subheader("⏱️ Break-Even Analysis")
    monthly_net_value = net_value / 12
    break_even_months = farmerpay_fee / monthly_net_value if monthly_net_value > 0 else float('inf')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Net Value", f"₹{monthly_net_value:,.0f}")
    with col2:
        st.metric("Annual Fee", f"₹{farmerpay_fee:,.0f}")
    with col3:
        if break_even_months < 12:
            st.metric("Break-Even Period", f"{break_even_months:.1f} months")
        else:
            st.metric("Break-Even Period", "Not achievable within 1 year", delta_color="inverse")
    
else:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📈 Financial Analysis Results")
        
        # Create detailed results table
        results_data = {
            'Revenue/Cost Item': [
                'Interest Income',
                'Government Subvention',
                'Other Revenue',
                'Total Revenue',
                'Operational Costs',
                'NPA Provisioning',
                'Total Costs',
                'Net Profit per KCC'
            ],
            'Calculation Method': [
                f"{interest_rate}% × ₹{loan_amount:,} × {metrics['collection_efficiency']:.1f}% collection efficiency",
                f"1.5% × ₹{loan_amount:,} × {metrics['recovery_rate']:.1f}% recovery rate",
                "Insurance + Cross-selling",
                "Sum of all revenue items",
                "Staff + Infrastructure + Collection",
                f"{npa_rate}% × 25% × ₹{loan_amount:,}",
                "Operational + NPA Provisioning",
                "Total Revenue - Total Costs"
            ],
            'Annual Amount (₹)': [
                f"₹{metrics['interest_income']:,.0f}",
                f"₹{metrics['govt_subvention']:,.0f}",
                f"₹{metrics['other_revenue']:,.0f}",
                f"₹{metrics['total_revenue']:,.0f}",
                f"₹{metrics['operational_costs']:,.0f}",
                f"₹{metrics['npa_provisioning']:,.0f}",
                f"₹{metrics['total_costs']:,.0f}",
                f"₹{metrics['net_profit']:,.0f}"
            ]
        }
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("📊 Bank Key Metrics")
        
        # Display key metrics in metric cards
        st.metric("Net Profit per KCC", f"₹{metrics['net_profit']:,.0f}")
        st.metric("Total Revenue", f"₹{metrics['total_revenue']:,.0f}")
        st.metric("Total Costs", f"₹{metrics['total_costs']:,.0f}")
        st.metric("NPA Provisioning", f"₹{metrics['npa_provisioning']:,.0f}")
        
        # Profit margin calculation
        profit_margin = (metrics['net_profit'] / metrics['total_revenue']) * 100 if metrics['total_revenue'] > 0 else 0
        st.metric("Bank Profit Margin", f"{profit_margin:.1f}%")

# Section 2: FarmerPay Business Analysis (only shown when enabled)
if include_farmerpay:
    st.markdown("---")
    st.header("🚀 FARMERPAY BUSINESS ANALYSIS")

    # FarmerPay Cost Structure (as per specifications)
    service_cost_per_farmer = 400  # ₹400 per farmer
    technology_opex_per_farmer = 100  # ₹100 per farmer
    total_direct_cost_per_farmer = service_cost_per_farmer + technology_opex_per_farmer  # ₹500 per farmer
    
    # Calculate FarmerPay's financials
    farmerpay_annual_revenue = num_farmers * total_revenue_per_farmer
    farmerpay_direct_costs = num_farmers * total_direct_cost_per_farmer
    farmerpay_gross_profit = farmerpay_annual_revenue - farmerpay_direct_costs
    
    # Intermediary payment: 30% of gross profit (only if gross profit is positive)
    if farmerpay_gross_profit > 0:
        intermediary_payment = farmerpay_gross_profit * 0.30
    else:
        intermediary_payment = 0
    
    # FarmerPay's net profit
    farmerpay_net_profit = farmerpay_gross_profit - intermediary_payment
    
    # FarmerPay profit margin
    farmerpay_profit_margin = (farmerpay_net_profit / farmerpay_annual_revenue * 100) if farmerpay_annual_revenue > 0 else 0
    
    # FarmerPay's ROI (assuming initial investment for platform development)
    # Estimate platform development cost based on scale
    if num_farmers <= 10000:
        platform_investment = 50000000  # ₹5 Cr for smaller scale
    elif num_farmers <= 100000:
        platform_investment = 100000000  # ₹10 Cr for medium scale
    else:
        platform_investment = 200000000  # ₹20 Cr for large scale
    
    farmerpay_roi = ((farmerpay_net_profit / platform_investment) * 100) if platform_investment > 0 else 0
    
    # Display Tiered Pricing Strategy
    st.subheader("💰 Tiered Pricing Strategy")
    
    pricing_breakdown_data = {
        'Tier': ['Basic', 'Premium', 'Enterprise'],
        'User %': [f"{basic_tier_percentage}%", f"{premium_tier_percentage}%", f"{enterprise_tier_percentage}%"],
        'Price per User (₹)': [f"₹{basic_tier_price:,}", f"₹{premium_tier_price:,}", f"₹{enterprise_tier_price:,}"],
        'Users': [
            f"{(basic_tier_percentage/100) * num_farmers:,.0f}",
            f"{(premium_tier_percentage/100) * num_farmers:,.0f}",
            f"{(enterprise_tier_percentage/100) * num_farmers:,.0f}"
        ],
        'Revenue (₹ Cr)': [
            f"₹{(basic_tier_percentage/100) * num_farmers * basic_tier_price / 10000000:.1f}",
            f"₹{(premium_tier_percentage/100) * num_farmers * premium_tier_price / 10000000:.1f}",
            f"₹{(enterprise_tier_percentage/100) * num_farmers * enterprise_tier_price / 10000000:.1f}"
        ],
        'Services': [
            'Core KCC services',
            'Enhanced analytics + insurance',
            'Full financial ecosystem'
        ]
    }
    
    pricing_breakdown_df = pd.DataFrame(pricing_breakdown_data)
    st.dataframe(pricing_breakdown_df, use_container_width=True, hide_index=True)
    
    # Display Additional Revenue Streams
    st.subheader("💼 Additional Revenue Streams")
    
    additional_revenue_data = {
        'Revenue Stream': [
            'Insurance Commissions',
            'Input Marketplace Commissions',
            'Data Analytics Services',
            'Credit Scoring Services',
            'Weather Advisory',
            'Training Programs'
        ],
        'Per Farmer (₹)': [
            f"₹{insurance_commission:,}",
            f"₹{marketplace_commission:,}",
            f"₹{data_analytics_revenue:,}",
            f"₹{credit_scoring_revenue:,}",
            f"₹{weather_advisory_revenue:,}",
            f"₹{training_programs_revenue:,}"
        ],
        'Total Revenue (₹ Cr)': [
            f"₹{num_farmers * insurance_commission / 10000000:.1f}",
            f"₹{num_farmers * marketplace_commission / 10000000:.1f}",
            f"₹{num_farmers * data_analytics_revenue / 10000000:.1f}",
            f"₹{num_farmers * credit_scoring_revenue / 10000000:.1f}",
            f"₹{num_farmers * weather_advisory_revenue / 10000000:.1f}",
            f"₹{num_farmers * training_programs_revenue / 10000000:.1f}"
        ]
    }
    
    additional_revenue_df = pd.DataFrame(additional_revenue_data)
    st.dataframe(additional_revenue_df, use_container_width=True, hide_index=True)
    
    # Display FarmerPay cost breakdown
    st.subheader("💰 FarmerPay Cost Structure")
    
    total_costs = farmerpay_direct_costs + intermediary_payment
    
    cost_breakdown_data = {
        'Cost Component': [
            'Service Cost per Farmer',
            'Technology OPEX per Farmer', 
            'Total Direct Cost per Farmer',
            'Total Direct Costs (All Farmers)',
            'Intermediary Payment (30% of Gross Profit)',
            'Total Costs'
        ],
        'Per Farmer (₹)': [
            f"₹{service_cost_per_farmer:,}",
            f"₹{technology_opex_per_farmer:,}",
            f"₹{total_direct_cost_per_farmer:,}",
            f"₹{total_direct_cost_per_farmer:,}",
            f"₹{intermediary_payment / num_farmers:,.0f}",
            f"₹{total_costs / num_farmers:,.0f}"
        ],
        'Total Amount (₹)': [
            f"₹{num_farmers * service_cost_per_farmer / 10000000:.1f} Cr",
            f"₹{num_farmers * technology_opex_per_farmer / 10000000:.1f} Cr",
            f"₹{farmerpay_direct_costs / 10000000:.1f} Cr",
            f"₹{farmerpay_direct_costs / 10000000:.1f} Cr",
            f"₹{intermediary_payment / 10000000:.1f} Cr",
            f"₹{total_costs / 10000000:.1f} Cr"
        ]
    }
    
    cost_breakdown_df = pd.DataFrame(cost_breakdown_data)
    st.dataframe(cost_breakdown_df, use_container_width=True, hide_index=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Annual Revenue",
            f"₹{farmerpay_annual_revenue / 10000000:.1f} Cr",
            help=f"₹{farmerpay_annual_revenue:,} ({num_farmers:,} farmers × ₹{total_revenue_per_farmer:,})"
        )
        st.caption(f"Core: ₹{farmerpay_fee:.0f} + Additional: ₹{additional_revenue_per_farmer:.0f}")
    
    with col2:
        st.metric(
            "Gross Profit",
            f"₹{farmerpay_gross_profit / 10000000:.1f} Cr",
            help=f"₹{farmerpay_gross_profit:,} (Revenue - Direct Costs)"
        )
    
    with col3:
        st.metric(
            "Net Profit",
            f"₹{farmerpay_net_profit / 10000000:.1f} Cr",
            help=f"₹{farmerpay_net_profit:,} (After intermediary payment)"
        )
    
    with col4:
        st.metric(
            "Profit Margin",
            f"{farmerpay_profit_margin:.1f}%",
            help="Net Profit as percentage of Revenue"
        )
    
    # ROI Analysis
    st.subheader("📈 FarmerPay ROI Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Platform Investment",
            f"₹{platform_investment / 10000000:.0f} Cr",
            help="Initial investment for platform development"
        )
    
    with col2:
        st.metric(
            "Annual ROI",
            f"{farmerpay_roi:.1f}%",
            help="Return on Investment based on annual net profit"
        )
    
    # Market penetration analysis
    st.subheader("📊 Market Impact Analysis")
    
    # Total value created in the ecosystem
    total_bank_value_addition = net_value * num_farmers
    ecosystem_value = farmerpay_net_profit + total_bank_value_addition
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Bank Value Addition",
            f"₹{total_bank_value_addition / 10000000:.1f} Cr",
            help=f"₹{total_bank_value_addition:,} (Value added to all participating banks)"
        )
    
    with col2:
        st.metric(
            "Total Ecosystem Value",
            f"₹{ecosystem_value / 10000000:.1f} Cr",
            help=f"₹{ecosystem_value:,} (Combined value for FarmerPay + Banks)"
        )
    
    with col3:
        # Calculate value per farmer
        value_per_farmer = ecosystem_value / num_farmers if num_farmers > 0 else 0
        st.metric(
            "Value per Farmer",
            f"₹{value_per_farmer:,.0f}",
            help="Total ecosystem value divided by number of farmers"
        )

# Optimal Pricing Analysis for FarmerPay
if include_farmerpay:
    st.header("🎯 Optimal FarmerPay Pricing Analysis")
    
    # Calculate optimal pricing range
    if bank_type == "Scheduled Commercial Banks (SCBs)":
        price_range = np.arange(600, 1001, 50)
    elif bank_type == "Regional Rural Banks (RRBs)":
        price_range = np.arange(450, 751, 50)
    else:  # Cooperative Banks
        price_range = np.arange(350, 651, 50)
    
    pricing_data = []
    for test_fee in price_range:
        test_metrics_fp = calculate_metrics(loan_amount, interest_rate, npa_rate, bank_params_fp, int(test_fee))
        test_net_value = test_metrics_fp['net_profit'] - metrics['net_profit']
        test_roi = ((test_net_value / test_fee) * 100) if test_fee > 0 else 0
        
        pricing_data.append({
            'Fee': test_fee,
            'Bank_Net_Profit': test_metrics_fp['net_profit'],
            'Net_Value_Addition': test_net_value,
            'ROI': test_roi,
            'Monthly_Value': test_net_value / 12,
            'Break_Even_Months': test_fee / (test_net_value / 12) if test_net_value > 0 else float('inf')
        })
    
    pricing_df = pd.DataFrame(pricing_data)
    
    # Find optimal fee (highest net value that maintains positive ROI)
    viable_fees = pricing_df[pricing_df['Net_Value_Addition'] > 0]
    if not viable_fees.empty:
        max_idx = viable_fees['Net_Value_Addition'].idxmax()
        optimal_fee = viable_fees.loc[max_idx, 'Fee']
        optimal_roi = viable_fees.loc[max_idx, 'ROI']
        
        st.success(f"**Recommended FarmerPay Fee: ₹{optimal_fee:,.0f}** (ROI: {optimal_roi:.0f}%)")
    
    # Pricing sensitivity chart
    fig_pricing = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Bank Net Profit vs FarmerPay Fee', 'ROI vs FarmerPay Fee'),
        vertical_spacing=0.15
    )
    
    # Bank profit line
    fig_pricing.add_trace(
        go.Scatter(
            x=pricing_df['Fee'],
            y=pricing_df['Bank_Net_Profit'],
            mode='lines+markers',
            name='Bank Net Profit',
            line=dict(color='green')
        ),
        row=1, col=1
    )
    
    # Current fee point
    fig_pricing.add_trace(
        go.Scatter(
            x=[farmerpay_fee],
            y=[metrics_fp['net_profit']],
            mode='markers',
            name='Current Fee',
            marker=dict(color='red', size=10)
        ),
        row=1, col=1
    )
    
    # ROI line
    fig_pricing.add_trace(
        go.Scatter(
            x=pricing_df['Fee'],
            y=pricing_df['ROI'],
            mode='lines+markers',
            name='ROI %',
            line=dict(color='blue')
        ),
        row=2, col=1
    )
    
    # Current ROI point
    fig_pricing.add_trace(
        go.Scatter(
            x=[farmerpay_fee],
            y=[roi],
            mode='markers',
            name='Current ROI',
            marker=dict(color='darkblue', size=10)
        ),
        row=2, col=1
    )
    
    fig_pricing.update_layout(
        title="FarmerPay Pricing Impact Analysis",
        height=600,
        showlegend=True
    )
    
    fig_pricing.update_xaxes(title_text="FarmerPay Fee (₹)", row=2, col=1)
    fig_pricing.update_yaxes(title_text="Bank Net Profit (₹)", row=1, col=1)
    fig_pricing.update_yaxes(title_text="ROI (%)", row=2, col=1)
    
    st.plotly_chart(fig_pricing, use_container_width=True)

# Charts section
st.header("📊 Visual Analysis")

if include_farmerpay:
    col1, col2 = st.columns(2)
    
    with col1:
        # Comparison bar chart
        comparison_chart_data = pd.DataFrame({
            'Metric': ['Revenue', 'Costs', 'Net Profit'],
            'Current': [metrics['total_revenue'], metrics['total_costs'], metrics['net_profit']],
            'With FarmerPay': [metrics_fp['total_revenue'], metrics_fp['total_costs'], metrics_fp['net_profit']]
        })
        
        fig_comparison = px.bar(
            comparison_chart_data,
            x='Metric',
            y=['Current', 'With FarmerPay'],
            title="Current vs FarmerPay Financial Comparison",
            barmode='group'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col2:
        # FarmerPay value breakdown
        value_data = {
            'Revenue Increase': revenue_increase,
            'Cost Reduction': cost_reduction,
            'Provisioning Savings': provisioning_savings,
            'FarmerPay Fee': -farmerpay_fee
        }
        
        fig_value = px.bar(
            x=list(value_data.keys()),
            y=list(value_data.values()),
            title="FarmerPay Value Component Breakdown",
            color=list(value_data.values()),
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig_value.update_layout(showlegend=False)
        st.plotly_chart(fig_value, use_container_width=True)
    
    # FarmerPay scaling analysis chart
    st.subheader("📈 FarmerPay Business Scaling Analysis")
    
    # Create scaling data for different farmer counts
    farmer_scale_range = np.array([1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000])
    scaling_data = []
    
    for scale in farmer_scale_range:
        scale_revenue = scale * total_revenue_per_farmer
        scale_direct_costs = scale * total_direct_cost_per_farmer  # ₹500 per farmer (₹400 service + ₹100 tech)
        scale_gross_profit = scale_revenue - scale_direct_costs
        scale_intermediary_payment = scale_gross_profit * 0.30 if scale_gross_profit > 0 else 0
        scale_profit = scale_gross_profit - scale_intermediary_payment
        
        # Platform investment based on scale
        if scale <= 10000:
            investment = 50000000
        elif scale <= 100000:
            investment = 100000000
        else:
            investment = 200000000
        
        scale_roi = (scale_profit / investment) * 100
        
        scaling_data.append({
            'Farmers': scale,
            'Revenue_Cr': scale_revenue / 10000000,
            'Profit_Cr': scale_profit / 10000000,
            'ROI': scale_roi
        })
    
    scaling_df = pd.DataFrame(scaling_data)
    
    # Create scaling chart
    fig_scaling = make_subplots(
        rows=2, cols=1,
        subplot_titles=('FarmerPay Profit vs Number of Farmers', 'FarmerPay ROI vs Number of Farmers'),
        vertical_spacing=0.15
    )
    
    # Profit line
    fig_scaling.add_trace(
        go.Scatter(
            x=scaling_df['Farmers'],
            y=scaling_df['Profit_Cr'],
            mode='lines+markers',
            name='FarmerPay Profit',
            line=dict(color='green', width=3)
        ),
        row=1, col=1
    )
    
    # Current scale point
    current_profit_cr = farmerpay_net_profit / 10000000
    fig_scaling.add_trace(
        go.Scatter(
            x=[num_farmers],
            y=[current_profit_cr],
            mode='markers',
            name='Current Scale',
            marker=dict(color='red', size=12, symbol='star')
        ),
        row=1, col=1
    )
    
    # ROI line
    fig_scaling.add_trace(
        go.Scatter(
            x=scaling_df['Farmers'],
            y=scaling_df['ROI'],
            mode='lines+markers',
            name='FarmerPay ROI',
            line=dict(color='blue', width=3)
        ),
        row=2, col=1
    )
    
    # Current ROI point
    fig_scaling.add_trace(
        go.Scatter(
            x=[num_farmers],
            y=[farmerpay_roi],
            mode='markers',
            name='Current ROI',
            marker=dict(color='darkblue', size=12, symbol='star')
        ),
        row=2, col=1
    )
    
    fig_scaling.update_layout(
        title="FarmerPay Business Scaling Projections",
        height=600,
        showlegend=True
    )
    
    fig_scaling.update_xaxes(title_text="Number of Farmers", type="log", row=2, col=1)
    fig_scaling.update_xaxes(type="log", row=1, col=1)
    fig_scaling.update_yaxes(title_text="Profit (₹ Crores)", row=1, col=1)
    fig_scaling.update_yaxes(title_text="ROI (%)", row=2, col=1)
    
    st.plotly_chart(fig_scaling, use_container_width=True)

else:
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue breakdown pie chart
        revenue_data = {
            'Interest Income': metrics['interest_income'],
            'Government Subvention': metrics['govt_subvention'],
            'Other Revenue': metrics['other_revenue']
        }
        
        fig_revenue = px.pie(
            values=list(revenue_data.values()),
            names=list(revenue_data.keys()),
            title="Revenue Breakdown"
        )
        fig_revenue.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Cost breakdown pie chart
        cost_data = {
            'Operational Costs': metrics['operational_costs'],
            'NPA Provisioning': metrics['npa_provisioning']
        }
        
        fig_costs = px.pie(
            values=list(cost_data.values()),
            names=list(cost_data.keys()),
            title="Cost Breakdown"
        )
        fig_costs.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_costs, use_container_width=True)

# NPA Impact Analysis
st.header("🎯 NPA Impact Analysis")

# Create NPA sensitivity analysis
npa_range = np.arange(0.5, min(25.0, npa_rate * 2), 0.5)
sensitivity_data = []

for test_npa in npa_range:
    test_params = get_bank_parameters(bank_type, test_npa)
    test_metrics = calculate_metrics(loan_amount, interest_rate, test_npa, test_params)
    sensitivity_data.append({
        'NPA_Rate': test_npa,
        'Net_Profit': test_metrics['net_profit'],
        'NPA_Provisioning': test_metrics['npa_provisioning'],
        'Total_Revenue': test_metrics['total_revenue']
    })

sensitivity_df = pd.DataFrame(sensitivity_data)

# Plot NPA sensitivity
fig_sensitivity = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Net Profit vs NPA Rate', 'NPA Provisioning vs NPA Rate'),
    vertical_spacing=0.1
)

# Net profit line
fig_sensitivity.add_trace(
    go.Scatter(
        x=sensitivity_df['NPA_Rate'],
        y=sensitivity_df['Net_Profit'],
        mode='lines+markers',
        name='Net Profit',
        line=dict(color='green')
    ),
    row=1, col=1
)

# Current NPA point
fig_sensitivity.add_trace(
    go.Scatter(
        x=[npa_rate],
        y=[metrics['net_profit']],
        mode='markers',
        name='Current NPA',
        marker=dict(color='red', size=10)
    ),
    row=1, col=1
)

# NPA provisioning line
fig_sensitivity.add_trace(
    go.Scatter(
        x=sensitivity_df['NPA_Rate'],
        y=sensitivity_df['NPA_Provisioning'],
        mode='lines+markers',
        name='NPA Provisioning',
        line=dict(color='red')
    ),
    row=2, col=1
)

# Current NPA provisioning point
fig_sensitivity.add_trace(
    go.Scatter(
        x=[npa_rate],
        y=[metrics['npa_provisioning']],
        mode='markers',
        name='Current Provisioning',
        marker=dict(color='darkred', size=10)
    ),
    row=2, col=1
)

fig_sensitivity.update_layout(
    title="NPA Rate Impact on Profitability",
    height=600,
    showlegend=True
)

fig_sensitivity.update_xaxes(title_text="NPA Rate (%)", row=2, col=1)
fig_sensitivity.update_yaxes(title_text="Net Profit (₹)", row=1, col=1)
fig_sensitivity.update_yaxes(title_text="NPA Provisioning (₹)", row=2, col=1)

st.plotly_chart(fig_sensitivity, use_container_width=True)

# Portfolio Analysis
st.header("💼 Portfolio Impact Analysis")

portfolio_size = st.selectbox("Portfolio Size (Number of KCCs)", [100, 500, 1000, 2000, 5000], index=2)

if include_farmerpay:
    current_portfolio_profit = metrics['net_profit'] * portfolio_size
    fp_portfolio_profit = metrics_fp['net_profit'] * portfolio_size
    portfolio_improvement = fp_portfolio_profit - current_portfolio_profit
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Portfolio Profit", 
            f"₹{current_portfolio_profit / 100000:.1f}L",
            help=f"₹{current_portfolio_profit:,.0f}"
        )
    
    with col2:
        st.metric(
            "With FarmerPay", 
            f"₹{fp_portfolio_profit / 100000:.1f}L",
            help=f"₹{fp_portfolio_profit:,.0f}"
        )
    
    with col3:
        st.metric(
            "Portfolio Improvement", 
            f"₹{portfolio_improvement / 100000:.1f}L",
            delta=f"{((portfolio_improvement / current_portfolio_profit) * 100 if current_portfolio_profit != 0 else 0):.1f}%",
            help=f"₹{portfolio_improvement:,.0f}"
        )
    
    with col4:
        annual_fp_investment = farmerpay_fee * portfolio_size
        portfolio_roi = ((portfolio_improvement / annual_fp_investment) * 100) if annual_fp_investment > 0 else 0
        st.metric(
            "Portfolio ROI", 
            f"{portfolio_roi:.0f}%",
            help=f"Annual FarmerPay investment: ₹{annual_fp_investment:,.0f}"
        )
    
    # 5-Year Impact Analysis
    st.subheader("📈 5-Year Cumulative Impact")
    
    five_year_investment = annual_fp_investment * 5
    five_year_benefits = portfolio_improvement * 5
    five_year_net_value = five_year_benefits - five_year_investment
    five_year_roi = ((five_year_net_value / five_year_investment) * 100) if five_year_investment > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("5-Year Investment", f"₹{five_year_investment / 100000:.1f}L")
    
    with col2:
        st.metric("5-Year Benefits", f"₹{five_year_benefits / 100000:.1f}L")
    
    with col3:
        st.metric("5-Year Net Value", f"₹{five_year_net_value / 100000:.1f}L")
    
    with col4:
        st.metric("5-Year Total ROI", f"{five_year_roi:.0f}%")

else:
    portfolio_profit = metrics['net_profit'] * portfolio_size
    portfolio_revenue = metrics['total_revenue'] * portfolio_size
    portfolio_costs = metrics['total_costs'] * portfolio_size
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Portfolio Net Profit", f"₹{portfolio_profit:,.0f}")
    
    with col2:
        st.metric("Portfolio Revenue", f"₹{portfolio_revenue:,.0f}")
    
    with col3:
        st.metric("Portfolio Costs", f"₹{portfolio_costs:,.0f}")

# Additional insights
st.header("💡 Key Insights & Recommendations")

insights = []

if include_farmerpay:
    # FarmerPay specific insights
    if net_value > 0:
        insights.append("✅ FarmerPay integration is highly beneficial for this bank")
        insights.append(f"💰 Expected annual value addition: ₹{net_value:,.0f} per KCC")
        
        if break_even_months < 6:
            insights.append(f"⚡ Extremely fast break-even: {break_even_months:.1f} months")
        elif break_even_months < 12:
            insights.append(f"✅ Acceptable break-even period: {break_even_months:.1f} months")
        else:
            insights.append(f"⚠️ Long break-even period: {break_even_months:.1f} months")
    else:
        insights.append("❌ FarmerPay fee is too high for current benefits")
        insights.append("💡 Consider negotiating a lower fee or improving operational efficiency")
    
    # NPA improvement insights
    npa_reduction = npa_rate - metrics_fp['effective_npa']
    insights.append(f"📉 FarmerPay reduces effective NPA by {npa_reduction:.1f}% points")
    insights.append(f"💵 Annual provisioning savings: ₹{provisioning_savings:,.0f}")
    
    # Pricing recommendations
    if bank_type == "Scheduled Commercial Banks (SCBs)":
        if farmerpay_fee > 850:
            insights.append("💡 Consider reducing FarmerPay fee below ₹850 for better ROI")
        elif farmerpay_fee < 700:
            insights.append("💡 Current fee provides excellent value - could potentially increase")
    elif bank_type == "Regional Rural Banks (RRBs)":
        if farmerpay_fee > 650:
            insights.append("💡 Consider reducing FarmerPay fee below ₹650 for better ROI") 
        elif farmerpay_fee < 550:
            insights.append("💡 Current fee provides excellent value - could potentially increase")
    else:  # Cooperative Banks
        if farmerpay_fee > 550:
            insights.append("💡 Consider reducing FarmerPay fee below ₹550 for better ROI")
        elif farmerpay_fee < 400:
            insights.append("💡 Current fee provides excellent value - could potentially increase")
    
    # FarmerPay business insights
    insights.append(f"🏢 FarmerPay can generate ₹{farmerpay_net_profit / 10000000:.1f} Cr annual profit at {num_farmers:,} farmers")
    insights.append(f"📈 FarmerPay ROI: {farmerpay_roi:.1f}% on platform investment")
    
    if farmerpay_roi > 50:
        insights.append("✅ Excellent ROI - FarmerPay business model is highly profitable")
    elif farmerpay_roi > 25:
        insights.append("✅ Good ROI - FarmerPay business model is profitable")
    else:
        insights.append("⚠️ Low ROI - Consider scaling up or optimizing costs")
    
    # Scale insights
    if num_farmers >= 100000:
        insights.append("🚀 Large scale deployment - significant market impact")
    elif num_farmers >= 50000:
        insights.append("📈 Medium scale deployment - good market penetration")
    else:
        insights.append("🌱 Small scale deployment - room for growth")

else:
    # Standard insights without FarmerPay
    if metrics['net_profit'] > 0:
        insights.append("✅ The current configuration is profitable")
    else:
        insights.append("❌ The current configuration results in losses")

# Common insights for both scenarios
if npa_rate > 15:
    insights.append("⚠️ High NPA rate significantly impacts profitability")
    if include_farmerpay:
        insights.append("💡 FarmerPay's NPA reduction capabilities are especially valuable here")
elif npa_rate > 10:
    insights.append("⚠️ Moderate NPA rate - monitor closely")
else:
    insights.append("✅ NPA rate is within acceptable range")

if metrics['npa_provisioning'] > metrics['interest_income']:
    insights.append("❌ NPA provisioning exceeds interest income")
    if include_farmerpay:
        insights.append("💡 FarmerPay can help reduce this provisioning burden")

# ROI calculations
current_roi = (metrics['net_profit'] / loan_amount) * 100 if loan_amount > 0 else 0

if include_farmerpay:
    fp_roi = (metrics_fp['net_profit'] / loan_amount) * 100 if loan_amount > 0 else 0
    insights.append(f"📈 Current ROI: {current_roi:.2f}% → With FarmerPay: {fp_roi:.2f}%")
    
    # Portfolio scaling insights
    if portfolio_size >= 1000:
        insights.append(f"🚀 At {portfolio_size} KCCs, annual portfolio improvement: ₹{portfolio_improvement / 100000:.1f}L")
else:
    insights.append(f"📈 Return on Investment: {current_roi:.2f}%")

for insight in insights:
    st.write(insight)

# Footer
st.markdown("---")
st.markdown("*This calculator provides estimates based on standard banking practices and may vary based on specific bank policies and market conditions.*")
