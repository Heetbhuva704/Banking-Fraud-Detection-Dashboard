import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

from data_generator import generate_initial_data, generate_live_transaction
from model_trainer import train_fraud_model, predict_fraud
from ui_components import (
    get_enterprise_css,
    icon_svg,
    card_kpi_html,
    header_bar_html,
    plotly_dark_theme,
    BG_CARD,
    BG_SURFACE,
    BORDER_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT_PRIMARY,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER
)

st.set_page_config(
    page_title="FinEdge | Banking Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Inject Enterprise Dark CSS ---
st.markdown(get_enterprise_css(), unsafe_allow_html=True)

# --- Initialization & Session State ---
if 'initialized' not in st.session_state or 'tickets' not in st.session_state or 'phone_number' not in st.session_state.get('customers', pd.DataFrame()).columns:
    with st.spinner("Connecting to Core Banking Engine..."):
        df_customers, df_products, df_transactions, df_tickets = generate_initial_data()
        model, accuracy = train_fraud_model(df_transactions)
        
        st.session_state['customers'] = df_customers
        st.session_state['products'] = df_products
        st.session_state['transactions'] = df_transactions
        st.session_state['tickets'] = df_tickets
        st.session_state['model'] = model
        st.session_state['accuracy'] = accuracy
        st.session_state['live_feed'] = []
        st.session_state['time_series_x'] = list(range(50))
        st.session_state['time_series_y'] = [0] * 50
        st.session_state['notices'] = []
        st.session_state['blocked_accounts'] = []
        st.session_state['bot_logs'] = []
        st.session_state['initialized'] = True

df_c = st.session_state['customers']
df_p = st.session_state['products']
df_t = st.session_state['transactions']
df_tickets = st.session_state['tickets']
model = st.session_state['model']

live_df = pd.DataFrame(st.session_state['live_feed'])
if not live_df.empty:
    live_df_viz = live_df.copy()
    live_df_viz['is_fraud'] = live_df_viz['predicted_fraud']
    all_txns = pd.concat([df_t, live_df_viz], ignore_index=True)
else:
    all_txns = df_t.copy()

# --- Sidebar ---
with st.sidebar:
    # Enterprise Brand Header
    logo_svg = icon_svg("building", size=22, color=ACCENT_PRIMARY)
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; padding: 4px 0 16px 0; border-bottom: 1px solid {BORDER_COLOR}; margin-bottom: 16px;">
        <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 6px; padding: 6px; display: flex; align-items: center; justify-content: center;">
            {logo_svg}
        </div>
        <div>
            <div style="font-size: 16px; font-weight: 700; color: {TEXT_PRIMARY}; letter-spacing: -0.02em;">FinEdge</div>
            <div style="font-size: 11px; color: {TEXT_MUTED}; font-weight: 500;">Banking Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Operational Controls Section
    st.markdown(f"""
    <div style="font-size: 11px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
        System Controls
    </div>
    """, unsafe_allow_html=True)
    
    is_live = st.session_state.get('simulate', False)
    btn_label = "Stop Telemetry Stream" if is_live else "Engage Live System"
    
    st.markdown(f"""
    <style>
    div[data-testid="stSidebar"] div[data-testid="stButton"] button {{
        background: {'rgba(248, 113, 113, 0.15)' if is_live else 'linear-gradient(135deg, #0284C7 0%, #0369A1 100%)'} !important;
        color: {'#F87171' if is_live else '#FFFFFF'} !important;
        border: 1px solid {'rgba(248, 113, 113, 0.4)' if is_live else '#38BDF8'} !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 8px 12px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
        background: {'rgba(248, 113, 113, 0.25)' if is_live else '#0284C7'} !important;
        border-color: {'#F87171' if is_live else '#7DD3FC'} !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(btn_label, use_container_width=True):
        st.session_state['simulate'] = not is_live
        st.rerun()
        
    simulate = st.session_state.get('simulate', False)
    
    status_color = COLOR_SUCCESS if simulate else TEXT_MUTED
    status_text = "Live Stream Active (Ingesting)" if simulate else "Telemetry Stream Paused"
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 6px; font-size: 11px; color: {status_color}; font-weight: 500; margin-top: 6px; margin-bottom: 16px;">
        <span style="width: 6px; height: 6px; border-radius: 50%; background-color: {status_color}; display: inline-block;"></span>
        {status_text}
    </div>
    """, unsafe_allow_html=True)
    
    timeframe = st.selectbox("Telemetry Timeframe", ["Live Feed (Active)", "Last 24 Hours", "Year to Date (YTD)"])
    
    st.markdown(f"""<div style="border-top: 1px solid {BORDER_COLOR}; margin: 20px 0 16px 0;"></div>""", unsafe_allow_html=True)
    
    # Model Metadata & Validation
    acc_val = st.session_state['accuracy'] * 100
    cpu_icon = icon_svg("cpu", size=16, color=ACCENT_PRIMARY)
    shield_icon = icon_svg("shield", size=16, color=COLOR_SUCCESS)
    
    st.markdown(f"""
    <div style="font-size: 11px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
        Model Governance
    </div>
    <div style="background: {BG_CARD}; border: 1px solid {BORDER_COLOR}; border-radius: 8px; padding: 12px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-size: 11px; color: {TEXT_SECONDARY};">Algorithm</span>
            <span style="font-size: 11px; font-weight: 600; color: {TEXT_PRIMARY};">Random Forest v2.4</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-size: 11px; color: {TEXT_SECONDARY};">Validation Accuracy</span>
            <span style="font-size: 11px; font-weight: 700; color: {COLOR_SUCCESS};">{acc_val:.1f}% (Test Set)</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-size: 11px; color: {TEXT_SECONDARY};">Features Evaluated</span>
            <span style="font-size: 11px; font-weight: 600; color: {TEXT_PRIMARY};">5 Vector Inputs</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 11px; color: {TEXT_SECONDARY};">Inference Latency</span>
            <span style="font-size: 11px; font-weight: 600; color: {ACCENT_PRIMARY};">&lt; 2 ms / txn</span>
        </div>
    </div>
    
    <div style="font-size: 10px; color: {TEXT_MUTED}; line-height: 1.4;">
        Note: Model metrics represent offline test-set validation on balanced historical data.
    </div>
    """, unsafe_allow_html=True)

# --- Top Header ---
current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
st.markdown(header_bar_html(simulate, current_time_str), unsafe_allow_html=True)

# --- KPI Cards Row ---
avg_balance = df_c['balance'].mean()
total_advances = df_p['loan_amount'].sum()
fraud_count = all_txns['is_fraud'].sum()
active_lockers_count = len(df_c[df_c['locker_type'] != 'None'])

new_flags = len(live_df[live_df['predicted_fraud'] == 1]) if not live_df.empty else 0
live_flags_str = f"+{new_flags} Live Anomalies" if new_flags > 0 else "Baseline Normal"
trend_type = "alert" if new_flags > 0 else "neutral"

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(card_kpi_html(
        label="Average Account Balance",
        value=f"₹{avg_balance:,.0f}",
        icon_name="wallet",
        subtitle="Across 800 retail accounts",
        trend_text="Stable Liquidity"
    ), unsafe_allow_html=True)

with k2:
    st.markdown(card_kpi_html(
        label="Active Loan Portfolio",
        value=f"₹{total_advances/10000000:.2f} Cr",
        icon_name="landmark",
        subtitle="Gross credit exposure",
        trend_text="Total Book Value"
    ), unsafe_allow_html=True)

with k3:
    st.markdown(card_kpi_html(
        label="Detected Fraud Events",
        value=f"{fraud_count:,}",
        icon_name="shield-alert",
        subtitle="Omni-channel flagged vectors",
        trend_text=live_flags_str,
        trend_type=trend_type
    ), unsafe_allow_html=True)

with k4:
    st.markdown(card_kpi_html(
        label="Active Safety Lockers",
        value=f"{active_lockers_count:,}",
        icon_name="lock",
        subtitle="Customer vault rentals",
        trend_text="Fee Generating"
    ), unsafe_allow_html=True)

# --- Main Navigation Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Live Telemetry",
    "Treasury & Liquidity",
    "Risk & Compliance (AML)",
    "AI Predictive Intelligence",
    "Customer Care & CRM"
])

# ==============================================================================
# TAB 1: Live Telemetry
# ==============================================================================
with tab1:
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; display: flex; align-items: center; gap: 8px;">
            {icon_svg("activity", size=18, color=ACCENT_PRIMARY)}
            Real-Time Network Ingestion & Telemetry
        </div>
        <div style="font-size: 12px; color: {TEXT_MUTED};">
            Ingestion channels: UPI · ATM · POS · Online Banking
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state['live_feed']) < 5 and not simulate:
        st.info("Live telemetry stream is currently paused. Activate 'Engage Live System' in the sidebar to stream real-time transactions.")
    
    col_chart, col_feed = st.columns([1.8, 1.2])
    
    with col_chart:
        # Time-series volume
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
            Operational Throughput (Transactions / Second)
        </div>
        """, unsafe_allow_html=True)
        
        fig_vol = go.Figure(go.Scatter(
            x=st.session_state['time_series_x'],
            y=st.session_state['time_series_y'],
            mode='lines',
            fill='tozeroy',
            line=dict(color=ACCENT_PRIMARY, width=2.5),
            fillcolor='rgba(56, 189, 248, 0.12)'
        ))
        fig_vol = plotly_dark_theme(fig_vol, height=220, x_tick=False)
        fig_vol.update_yaxes(title_text="Txns / Sec", title_font=dict(size=10, color=TEXT_MUTED))
        st.plotly_chart(fig_vol, use_container_width=True)
        
        sub1, sub2 = st.columns(2)
        with sub1:
            st.markdown(f"""
            <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
                Transaction Channel Distribution
            </div>
            """, unsafe_allow_html=True)
            
            if not live_df.empty:
                cat_counts = live_df.tail(60)['category'].value_counts().reset_index()
                fig_cat = px.pie(
                    cat_counts, 
                    names='category', 
                    values='count', 
                    hole=0.6,
                    color_discrete_sequence=['#38BDF8', '#818CF8', '#34D399', '#FBBF24', '#64748B']
                )
                fig_cat = plotly_dark_theme(fig_cat, height=220, show_legend=False)
                fig_cat.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color=BG_CARD, width=2)))
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                cat_counts = df_t['category'].value_counts().reset_index()
                fig_cat = px.pie(
                    cat_counts, 
                    names='category', 
                    values='count', 
                    hole=0.6,
                    color_discrete_sequence=['#38BDF8', '#818CF8', '#34D399', '#FBBF24', '#64748B']
                )
                fig_cat = plotly_dark_theme(fig_cat, height=220, show_legend=False)
                fig_cat.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color=BG_CARD, width=2)))
                st.plotly_chart(fig_cat, use_container_width=True)
                
        with sub2:
            st.markdown(f"""
            <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
                Model Anomaly Classification
            </div>
            """, unsafe_allow_html=True)
            
            if not live_df.empty:
                class_df = live_df.tail(60)['predicted_fraud'].value_counts().reset_index()
                class_df['Label'] = class_df['predicted_fraud'].map({0: 'Legitimate', 1: 'Flagged Anomaly'})
                fig_bar = px.bar(
                    class_df, 
                    x='Label', 
                    y='count', 
                    color='Label', 
                    color_discrete_map={'Legitimate': COLOR_SUCCESS, 'Flagged Anomaly': COLOR_DANGER}
                )
                fig_bar = plotly_dark_theme(fig_bar, height=220, show_legend=False)
                fig_bar.update_xaxes(title_text="")
                fig_bar.update_yaxes(title_text="Count")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.markdown(f"""
                <div style="background: {BG_CARD}; border: 1px dashed {BORDER_COLOR}; border-radius: 8px; height: 220px; display: flex; align-items: center; justify-content: center; color: {TEXT_MUTED}; font-size: 12px;">
                    Awaiting live streaming telemetry data...
                </div>
                """, unsafe_allow_html=True)

    with col_feed:
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; display: flex; justify-content: space-between;">
            <span>Live Omni-Channel Stream</span>
            <span style="color: {TEXT_MUTED}; font-size: 11px;">Latest 15 Events</span>
        </div>
        """, unsafe_allow_html=True)
        
        feed_box = st.container(height=510)
        with feed_box:
            recent_items = st.session_state['live_feed'][-15:]
            if recent_items:
                for txn in reversed(recent_items):
                    is_anomaly = txn.get('predicted_fraud', 0) == 1
                    item_class = "txn-item-fraud" if is_anomaly else "txn-item-normal"
                    badge_class = "badge-fraud" if is_anomaly else "badge-normal"
                    amt_class = "txn-amount-fraud" if is_anomaly else "txn-amount-normal"
                    status_text = "Anomaly Detected" if is_anomaly else "Authorized"
                    
                    amt_val = f"₹{txn['amount']:,.2f}" if txn['amount'] > 0 else "Non-Monetary"
                    cust_id = txn.get('customer_id', 'N/A')
                    loc = txn.get('location', 'Unknown Terminal')
                    cat = txn.get('category', 'Transaction')
                    mode = txn.get('mode', 'Channel')
                    
                    st.markdown(f"""
                    <div class="txn-item {item_class}">
                        <div class="txn-row-top">
                            <div>
                                <span class="txn-id">{cust_id}</span>
                                <span class="txn-badge badge-channel" style="margin-left: 6px;">{mode}</span>
                            </div>
                            <span class="txn-amount {amt_class}">{amt_val}</span>
                        </div>
                        <div class="txn-row-bottom">
                            <span>{loc}</span>
                            <span class="txn-badge {badge_class}">{status_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="padding: 24px 12px; text-align: center; color: {TEXT_MUTED}; font-size: 12px;">
                    {icon_svg("activity", size=24, color=TEXT_MUTED)}<br><br>
                    No streaming transactions captured yet.<br>
                    Toggle 'Engage Live System' in the sidebar to initiate real-time telemetry.
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: Treasury & Liquidity
# ==============================================================================
with tab2:
    st.markdown(f"""
    <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
        {icon_svg("landmark", size=18, color=ACCENT_PRIMARY)}
        Core Banking Operations & Liquidity Management
    </div>
    """, unsafe_allow_html=True)
    
    tc1, tc2, tc3 = st.columns([1, 1.2, 1.4])
    
    with tc1:
        min_bal_count = df_c['min_bal_violation'].sum()
        total_payout = df_p['total_interest_earned'].sum()
        
        st.markdown(f"""
        <div class="section-card" style="margin-bottom: 12px;">
            <div style="font-size: 11px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase;">Minimum Balance Violations</div>
            <div style="font-size: 24px; font-weight: 700; color: {COLOR_WARNING}; margin: 6px 0;">{min_bal_count:,} Accounts</div>
            <div style="font-size: 11px; color: {TEXT_SECONDARY};">Operating below standard ₹1,000 threshold</div>
        </div>
        
        <div class="section-card">
            <div style="font-size: 11px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase;">Customer Interest Payouts</div>
            <div style="font-size: 24px; font-weight: 700; color: {COLOR_SUCCESS}; margin: 6px 0;">₹{total_payout/100000:.2f} Lakh</div>
            <div style="font-size: 11px; color: {TEXT_SECONDARY};">Accrued FD (7%) & RD (5%) disbursements</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid {ACCENT_PRIMARY}; padding: 10px 12px; border-radius: 4px; font-size: 11px; color: {TEXT_SECONDARY}; line-height: 1.5; margin-top: 10px;">
            <strong style="color: {TEXT_PRIMARY};">Liquidity Metric:</strong> Gold loans currently generate the highest proportional interest yield per account in the institutional loan book.
        </div>
        """, unsafe_allow_html=True)

    with tc2:
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
            Locker Facility Utilization
        </div>
        """, unsafe_allow_html=True)
        
        locker_df = df_c[df_c['locker_type'] != 'None']['locker_type'].value_counts().reset_index()
        fig_lck = px.pie(
            locker_df, 
            names='locker_type', 
            values='count', 
            hole=0.6,
            color_discrete_sequence=['#38BDF8', '#818CF8', '#34D399']
        )
        fig_lck = plotly_dark_theme(fig_lck, height=270, show_legend=True)
        fig_lck.update_traces(marker=dict(line=dict(color=BG_CARD, width=2)), textinfo='percent')
        fig_lck.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5))
        st.plotly_chart(fig_lck, use_container_width=True)

    with tc3:
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
            Deposit Structure (Term vs. Liquid Balances)
        </div>
        """, unsafe_allow_html=True)
        
        prod_dist = pd.DataFrame({
            'Category': ['Fixed Deposits (FD)', 'Recurring Deposits (RD)', 'Liquid Balances (Savings/Current)'],
            'Volume': [df_p['fd_amount'].sum(), df_p['rd_amount'].sum(), df_c['balance'].sum()]
        })
        fig_prod = px.bar(
            prod_dist, 
            x='Volume', 
            y='Category', 
            orientation='h', 
            color='Category', 
            color_discrete_sequence=['#38BDF8', '#FBBF24', '#34D399']
        )
        fig_prod = plotly_dark_theme(fig_prod, height=270, show_legend=False)
        fig_prod.update_xaxes(title_text="Total Volume (₹)")
        fig_prod.update_yaxes(title_text="")
        st.plotly_chart(fig_prod, use_container_width=True)

# ==============================================================================
# TAB 3: Risk & Compliance (AML)
# ==============================================================================
with tab3:
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; display: flex; align-items: center; gap: 8px;">
            {icon_svg("shield-alert", size=18, color=COLOR_DANGER)}
            Anti-Money Laundering (AML) & Autonomous Threat Mitigation
        </div>
        <div style="font-size: 12px; color: {TEXT_MUTED};">
            3-Tier Escalation: Warn (50–75%) · Review (75–85%) · Auto-Block (&gt;85%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    rc1, rc2 = st.columns([1.6, 1.0])
    
    with rc1:
        r_sub1, r_sub2 = st.columns(2)
        with r_sub1:
            st.markdown(f"""
            <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
                Identified Fraud Pattern Vectors
            </div>
            """, unsafe_allow_html=True)
            
            fraud_subset = all_txns[all_txns['pattern_alert'] != 'None']
            if not fraud_subset.empty:
                pattern_counts = fraud_subset['pattern_alert'].value_counts().reset_index()
                fig_patterns = px.pie(
                    pattern_counts,
                    names='pattern_alert',
                    values='count',
                    hole=0.55,
                    color_discrete_sequence=['#F87171', '#FBBF24', '#38BDF8', '#818CF8']
                )
                fig_patterns = plotly_dark_theme(fig_patterns, height=240, show_legend=False)
                fig_patterns.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color=BG_CARD, width=2)))
                st.plotly_chart(fig_patterns, use_container_width=True)
            else:
                st.markdown(f"<div style='color: {TEXT_MUTED}; font-size: 12px;'>No anomaly vectors logged.</div>", unsafe_allow_html=True)
                
        with r_sub2:
            st.markdown(f"""
            <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
                Live Model Risk Probability (%)
            </div>
            """, unsafe_allow_html=True)
            
            if not live_df.empty:
                probs = live_df.tail(40)['fraud_prob'] * 100
                fig_prob = go.Figure(go.Scatter(
                    y=probs, 
                    mode='lines', 
                    line=dict(color=COLOR_DANGER, width=2.5), 
                    fill='tozeroy', 
                    fillcolor='rgba(248, 113, 113, 0.12)'
                ))
                fig_prob = plotly_dark_theme(fig_prob, height=240, x_tick=False)
                fig_prob.update_yaxes(range=[0, 100], title_text="Risk %", title_font=dict(size=10, color=TEXT_MUTED))
                st.plotly_chart(fig_prob, use_container_width=True)
            else:
                st.markdown(f"""
                <div style="background: {BG_CARD}; border: 1px dashed {BORDER_COLOR}; border-radius: 8px; height: 240px; display: flex; align-items: center; justify-content: center; color: {TEXT_MUTED}; font-size: 12px;">
                    Awaiting live probability stream...
                </div>
                """, unsafe_allow_html=True)

    with rc2:
        high_risk_count = len(df_c[df_c['risk_category'] == 'High'])
        pattern_matches_count = len(all_txns[all_txns['pattern_alert'] != 'None'])
        
        st.markdown(f"""
        <div class="section-card" style="border-left: 4px solid {COLOR_DANGER}; margin-bottom: 12px;">
            <div style="font-size: 11px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase;">AML Watchlist Alert</div>
            <div style="font-size: 24px; font-weight: 700; color: {COLOR_DANGER}; margin: 6px 0;">{high_risk_count:,} Accounts</div>
            <div style="font-size: 11px; color: {TEXT_SECONDARY};">Customers categorized in High-Risk AML tier</div>
        </div>
        
        <div class="section-card" style="border-left: 4px solid {COLOR_WARNING};">
            <div style="font-size: 11px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase;">Lifecycle Pattern Matches</div>
            <div style="font-size: 24px; font-weight: 700; color: {COLOR_WARNING}; margin: 6px 0;">{pattern_matches_count:,} Incidents</div>
            <div style="font-size: 11px; color: {TEXT_SECONDARY};">Total flagged anomalies in historical corpus</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""<div style="border-top: 1px solid {BORDER_COLOR}; margin: 18px 0;"></div>""", unsafe_allow_html=True)
    
    # Process Live Feed for Autonomous Bot
    if 'bot_logs' not in st.session_state:
        st.session_state['bot_logs'] = []
    if 'review_queue' not in st.session_state:
        st.session_state['review_queue'] = []
        
    if not live_df.empty:
        bot_alerts = live_df[live_df['pattern_alert'] != 'None'].sort_values('timestamp', ascending=False).head(20)
        for _, row in bot_alerts.iterrows():
            txn_id = row['transaction_id']
            if f"bot_processed_{txn_id}" not in st.session_state:
                prob = row.get('fraud_prob', 0) * 100
                cust = row['customer_id']
                t_str = datetime.now().strftime("%H:%M:%S")
                
                if prob > 85:
                    if cust not in st.session_state['blocked_accounts']:
                        st.session_state['blocked_accounts'].append(cust)
                        st.session_state['bot_logs'].append({'time': t_str, 'action': 'BLOCK', 'cust': cust, 'prob': prob})
                elif 75 < prob <= 85:
                    st.session_state['bot_logs'].append({'time': t_str, 'action': 'REVIEW', 'cust': cust, 'prob': prob})
                    if not any(r['txn_id'] == txn_id for r in st.session_state['review_queue']):
                        st.session_state['review_queue'].append({
                            'txn_id': txn_id, 'cust': cust, 'prob': prob,
                            'alert': row['pattern_alert'], 'category': row['category'], 'mode': row['mode']
                        })
                elif 50 <= prob <= 75:
                    st.session_state['bot_logs'].append({'time': t_str, 'action': 'WARN', 'cust': cust, 'prob': prob})
                    
                st.session_state[f"bot_processed_{txn_id}"] = True

    # 3-Column Bot Action Log
    st.markdown(f"""
    <div style="font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
        {icon_svg("cpu", size=16, color=ACCENT_PRIMARY)}
        Autonomous Containment Bot (Live Execution Stream)
    </div>
    """, unsafe_allow_html=True)
    
    bot_c1, bot_c2, bot_c3 = st.columns(3)
    
    with bot_c1:
        st.markdown(f"""
        <div style="font-size: 11px; font-weight: 600; color: {COLOR_DANGER}; text-transform: uppercase; margin-bottom: 6px;">
            Auto-Blocked (&gt; 85% Risk Score)
        </div>
        """, unsafe_allow_html=True)
        blocks = [log for log in st.session_state['bot_logs'] if log['action'] == 'BLOCK']
        if blocks:
            for b in blocks[-3:]:
                st.markdown(f"""
                <div style="background: rgba(248, 113, 113, 0.08); border-left: 3px solid {COLOR_DANGER}; padding: 8px 10px; margin-bottom: 6px; border-radius: 4px; font-size: 11px; color: {TEXT_PRIMARY};">
                    <span style="color: {TEXT_MUTED};">[{b['time']}]</span> Blocked <strong>{b['cust']}</strong> (Score: {b['prob']:.1f}%)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No critical threats auto-blocked in current session.")
            
    with bot_c2:
        st.markdown(f"""
        <div style="font-size: 11px; font-weight: 600; color: {ACCENT_PRIMARY}; text-transform: uppercase; margin-bottom: 6px;">
            Escalated to Review Queue (75–85%)
        </div>
        """, unsafe_allow_html=True)
        reviews = [log for log in st.session_state['bot_logs'] if log['action'] == 'REVIEW']
        if reviews:
            for r in reviews[-3:]:
                st.markdown(f"""
                <div style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid {ACCENT_PRIMARY}; padding: 8px 10px; margin-bottom: 6px; border-radius: 4px; font-size: 11px; color: {TEXT_PRIMARY};">
                    <span style="color: {TEXT_MUTED};">[{r['time']}]</span> Escalated <strong>{r['cust']}</strong> (Score: {r['prob']:.1f}%)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No pending cases escalated.")
            
    with bot_c3:
        st.markdown(f"""
        <div style="font-size: 11px; font-weight: 600; color: {COLOR_WARNING}; text-transform: uppercase; margin-bottom: 6px;">
            System Warnings Issued (50–75%)
        </div>
        """, unsafe_allow_html=True)
        warns = [log for log in st.session_state['bot_logs'] if log['action'] == 'WARN']
        if warns:
            for w in warns[-3:]:
                st.markdown(f"""
                <div style="background: rgba(251, 191, 36, 0.08); border-left: 3px solid {COLOR_WARNING}; padding: 8px 10px; margin-bottom: 6px; border-radius: 4px; font-size: 11px; color: {TEXT_PRIMARY};">
                    <span style="color: {TEXT_MUTED};">[{w['time']}]</span> Logged warning for <strong>{w['cust']}</strong> ({w['prob']:.1f}%)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No warnings recorded.")

    st.markdown(f"""<div style="border-top: 1px solid {BORDER_COLOR}; margin: 20px 0;"></div>""", unsafe_allow_html=True)
    
    # Employee Review Queue
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; display: flex; align-items: center; gap: 8px;">
            {icon_svg("users", size=16, color=ACCENT_PRIMARY)}
            Employee Review Queue (Human-in-the-Loop Decisions)
        </div>
        <div style="font-size: 11px; color: {TEXT_MUTED};">
            Pending Items: {len(st.session_state['review_queue'])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state['review_queue']:
        if st.button("Auto-Resolve All Pending (AI Secondary 65% Threshold)", use_container_width=True):
            for q in st.session_state['review_queue']:
                if q['prob'] > 65.0:
                    if q['cust'] not in st.session_state['blocked_accounts']:
                        st.session_state['blocked_accounts'].append(q['cust'])
            st.session_state['review_queue'] = []
            st.toast("Auto-Bot resolved pending items using secondary 65% threshold.")
            st.rerun()
            
        for q in reversed(st.session_state['review_queue']):
            st.markdown(f"""
            <div class="ticket-card">
                <div class="ticket-header">
                    <span class="ticket-title">
                        {icon_svg("shield-alert", size=15, color=ACCENT_PRIMARY)}
                        {q['alert']}
                    </span>
                    <span class="ticket-score-badge">RISK: {q['prob']:.1f}%</span>
                </div>
                <div class="ticket-body">
                    <strong>Entity:</strong> {q['cust']} &nbsp;|&nbsp; 
                    <strong>Operation:</strong> {q['category']} &nbsp;|&nbsp; 
                    <strong>Channel:</strong> {q['mode']}<br>
                    <span style="color: {TEXT_MUTED};">AI Assessment: Ambiguous probability vector requires compliance analyst verification before containment.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if st.button("Verify & Block", key=f"btn_blk_{q['txn_id']}", use_container_width=True):
                    st.session_state['blocked_accounts'].append(q['cust'])
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    st.toast(f"Confirmed threat: {q['cust']} account locked.")
                    st.rerun()
            with b2:
                if st.button("Clear as Safe", key=f"btn_clr_{q['txn_id']}", use_container_width=True):
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    st.toast(f"Transaction authorized. {q['cust']} cleared.")
                    st.rerun()
            with b3:
                if st.button("Raise Ticket", key=f"btn_tkt_{q['txn_id']}", use_container_width=True, help="Flag as false-positive for model retraining"):
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    st.toast(f"Dispute logged for {q['cust']}. Forwarded to ML Engineering.")
                    st.rerun()
            with b4:
                if st.button("AI Auto-Resolve", key=f"btn_ai_{q['txn_id']}", use_container_width=True):
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    if q['prob'] > 65.0:
                        st.session_state['blocked_accounts'].append(q['cust'])
                        st.toast(f"AI Decision: Locked {q['cust']} (Score > 65%).")
                    else:
                        st.toast(f"AI Decision: Approved {q['cust']} (Score <= 65%).")
                    st.rerun()
    else:
        st.markdown(f"""
        <div style="background: {BG_CARD}; border: 1px solid {BORDER_COLOR}; border-radius: 8px; padding: 20px; text-align: center; color: {COLOR_SUCCESS}; font-size: 13px;">
            {icon_svg("check-circle", size=20, color=COLOR_SUCCESS)}<br><br>
            All flagged cases have been resolved. The Employee Review Queue is clear.
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: AI Predictive Intelligence
# ==============================================================================
with tab4:
    st.markdown(f"""
    <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
        {icon_svg("brain", size=18, color=ACCENT_PRIMARY)}
        Prescriptive Security Intelligence & Model Attribution
    </div>
    """, unsafe_allow_html=True)
    
    col_ai1, col_ai2 = st.columns([1.2, 1.0])
    
    with col_ai1:
        st.markdown(f"""
        <div class="section-card" style="border-left: 4px solid {COLOR_DANGER}; margin-bottom: 14px;">
            <div style="font-size: 11px; font-weight: 700; color: {COLOR_DANGER}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                Critical Cyber Threat Advisory
            </div>
            <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; margin-bottom: 6px;">
                Coordinated Transfer Anomaly Detected in Online Channel
            </div>
            <div style="font-size: 12px; color: {TEXT_SECONDARY}; line-height: 1.5; margin-bottom: 10px;">
                Inference telemetry reveals clustered high-value debit operations originating from non-primary geographic locations targeting net banking rails.
            </div>
            <div style="background: {BG_SURFACE}; padding: 8px 12px; border-radius: 6px; font-size: 11px; color: {TEXT_PRIMARY}; border: 1px solid {BORDER_COLOR};">
                <strong>Prescribed Action:</strong> Enforce mandatory step-up authentication (hardware OTP / biometric token) for transfers exceeding ₹2,00,000.
            </div>
        </div>
        
        <div class="section-card" style="border-left: 4px solid {ACCENT_PRIMARY};">
            <div style="font-size: 11px; font-weight: 700; color: {ACCENT_PRIMARY}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                Commercial Yield Optimization
            </div>
            <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; margin-bottom: 6px;">
                Safety Locker Capacity Optimization
            </div>
            <div style="font-size: 12px; color: {TEXT_SECONDARY}; line-height: 1.5; margin-bottom: 10px;">
                Analytics indicate steady rental fee income from medium units, while 40% of institutional High-Balance accounts maintain unallocated vault capacity.
            </div>
            <div style="background: {BG_SURFACE}; padding: 8px 12px; border-radius: 6px; font-size: 11px; color: {TEXT_PRIMARY}; border: 1px solid {BORDER_COLOR};">
                <strong>Prescribed Action:</strong> Initiate targeted communication campaign offering introductory 50% discount on first-year medium locker leases for High Net-Worth retail segments.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ai2:
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">
                <span class="section-title">
                    {icon_svg("sliders", size=16, color=ACCENT_PRIMARY)}
                    Model Feature Attribution
                </span>
            </div>
            <div style="font-size: 12px; color: {TEXT_SECONDARY}; margin-bottom: 12px; line-height: 1.4;">
                Relative Gini feature importances calculated by the Random Forest classifier:
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate feature importances from actual model
        feature_names = ['amount', 'hour', 'location_change', 'balance_ratio', 'txn_frequency']
        feature_labels = {
            'balance_ratio': 'Amount-to-Balance Ratio',
            'location_change': 'Geographic Location Delta',
            'amount': 'Transaction Value (₹)',
            'txn_frequency': '5-Minute Velocity Spike',
            'hour': 'Time-of-Day Anomaly (Hour)'
        }
        
        try:
            importances = model.feature_importances_
            feat_df = pd.DataFrame({
                'Feature': [feature_labels.get(f, f) for f in feature_names],
                'Importance': importances
            }).sort_values('Importance', ascending=True)
            
            fig_feat = px.bar(
                feat_df,
                x='Importance',
                y='Feature',
                orientation='h',
                color='Importance',
                color_continuous_scale=['#0369A1', '#38BDF8']
            )
            fig_feat = plotly_dark_theme(fig_feat, height=220, show_legend=False)
            fig_feat.update_layout(coloraxis_showscale=False, margin=dict(t=10, b=10, l=10, r=10))
            fig_feat.update_xaxes(title_text="Relative Weight")
            fig_feat.update_yaxes(title_text="")
            st.plotly_chart(fig_feat, use_container_width=True)
        except Exception:
            st.caption("Feature importance calculation unavailable.")
            
        st.markdown("""</div>""", unsafe_allow_html=True)

# ==============================================================================
# TAB 5: Customer Care & CRM
# ==============================================================================
with tab5:
    st.markdown(f"""
    <div style="font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
        {icon_svg("message-square", size=18, color=ACCENT_PRIMARY)}
        Omni-Channel Customer Broadcast & Dispute Resolution
    </div>
    """, unsafe_allow_html=True)
    
    col_crm1, col_crm2 = st.columns([1.1, 1.0])
    
    with col_crm1:
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
            Broadcast Emergency Advisory
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("notice_form", clear_on_submit=True):
            notice_title = st.text_input("Advisory Heading", placeholder="e.g. Scheduled Core Banking Maintenance Window")
            notice_type = st.selectbox("Category", ["System Maintenance", "Security Advisory", "Service Downtime", "Compliance Notice"])
            notice_msg = st.text_area("Advisory Narrative", placeholder="Dear Customer,\nPlease be advised that UPI gateway services will undergo scheduled maintenance...", height=140)
            notice_urgency = st.selectbox("Urgency Level", ["Critical (Immediate Push)", "Elevated", "Informational"])
            
            p_title = notice_title if notice_title else "Advisory Title Preview"
            p_msg = notice_msg if notice_msg else "The formatted broadcast narrative will appear here for customer endpoints..."
            
            st.markdown(f"""
            <div style="background-color: {BG_CARD}; border: 1px dashed {BORDER_COLOR}; padding: 12px 14px; border-radius: 6px; margin: 12px 0;">
                <div style="font-size: 10px; color: {TEXT_MUTED}; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">
                    Simulated Customer Endpoint Preview
                </div>
                <div style="font-size: 12px; font-weight: 700; color: {ACCENT_PRIMARY}; margin-bottom: 4px;">
                    [FinEdge Official] {p_title}
                </div>
                <div style="font-size: 11px; color: {TEXT_SECONDARY}; line-height: 1.4; white-space: pre-wrap;">{p_msg}</div>
            </div>
            """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Publish Broadcast", use_container_width=True)
            if submitted and notice_title:
                st.session_state['notices'].append({
                    "id": f"NTC_{datetime.now().timestamp()}",
                    "title": notice_title,
                    "msg": notice_msg,
                    "urgency": notice_urgency,
                    "type": notice_type,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                st.toast(f"Broadcast published to {len(df_c):,} verified accounts.")
                st.rerun()

        # Active Broadcasts Registry
        if st.session_state['notices']:
            st.markdown(f"""<div style="border-top: 1px solid {BORDER_COLOR}; margin: 16px 0 12px 0;"></div>""", unsafe_allow_html=True)
            
            nb_header1, nb_header2 = st.columns([3, 2])
            with nb_header1:
                st.markdown(f"""<span style="font-size: 12px; font-weight: 600; color: {TEXT_PRIMARY};">Active Announcements</span>""", unsafe_allow_html=True)
            with nb_header2:
                if st.button("Revoke All", use_container_width=True):
                    st.session_state['notices'] = []
                    st.rerun()
                    
            for n in reversed(st.session_state['notices']):
                color = COLOR_DANGER if "Critical" in n['urgency'] else COLOR_WARNING if "Elevated" in n['urgency'] else ACCENT_PRIMARY
                n_id = n.get('id', n['time'])
                
                nc1, nc2 = st.columns([4, 1.2])
                with nc1:
                    st.markdown(f"""
                    <div style="border-left: 3px solid {color}; padding: 8px 12px; background: {BG_CARD}; margin-bottom: 8px; border-radius: 4px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="color: {TEXT_PRIMARY}; font-size: 12px;">[{n.get('type')}] {n['title']}</strong>
                            <span style="font-size: 10px; color: {TEXT_MUTED};">{n['time']}</span>
                        </div>
                        <div style="font-size: 11px; color: {TEXT_SECONDARY}; margin-top: 4px;">{n['msg'][:75]}...</div>
                    </div>
                    """, unsafe_allow_html=True)
                with nc2:
                    if st.button("Revoke", key=f"del_{n_id}", use_container_width=True):
                        st.session_state['notices'] = [x for x in st.session_state['notices'] if x.get('id', x['time']) != n_id]
                        st.toast("Advisory revoked.")
                        st.rerun()

        # Automated SMS Gateway
        st.markdown(f"""<div style="border-top: 1px solid {BORDER_COLOR}; margin: 20px 0 14px 0;"></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
            Automated SMS Notification Gateway
        </div>
        """, unsafe_allow_html=True)
        
        violators = df_c['min_bal_violation'].sum()
        st.caption(f"{violators:,} retail accounts currently breach mandatory minimum balance parameters.")
        
        if st.button("Dispatch Balance Warning SMS", use_container_width=True):
            violators_df = df_c[df_c['min_bal_violation'] == 1].head(3)
            for _, row in violators_df.iterrows():
                short_bal = f"₹{row['balance']:,.2f}"
                min_req = f"₹{row['min_balance']:,.2f}"
                st.markdown(f"""
                <div style="background-color: {BG_CARD}; padding: 8px 10px; border-left: 3px solid {ACCENT_PRIMARY}; margin-bottom: 6px; border-radius: 4px; font-family: monospace; font-size: 11px;">
                    <span style="color: {TEXT_MUTED};">[{datetime.now().strftime('%H:%M:%S')}] SMS Sent &rarr; </span> 
                    <strong style="color: {TEXT_PRIMARY};">{row['phone_number']}</strong> ({row['name']})<br>
                    <span style="color: {TEXT_SECONDARY};">"Dear {row['name']}, FinEdge {row['account_type']} balance is {short_bal}. Maintain minimum {min_req} to prevent regulatory penal charges."</span>
                </div>
                """, unsafe_allow_html=True)
            st.toast(f"Dispatched SMS notifications to {violators:,} accounts.")

    with col_crm2:
        st.markdown(f"""
        <div style="font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">
            Customer Service Ticket Registry
        </div>
        """, unsafe_allow_html=True)
        
        def style_priority(val):
            color = COLOR_DANGER if val == 'High' else COLOR_WARNING if val == 'Medium' else COLOR_SUCCESS
            return f'color: {color}; font-weight: 600'
            
        st.dataframe(
            df_tickets.style.map(style_priority, subset=['priority']),
            use_container_width=True,
            height=460,
            hide_index=True
        )

# --- Bottom Status Banner ---
status_str = "ACTIVE INGESTION STREAM" if simulate else "SYSTEM PAUSED"
st.markdown(f"""
<div style="text-align: center; font-size: 12px; font-weight: 500; color: {TEXT_MUTED}; padding: 24px 0 10px 0; border-top: 1px solid {BORDER_COLOR}; margin-top: 40px;">
    FinEdge Banking Intelligence Platform &nbsp;|&nbsp; Status: {status_str} &nbsp;|&nbsp; Engine: Random Forest Classifier v2.4 &nbsp;|&nbsp; Core Architecture: Real-Time Telemetry SOC
</div>
""", unsafe_allow_html=True)

# --- Background Telemetry Simulation Loop ---
if simulate:
    num_txns = np.random.randint(1, 4)
    for _ in range(num_txns):
        new_txn = generate_live_transaction(df_c, df_t)
        pred, prob = predict_fraud(model, new_txn)
        new_txn['predicted_fraud'] = pred
        new_txn['fraud_prob'] = prob
        
        idx = df_c.index[df_c['customer_id'] == new_txn['customer_id']].tolist()[0]
        if new_txn['type'] == 'Debit' and new_txn['category'] == 'Fund Transfer':
            st.session_state['customers'].at[idx, 'balance'] -= new_txn['amount']
        elif new_txn['type'] == 'Credit' and new_txn['category'] == 'Fund Transfer':
            st.session_state['customers'].at[idx, 'balance'] += new_txn['amount']
            
        st.session_state['live_feed'].append(new_txn)
        if len(st.session_state['live_feed']) > 150:
            st.session_state['live_feed'].pop(0)
            
    st.session_state['time_series_y'].pop(0)
    st.session_state['time_series_y'].append(num_txns)
    
    time.sleep(np.random.uniform(0.6, 1.4))
    st.rerun()
