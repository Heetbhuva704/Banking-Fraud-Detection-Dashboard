import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from data_generator import generate_initial_data, generate_live_transaction
from model_trainer import train_fraud_model, predict_fraud

st.set_page_config(page_title="FinEdge Command Center", layout="wide", page_icon="🏦")

# --- Custom Premium CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp { background-color: #0F172A; color: #E5E7EB; }
    h1, h2, h3, h4, h5, p, span, div, strong, label { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #E5E7EB; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .top-banner { 
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #06B6D4; padding: 25px 20px; border-radius: 16px; 
        text-align: center; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5); margin-bottom: 30px;
        border: 1px solid #334155;
    }
    
    .bottom-banner { text-align: center; font-size: 14px; font-weight: 600; color: #9CA3AF; padding: 20px; margin-top: 40px; border-top: 1px solid #334155;}
    
    .kpi-card { background: #1E293B; border-radius: 16px; padding: 24px; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; margin-bottom: 25px; }
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(6, 182, 212, 0.1); border-color: #06B6D4; }
    .kpi-icon { font-size: 28px; margin-bottom: 12px; }
    .kpi-title { color: #9CA3AF; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
    .kpi-value { color: #F8FAFC; font-size: 32px; font-weight: 800; letter-spacing: -1px; }
    .kpi-trend { font-size: 12px; font-weight: 700; margin-top: 8px; display: inline-block; padding: 4px 10px; border-radius: 20px; }
    .trend-neutral { background: #334155; color: #E5E7EB; }
    .trend-danger { background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulseGlow { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
    .blink-dot { height: 10px; width: 10px; background-color: #EF4444; border-radius: 50%; display: inline-block; margin-right: 8px; animation: pulseGlow 2s infinite; }
    
    .feed-card { background: #1E293B; border-radius: 12px; padding: 16px; margin-bottom: 12px; border: 1px solid #334155; border-left-width: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); animation: slideIn 0.3s ease-out; transition: all 0.2s; }
    .feed-card:hover { transform: scale(1.02); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4); }
    .fraud-feed { border-left-color: #EF4444; background-color: rgba(239, 68, 68, 0.08); }
    .normal-feed { border-left-color: #22C55E; background-color: rgba(34, 197, 94, 0.05); }
    
    .sys-card { background: #1E293B; border-radius: 16px; padding: 20px; border: 1px solid #334155; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2); transition: all 0.3s;}
    .sys-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4); }
    .sys-card h5 { margin-top: 0; color: #06B6D4 !important; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #334155; padding-bottom: 10px; }
    .sys-value { font-size: 28px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px; margin-top: 10px;}
    .sys-sub { font-size: 13px; color: #9CA3AF; font-weight: 600;}
    
    .stTabs [data-baseweb="tab-list"] { background-color: #1E293B; padding: 8px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3); gap: 8px; border: 1px solid #334155; }
    .stTabs [data-baseweb="tab"] { font-weight: 700; color: #9CA3AF; padding: 12px 20px; border-radius: 12px; font-size: 14px; transition: all 0.2s; border: none !important; }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; background: linear-gradient(135deg, #06B6D4, #3B82F6) !important; box-shadow: 0 0 15px rgba(6, 182, 212, 0.4); }
    
    .action-tag { display: inline-block; background-color: #06B6D4; color: #0F172A; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 11px; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;}
    .category-badge { font-size: 11px; padding: 3px 8px; border-radius: 6px; background-color: #334155; color: #E5E7EB; margin-left: 8px; font-weight: 700; border: 1px solid #475569;}
    
    .action-btn { background-color: #1E293B; border: 1px solid #475569; color: #E5E7EB; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; cursor: pointer; display: inline-block; margin-right: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.2); transition: all 0.2s;}
    .action-btn:hover { background-color: #334155; color: #FFFFFF; border-color: #9CA3AF; box-shadow: 0 4px 6px rgba(0,0,0,0.3);}
    .btn-block { color: #EF4444; border-color: rgba(239, 68, 68, 0.5); background-color: rgba(239, 68, 68, 0.1);}
    .btn-block:hover { background-color: rgba(239, 68, 68, 0.2); border-color: #EF4444; color: #FFFFFF;}
    </style>
""", unsafe_allow_html=True)

# --- Initialization ---
if 'initialized' not in st.session_state or 'tickets' not in st.session_state or 'phone_number' not in st.session_state.get('customers', pd.DataFrame()).columns:
    with st.spinner("Connecting to Core Banking Mainframe..."):
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
        st.session_state['time_series_y'] = [0]*50
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

# --- Sidebar Controls ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=60)
    st.markdown("### 🎛️ Command Controls")
    simulate = st.toggle("📡 Engage Live System", value=False)
    st.markdown("---")
    st.markdown(f"**AI Model Acc:** `{st.session_state['accuracy']*100:.1f}%`")
    st.selectbox("Timeframe", ["Live Feed (Active)", "Last 24 Hrs", "YTD"])

# --- Top Banner ---
st.markdown('<div class="top-banner">🏦 FinEdge Bank – Command Center</div>', unsafe_allow_html=True)

# --- KPIs ---
avg_balance = df_c['balance'].mean()
total_advances = df_p['loan_amount'].sum()
fraud_count = all_txns['is_fraud'].sum()

k1, k2, k3, k4 = st.columns(4)

new_flags = len(live_df[live_df['predicted_fraud']==1]) if not live_df.empty else 0
live_flags_str = f"+{new_flags} Live Flags" if new_flags > 0 else "System Stable"
trend_class = "trend-danger" if new_flags > 0 else "trend-neutral"

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-title">Average Balance</div>
        <div class="kpi-value">₹{avg_balance:,.0f}</div>
        <div class="kpi-trend trend-neutral">System Average</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🏦</div>
        <div class="kpi-title">Loan Portfolio</div>
        <div class="kpi-value">₹{total_advances/10000000:.1f} Cr</div>
        <div class="kpi-trend trend-neutral">Active Book</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left: 5px solid {'#EF4444' if new_flags > 0 else '#E2E8F0'};">
        <div class="kpi-icon">🚨</div>
        <div class="kpi-title">Threat Detects</div>
        <div class="kpi-value">{fraud_count:,}</div>
        <div class="kpi-trend {trend_class}">{live_flags_str}</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🔐</div>
        <div class="kpi-title">Active Lockers</div>
        <div class="kpi-value">{len(df_c[df_c['locker_type']!='None']):,}</div>
        <div class="kpi-trend trend-neutral">Generating Fee</div>
    </div>
    """, unsafe_allow_html=True)

# --- Tabs ---
t1, t2, t3, t4, t5 = st.tabs(["📡 Live Telemetry Dashboard", "🏦 Treasury", "🚨 Risk & AML", "💡 AI Insights", "💬 Customer Care & CRM"])

# --- TAB 1: Live Telemetry Dashboard ---
with t1:
    st.markdown(f"<h4>Dynamic Network Telemetry | System: {'<span class=\"blink-dot\"></span> ACTIVE 🟢' if simulate else 'PAUSED 🔴'}</h4>", unsafe_allow_html=True)
    
    if len(st.session_state['live_feed']) < 5:
        st.info("Activate 'Engage Live System' in the sidebar and wait a few seconds to populate live charts.")
    
    c_live1, c_live2 = st.columns([2, 1])
    
    with c_live1:
        st.markdown("**Live Operational Volume (per second)**")
        fig_live_line = go.Figure(go.Scatter(
            x=st.session_state['time_series_x'], 
            y=st.session_state['time_series_y'], 
            mode='lines', fill='tozeroy', 
            line=dict(color='#06B6D4', width=3),
            fillcolor='rgba(6, 182, 212, 0.2)'
        ))
        fig_live_line.update_layout(plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', height=250, margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showticklabels=False))
        st.plotly_chart(fig_live_line, use_container_width=True)

        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            st.markdown("**Live Event Categorization**")
            if not live_df.empty:
                live_cat = live_df.tail(50)['category'].value_counts().reset_index()
                fig_live_pie = px.pie(live_cat, names='category', values='count', hole=0.6, color_discrete_sequence=['#3B82F6', '#06B6D4', '#F59E0B', '#EF4444', '#9CA3AF'])
                fig_live_pie.update_layout(plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', height=250, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
                fig_live_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#1E293B', width=2)))
                st.plotly_chart(fig_live_pie, use_container_width=True)
            else:
                st.write("Awaiting data...")
                
        with c_sub2:
            st.markdown("**Live Threat Detection**")
            if not live_df.empty:
                live_threat = live_df.tail(50)['predicted_fraud'].value_counts().reset_index()
                live_threat['Status'] = live_threat['predicted_fraud'].map({0: 'Normal', 1: 'Fraud'})
                fig_live_bar = px.bar(live_threat, x='Status', y='count', color='Status', color_discrete_map={'Normal': '#22C55E', 'Fraud': '#EF4444'})
                fig_live_bar.update_layout(plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', height=250, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
                st.plotly_chart(fig_live_bar, use_container_width=True)
            else:
                st.write("Awaiting data...")
        
    with c_live2:
        st.markdown("**Live Omni-Channel Stream**")
        feed_container = st.container(height=550)
        with feed_container:
            for txn in reversed(st.session_state['live_feed'][-15:]):
                amount_str = f"₹{txn['amount']:,}" if txn['amount'] > 0 else "System Action"
                if txn['predicted_fraud'] == 1:
                    st.markdown(f"""
                    <div class="feed-card fraud-feed">
                        <strong>{txn['customer_id']} | <span style="color:#EF4444;">{amount_str}</span></strong>
                        <span class="category-badge">{txn['category']}</span><br>
                        <span style="font-size: 13px; color: #9CA3AF;">📍 {txn['location']}</span> <br>
                        <span style="font-size: 12px; font-weight: bold; color: #EF4444;">⚠️ Suspicious</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="feed-card normal-feed">
                        <strong>{txn['customer_id']} | <span style="color:#22C55E;">{amount_str}</span></strong>
                        <span class="category-badge">{txn['category']}</span><br>
                        <span style="font-size: 13px; color: #9CA3AF;">📍 {txn['location']}</span> <br>
                        <span style="font-size: 12px; font-weight: bold; color: #22C55E;">✅ Normal</span>
                    </div>
                    """, unsafe_allow_html=True)

# --- TAB 2: Treasury & Core Banking ---
with t2:
    st.markdown("<h4>Core Financial Health</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1.5])
    
    with c1:
        st.markdown(f"""
        <div class="sys-card">
            <h5>Minimum Balance Violations</h5>
            <div class="sys-value">{df_c['min_bal_violation'].sum():,}</div>
            <div class="sys-sub">Accounts facing penal charges</div>
        </div>
        <div class="sys-card">
            <h5>Total Interest Earned</h5>
            <div class="sys-value">₹{df_p['total_interest_earned'].sum()/100000:.2f} L</div>
            <div class="sys-sub">Customer payouts</div>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Insight:** Gold loans currently contribute the highest proportional interest revenue per capita.")
        
    with c2:
        st.markdown("**Locker Facility Distribution**")
        locker_dist = df_c[df_c['locker_type'] != 'None']['locker_type'].value_counts().reset_index()
        fig_lck = px.pie(locker_dist, names='locker_type', values='count', hole=0.6, color_discrete_sequence=['#3B82F6', '#06B6D4', '#F59E0B'])
        fig_lck.update_layout(
            plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', 
            margin=dict(t=20, b=40, l=10, r=10), 
            height=260,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        fig_lck.update_traces(marker=dict(line=dict(color='#1E293B', width=3)), textinfo='percent')
        st.plotly_chart(fig_lck, use_container_width=True)

    with c3:
        st.markdown("**Deposit Distribution (FD/RD vs Savings/Current)**")
        prod_dist = pd.DataFrame({
            'Category': ['Term Deposits (FD)', 'Recurring (RD)', 'Liquid (Sav/Cur)'],
            'Volume': [df_p['fd_amount'].sum(), df_p['rd_amount'].sum(), df_c['balance'].sum()]
        })
        fig_prod = px.bar(prod_dist, x='Volume', y='Category', orientation='h', color='Category', color_discrete_sequence=['#06B6D4', '#F59E0B', '#3B82F6'])
        fig_prod.update_layout(plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', showlegend=False, margin=dict(t=0, b=0))
        st.plotly_chart(fig_prod, use_container_width=True)

# --- TAB 3: Risk & Compliance (AML) ---
with t3:
    st.markdown("<h4>Live Threat Intelligence Engine</h4>", unsafe_allow_html=True)
    
    if len(st.session_state['live_feed']) < 5:
        st.info("Activate 'Engage Live System' to stream real-time threat telemetry.")
        
    c_risk1, c_risk2 = st.columns([1.5, 1])
    
    with c_risk1:
        c_r_sub1, c_r_sub2 = st.columns(2)
        with c_r_sub1:
            st.markdown("**Live Threat Vector Distribution**")
            if not live_df.empty:
                live_fraud = live_df[live_df['predicted_fraud'] == 1]
                if not live_fraud.empty:
                    threat_counts = live_fraud['pattern_alert'].value_counts().reset_index()
                    fig_threat_pie = px.pie(threat_counts, names='pattern_alert', values='count', hole=0.5,
                                           color_discrete_sequence=['#EF4444', '#F59E0B', '#1E3A8A', '#14B8A6'])
                    fig_threat_pie.update_layout(plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', height=280, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
                    fig_threat_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#1E293B', width=2)))
                    st.plotly_chart(fig_threat_pie, use_container_width=True)
                else:
                    st.success("No active threats in current window ✅")
            else:
                st.write("Awaiting data...")
                
        with c_r_sub2:
            st.markdown("**Live Risk Probability Tracker (%)**")
            if not live_df.empty:
                live_prob = live_df.tail(50)['fraud_prob'] * 100
                fig_prob = go.Figure(go.Scatter(y=live_prob, mode='lines', line=dict(color='#EF4444', width=3), fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.2)'))
                fig_prob.update_layout(plot_bgcolor='#1E293B', paper_bgcolor='#1E293B', font_color='#E5E7EB', height=280, margin=dict(t=10, b=10, l=10, r=10), yaxis=dict(range=[0, 100]), xaxis=dict(showticklabels=False))
                st.plotly_chart(fig_prob, use_container_width=True)
            else:
                st.write("Awaiting data...")

    with c_risk2:
        st.markdown(f"""
        <div class="sys-card" style="border-left: 4px solid #EF4444;">
            <h5>AML Watchlist Alert</h5>
            <div class="sys-value">{len(df_c[df_c['risk_category']=='High']):,}</div>
            <div class="sys-sub">High-Risk Customers Identified</div>
        </div>
        <div class="sys-card" style="border-left: 4px solid #F59E0B;">
            <h5>Cumulative Suspicious Operations</h5>
            <div class="sys-value">{len(all_txns[all_txns['pattern_alert']!='None']):,}</div>
            <div class="sys-sub">Total Lifecycle Pattern Matches</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("<h4>🤖 Autonomous Risk Bot (Live Agent Action Log)</h4>", unsafe_allow_html=True)
    st.info("The AI Agent actively monitors incoming telemetry and executes autonomous actions based on probability thresholds (50-75% Warn | 75-85% Employee Review | >85% Auto-Block).")
    
    bot_c1, bot_c2, bot_c3 = st.columns(3)
    
    if 'bot_logs' not in st.session_state:
        st.session_state['bot_logs'] = []
    if 'review_queue' not in st.session_state:
        st.session_state['review_queue'] = []
    
    # Process Live Feed for Autonomous Bot
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
                
    with bot_c1:
        st.markdown("**🛑 Auto-Blocked (>85%)**")
        blocks = [log for log in st.session_state['bot_logs'] if log['action'] == 'BLOCK']
        if blocks:
            for b in blocks[-3:]:
                st.markdown(f"<div style='background: rgba(239, 68, 68, 0.1); border-left: 3px solid #EF4444; padding: 10px; margin-bottom: 8px; border-radius: 4px; font-size: 13px; color: #E5E7EB;'>[{b['time']}] Blocked {b['cust']} ({b['prob']:.1f}%)</div>", unsafe_allow_html=True)
        else:
            st.caption("No recent blocks.")
            
    with bot_c2:
        st.markdown("**👁️ Employee Review Queue (75-85%)**")
        reviews = [log for log in st.session_state['bot_logs'] if log['action'] == 'REVIEW']
        if reviews:
            for r in reviews[-3:]:
                st.markdown(f"<div style='background: rgba(6, 182, 212, 0.1); border-left: 3px solid #06B6D4; padding: 10px; margin-bottom: 8px; border-radius: 4px; font-size: 13px; color: #E5E7EB;'>[{r['time']}] Flagged {r['cust']} ({r['prob']:.1f}%)</div>", unsafe_allow_html=True)
        else:
            st.caption("No recent flags.")
            
    with bot_c3:
        st.markdown("**⚠️ Warnings Issued (50-75%)**")
        warns = [log for log in st.session_state['bot_logs'] if log['action'] == 'WARN']
        if warns:
            for w in warns[-3:]:
                st.markdown(f"<div style='background: rgba(245, 158, 11, 0.1); border-left: 3px solid #F59E0B; padding: 10px; margin-bottom: 8px; border-radius: 4px; font-size: 13px; color: #E5E7EB;'>[{w['time']}] Warned {w['cust']} ({w['prob']:.1f}%)</div>", unsafe_allow_html=True)
        else:
            st.caption("No recent warnings.")

    st.markdown("---")
    st.markdown("<h4>👨‍💻 Employee Review Queue (Pending Decisions)</h4>", unsafe_allow_html=True)
    
    if st.session_state['review_queue']:
        if st.button("🤖 Auto-Resolve All Pending (AI Bot)", use_container_width=True, help="Automatically block >65% risk and clear <=65% risk"):
            for q in st.session_state['review_queue']:
                if q['prob'] > 65.0:
                    if q['cust'] not in st.session_state['blocked_accounts']:
                        st.session_state['blocked_accounts'].append(q['cust'])
            st.session_state['review_queue'] = []
            st.toast("✅ Auto-Bot has successfully resolved all pending items based on 65% threshold.")
            st.rerun()
            
        for q in reversed(st.session_state['review_queue']):
            st.markdown(f"""
            <div style="background-color: rgba(6, 182, 212, 0.05); padding: 16px; border-left: 5px solid #06B6D4; margin-top: 12px; border-radius: 8px 8px 0px 0px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <strong style="color: #06B6D4; font-size: 15px;">🤖 BOT FLAGGED: {q['alert']}</strong>
                    <span style="background: #06B6D4; color: #0F172A; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;">RISK SCORE: {q['prob']:.1f}% (REVIEW REQUIRED)</span>
                </div>
                <div style="font-size: 13px; color: #9CA3AF; line-height: 1.5;">
                    <strong>Target Entity:</strong> {q['cust']} | <strong>Operation:</strong> {q['category']} <br>
                    <strong>AI Diagnostics:</strong> Suspicious {q['mode']} execution. Score too low for auto-block. Manual verification required.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='background-color: #1E293B; padding: 8px 16px; border: 1px solid #334155; border-top: none; border-radius: 0px 0px 8px 8px; margin-bottom: 12px;'>", unsafe_allow_html=True)
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            
            with btn_col1:
                if st.button(f"🚫 Verify & Block", key=f"rev_blk_{q['txn_id']}"):
                    st.session_state['blocked_accounts'].append(q['cust'])
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    st.toast(f"✅ Employee confirmed threat. {q['cust']} Blocked.")
                    st.rerun()
            
            with btn_col2:
                if st.button("✅ Clear as Safe", key=f"rev_clr_{q['txn_id']}"):
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    st.toast(f"✅ Employee cleared transaction as safe.")
                    st.rerun()
                    
            with btn_col3:
                if st.button("🎫 Raise Ticket", key=f"rev_tkt_{q['txn_id']}", help="Mark as False Positive & alert Engineering Team"):
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    st.toast(f"🎫 False-Positive Ticket raised for {q['cust']}! ML Team notified.")
                    st.rerun()
                    
            with btn_col4:
                if st.button("🤖 AI Auto-Resolve", key=f"rev_ai_{q['txn_id']}", help="Let the AI make the final call based on a 65% threshold"):
                    st.session_state['review_queue'] = [x for x in st.session_state['review_queue'] if x['txn_id'] != q['txn_id']]
                    if q['prob'] > 65.0:
                        st.session_state['blocked_accounts'].append(q['cust'])
                        st.toast(f"🤖 AI Decision: Blocked {q['cust']} (Risk > 65%).")
                    else:
                        st.toast(f"🤖 AI Decision: Cleared {q['cust']} as safe (Risk <= 65%).")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("🎉 Employee Review Queue is currently empty. All flagged items processed.")

# --- TAB 4: AI Insights Panel ---
with t4:
    st.markdown("<h4>Prescriptive Recommendations</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #334155; color: #E5E7EB; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
            <div class="action-tag">FRAUD RISK RECOMMENDATION</div>
            <h3 style="color: #F8FAFC;">High probability of coordinated attack in Online Channel</h3>
            <p style="color: #9CA3AF; font-size: 15px;">Model detects multiple high-value transactions originating from mismatched locations targeting Online portals.<br>
            <strong>System Action:</strong> Step-up authentication required for transfers > ₹2,00,000.</p>
        </div>
        <div style="background: #0F172A; border: 1px solid #334155; color: #E5E7EB; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
            <div class="action-tag" style="background-color: #F59E0B; color: #0F172A;">BUSINESS SUGGESTION</div>
            <h3 style="color: #F8FAFC;">Locker Capacity Optimization</h3>
            <p style="color: #E5E7EB; font-size: 15px;">Medium lockers are generating steady fee income but 40% of 'High Balance' customers do not own a locker.<br>
            <strong>System Action:</strong> Launch automated email campaign offering 50% off first-year Medium Locker rentals to High Net-Worth Individuals.</p>
        </div>
    """, unsafe_allow_html=True)

# --- TAB 5: Customer Care & CRM ---
with t5:
    st.markdown("<h4>Customer Relationship & Notice Management</h4>", unsafe_allow_html=True)
    
    c_crm1, c_crm2 = st.columns([1, 1])
    with c_crm1:
        st.markdown("**Broadcast Notice to Customers**")
        with st.form("notice_form", clear_on_submit=True):
            notice_title = st.text_input("Notice Title", placeholder="e.g. Scheduled UPI Maintenance")
            notice_type = st.selectbox("Category", ["Maintenance", "Fraud Alert", "System Downtime", "Promotional"])
            notice_msg = st.text_area("Message Body", placeholder="Dear Customer,\nUPI services will undergo scheduled maintenance...", height=180)
            notice_urgency = st.selectbox("Urgency", ["High", "Medium", "Low"])
            
            p_title = notice_title if notice_title else "Notice Title Preview"
            p_msg = notice_msg if notice_msg else "Your broadcast message will appear here..."
            
            st.markdown("""
            <div style="background-color: #1E293B; border: 1px dashed #475569; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <span style="font-size: 11px; color: #9CA3AF; font-weight: bold; text-transform: uppercase;">📢 Customer Device Preview</span><br>
                <div style="margin-top: 10px; font-family: sans-serif; color: #F8FAFC;">
                    <strong>[FinEdge]</strong> <span style="font-weight: bold; color: #06B6D4;">""" + p_title + """</span><br>
                    <span style="font-size: 13px; color: #9CA3AF; white-space: pre-wrap;">""" + p_msg + """</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Execute Broadcast")
            
            if submitted and notice_title:
                st.session_state['notices'].append({
                    "id": f"NTC_{datetime.now().timestamp()}",
                    "title": notice_title, 
                    "msg": notice_msg, 
                    "urgency": notice_urgency,
                    "type": notice_type,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                st.success(f"✅ Executed {notice_type} broadcast to {len(df_c):,} verified devices.")
                
        if st.session_state['notices']:
            h_col1, h_col2 = st.columns([3, 2])
            with h_col1:
                st.markdown("**Active System Broadcasts:**")
            with h_col2:
                if st.button("⚠️ Clear All Broadcasts", use_container_width=True):
                    st.session_state['notices'] = []
                    st.rerun()
                    
            for n in reversed(st.session_state['notices']):
                color = "#EF4444" if n['urgency'] == "High" else "#F59E0B" if n['urgency'] == "Medium" else "#06B6D4"
                n_id = n.get('id', n['time'])
                
                n_col1, n_col2 = st.columns([5, 2])
                with n_col1:
                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding: 12px; background: #1E293B; margin-bottom: 10px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.2);">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="color: {color}; font-size: 14px;">[{n.get('type', 'Alert')}] {n['title']}</strong>
                            <span style="font-size: 11px; background: #334155; padding: 2px 6px; border-radius: 4px; color: #E5E7EB;">{n['time']}</span>
                        </div>
                        <div style="font-size: 13px; color: #9CA3AF; margin-top: 5px;">{n['msg'][:80]}...</div>
                    </div>
                    """, unsafe_allow_html=True)
                with n_col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("❌ Remove", key=f"del_{n_id}"):
                        st.session_state['notices'] = [x for x in st.session_state['notices'] if x.get('id', x['time']) != n_id]
                        st.toast("✅ Broadcast successfully revoked.")
                        st.rerun()
                
        st.markdown("---")
        st.markdown("**Automated SMS Gateway (Live Dispatch)**")
        violators = df_c['min_bal_violation'].sum()
        violators_df = df_c[df_c['min_bal_violation'] == 1].head(3)
        
        st.warning(f"⚠️ {violators:,} accounts currently operating below minimum balance requirements.")
        if st.button("Dispatch Targeted SMS Warnings"):
            st.success(f"Gateway connection established. Routing SMS to {violators:,} numbers...")
            for _, row in violators_df.iterrows():
                short_bal = f"₹{row['balance']:,.2f}"
                min_req = f"₹{row['min_balance']:,.2f}"
                st.markdown(f"""
                <div style="background-color: #F3F4F6; padding: 10px; border-left: 3px solid #14B8A6; margin-bottom: 5px; border-radius: 4px; font-family: monospace;">
                    <span style="color: #6B7280;">[{datetime.now().strftime('%H:%M:%S')}] SMS Sent -> </span> 
                    <strong>{row['phone_number']}</strong> ({row['name']})<br>
                    <span style="color: #0B1F3A;">"Dear {row['name']}, your FinEdge {row['account_type']} balance is {short_bal}. Please fund your account to maintain the required {min_req} min balance to avoid penal charges."</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 12px; color: #6B7280;'>... and {violators - 3} more messages dispatched successfully.</span>", unsafe_allow_html=True)
                
    with c_crm2:
        st.markdown("**Active Support Tickets**")
        
        def highlight_priority(val):
            color = '#EF4444' if val == 'High' else '#F59E0B' if val == 'Medium' else '#22C55E'
            return f'color: {color}; font-weight: bold'
            
        st.dataframe(
            df_tickets.style.map(highlight_priority, subset=['priority']),
            use_container_width=True, 
            height=400,
            hide_index=True
        )


# --- Bottom Banner ---
st.markdown(f'<div class="bottom-banner">📡 System Status: {"LIVE 🟢" if simulate else "PAUSED 🔴"} | Last Updated: Live | AI Engine: Random Forest v2.4</div>', unsafe_allow_html=True)

# --- Simulation Engine ---
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
    
    time.sleep(np.random.uniform(0.5, 1.5))
    st.rerun()
