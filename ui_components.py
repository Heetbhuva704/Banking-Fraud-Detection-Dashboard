"""
FinEdge Enterprise UI Components & Icons Module
Provides pixel-perfect SVG Lucide-style icons and reusable styled HTML blocks.
"""

# Color Palette Constants
BG_MAIN = "#0B1120"
BG_SIDEBAR = "#111827"
BG_CARD = "#151F32"
BG_SURFACE = "#1B263B"
BORDER_COLOR = "#2A3850"
BORDER_SUBTLE = "#1E293B"
TEXT_PRIMARY = "#F1F5F9"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#64748B"
ACCENT_PRIMARY = "#38BDF8"    # Sky blue
ACCENT_SECONDARY = "#818CF8"  # Indigo
COLOR_SUCCESS = "#34D399"     # Emerald
COLOR_WARNING = "#FBBF24"     # Amber
COLOR_DANGER = "#F87171"      # Rose/Coral
COLOR_INFO = "#38BDF8"

def icon_svg(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 2.0) -> str:
    """Returns pure inline SVG for enterprise Lucide icons."""
    svg_attrs = (
        f'width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"'
    )
    
    icons = {
        # Navigation & System
        "building": f'<svg {svg_attrs}><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>',
        "activity": f'<svg {svg_attrs}><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
        "shield": f'<svg {svg_attrs}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "shield-alert": f'<svg {svg_attrs}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        "brain": f'<svg {svg_attrs}><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/><path d="M16 8h2a2 2 0 0 1 2 2v1"/><path d="M18 15h-2"/><path d="M8 8H6a2 2 0 0 0-2 2v1"/><path d="M6 15h2"/></svg>',
        "users": f'<svg {svg_attrs}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        "lock": f'<svg {svg_attrs}><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
        "unlock": f'<svg {svg_attrs}><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>',
        "wallet": f'<svg {svg_attrs}><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>',
        "landmark": f'<svg {svg_attrs}><line x1="2" y1="22" x2="22" y2="22"/><line x1="4" y1="10" x2="4" y2="18"/><line x1="8" y1="10" x2="8" y2="18"/><line x1="12" y1="10" x2="12" y2="18"/><line x1="16" y1="10" x2="16" y2="18"/><line x1="20" y1="10" x2="20" y2="18"/><polygon points="12 2 20 7 4 7"/></svg>',
        "chart": f'<svg {svg_attrs}><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "check-circle": f'<svg {svg_attrs}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        "alert-circle": f'<svg {svg_attrs}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        "x-circle": f'<svg {svg_attrs}><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        "bell": f'<svg {svg_attrs}><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
        "database": f'<svg {svg_attrs}><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
        "search": f'<svg {svg_attrs}><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
        "sliders": f'<svg {svg_attrs}><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>',
        "radio": f'<svg {svg_attrs}><circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/></svg>',
        "refresh": f'<svg {svg_attrs}><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21h5v-5"/></svg>',
        "message-square": f'<svg {svg_attrs}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        "send": f'<svg {svg_attrs}><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
        "map-pin": f'<svg {svg_attrs}><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
        "check": f'<svg {svg_attrs}><polyline points="20 6 9 17 4 12"/></svg>',
        "x": f'<svg {svg_attrs}><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
        "cpu": f'<svg {svg_attrs}><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        "ticket": f'<svg {svg_attrs}><path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2"/><path d="M13 11v2"/><path d="M13 17v2"/></svg>',
        "arrow-up-right": f'<svg {svg_attrs}><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>',
        "arrow-down-right": f'<svg {svg_attrs}><line x1="7" y1="7" x2="17" y2="17"/><polyline points="17 7 17 17 7 17"/></svg>',
        "info": f'<svg {svg_attrs}><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        "file-text": f'<svg {svg_attrs}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    }
    return icons.get(name, icons["activity"])

def get_enterprise_css() -> str:
    """Returns clean, institutional dark theme stylesheet."""
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Core app surface */
    .stApp {{
        background-color: {BG_MAIN};
        color: {TEXT_PRIMARY};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    
    /* Typography defaults */
    h1, h2, h3, h4, h5, h6, p, span, div, label, input, button, select, textarea {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    
    /* Hide Streamlit chrome */
    #MainMenu, footer, header {{ visibility: hidden; }}
    div[data-testid="stToolbar"] {{ display: none; }}
    
    /* Global scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {BG_MAIN}; }}
    ::-webkit-scrollbar-thumb {{ background: {BORDER_COLOR}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {TEXT_MUTED}; }}
    
    /* Main container padding */
    .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px;
    }}
    
    /* Header layout */
    .finedge-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0 16px 0;
        border-bottom: 1px solid {BORDER_COLOR};
        margin-bottom: 20px;
    }}
    .finedge-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .finedge-logo-box {{
        width: 38px;
        height: 38px;
        border-radius: 8px;
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        border: 1px solid #38BDF8;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.2);
    }}
    .finedge-title {{
        font-size: 20px;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}
    .finedge-subtitle {{
        font-size: 12px;
        color: {TEXT_SECONDARY};
        font-weight: 500;
    }}
    .finedge-meta {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }}
    .status-badge-sim {{
        background: rgba(56, 189, 248, 0.1);
        color: {ACCENT_PRIMARY};
        border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .status-badge-active {{
        background: rgba(52, 211, 153, 0.1);
        color: {COLOR_SUCCESS};
        border: 1px solid rgba(52, 211, 153, 0.3);
    }}
    .status-badge-paused {{
        background: rgba(248, 113, 113, 0.1);
        color: {COLOR_DANGER};
        border: 1px solid rgba(248, 113, 113, 0.3);
    }}
    .status-indicator-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: inline-block;
    }}
    .dot-active {{ background-color: {COLOR_SUCCESS}; box-shadow: 0 0 6px {COLOR_SUCCESS}; }}
    .dot-paused {{ background-color: {COLOR_DANGER}; }}
    
    /* Modern KPI Cards */
    .kpi-card {{
        background: {BG_CARD};
        border: 1px solid {BORDER_COLOR};
        border-radius: 10px;
        padding: 16px 18px;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .kpi-card:hover {{
        border-color: {ACCENT_PRIMARY};
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }}
    .kpi-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }}
    .kpi-label {{
        font-size: 12px;
        font-weight: 600;
        color: {TEXT_SECONDARY};
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .kpi-icon-wrap {{
        color: {ACCENT_PRIMARY};
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .kpi-value {{
        font-size: 26px;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}
    .kpi-footer {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 11px;
        color: {TEXT_MUTED};
        margin-top: 8px;
        padding-top: 6px;
        border-top: 1px solid {BORDER_SUBTLE};
    }}
    .kpi-pill {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
    }}
    .kpi-pill-neutral {{ background: {BG_SURFACE}; color: {TEXT_SECONDARY}; }}
    .kpi-pill-alert {{ background: rgba(248, 113, 113, 0.15); color: {COLOR_DANGER}; border: 1px solid rgba(248, 113, 113, 0.3); }}
    
    /* Institutional Section Containers */
    .section-card {{
        background: {BG_CARD};
        border: 1px solid {BORDER_COLOR};
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 18px;
    }}
    .section-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 12px;
        margin-bottom: 14px;
        border-bottom: 1px solid {BORDER_SUBTLE};
    }}
    .section-title {{
        font-size: 14px;
        font-weight: 600;
        color: {TEXT_PRIMARY};
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.01em;
    }}
    
    /* Live Feed Transaction Items */
    .txn-item {{
        background: {BG_SURFACE};
        border: 1px solid {BORDER_COLOR};
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .txn-item:hover {{
        border-color: {ACCENT_PRIMARY};
        transform: translateX(2px);
    }}
    .txn-item-fraud {{
        border-left: 4px solid {COLOR_DANGER};
        background: rgba(248, 113, 113, 0.05);
    }}
    .txn-item-normal {{
        border-left: 4px solid {COLOR_SUCCESS};
        background: rgba(52, 211, 153, 0.03);
    }}
    .txn-row-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .txn-id {{
        font-family: 'JetBrains Mono', Consolas, monospace !important;
        font-size: 12px;
        font-weight: 600;
        color: {TEXT_PRIMARY};
    }}
    .txn-amount {{
        font-size: 13px;
        font-weight: 700;
    }}
    .txn-amount-fraud {{ color: {COLOR_DANGER}; }}
    .txn-amount-normal {{ color: {COLOR_SUCCESS}; }}
    .txn-row-bottom {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        color: {TEXT_MUTED};
    }}
    .txn-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .badge-fraud {{ background: rgba(248, 113, 113, 0.15); color: {COLOR_DANGER}; }}
    .badge-normal {{ background: rgba(52, 211, 153, 0.15); color: {COLOR_SUCCESS}; }}
    .badge-channel {{ background: {BG_CARD}; color: {TEXT_SECONDARY}; border: 1px solid {BORDER_COLOR}; }}
    
    /* Review Queue Ticket Card */
    .ticket-card {{
        background: {BG_CARD};
        border: 1px solid {BORDER_COLOR};
        border-left: 4px solid {ACCENT_PRIMARY};
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }}
    .ticket-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}
    .ticket-title {{
        font-size: 13px;
        font-weight: 600;
        color: {ACCENT_PRIMARY};
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .ticket-score-badge {{
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        background: rgba(56, 189, 248, 0.15);
        color: {ACCENT_PRIMARY};
        border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .ticket-body {{
        font-size: 12px;
        color: {TEXT_SECONDARY};
        line-height: 1.5;
        margin-bottom: 10px;
    }}
    
    /* Institutional Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {BG_CARD};
        padding: 4px;
        border-radius: 8px;
        border: 1px solid {BORDER_COLOR};
        gap: 4px;
        margin-bottom: 18px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 13px;
        font-weight: 600;
        color: {TEXT_SECONDARY};
        padding: 8px 16px;
        border-radius: 6px;
        border: none !important;
        background: transparent;
        transition: all 0.15s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {TEXT_PRIMARY};
        background: {BG_SURFACE};
    }}
    .stTabs [aria-selected="true"] {{
        color: #FFFFFF !important;
        background-color: {ACCENT_PRIMARY} !important;
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }}
    .stTabs [data-baseweb="tab-border"] {{ display: none; }}
    
    /* Sidebar Enterprise Styling */
    section[data-testid="stSidebar"] {{
        background-color: {BG_SIDEBAR};
        border-right: 1px solid {BORDER_COLOR};
    }}
    section[data-testid="stSidebar"] .block-container {{
        padding: 1.5rem 1rem !important;
    }}
    
    /* Form fields */
    div[data-baseweb="select"] > div,
    input, textarea {{
        background-color: {BG_CARD} !important;
        border-color: {BORDER_COLOR} !important;
        color: {TEXT_PRIMARY} !important;
        border-radius: 6px !important;
    }}
    
    /* Streamlit Alert Callouts */
    div[data-testid="stAlert"] {{
        background-color: {BG_CARD} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 8px !important;
        color: {TEXT_PRIMARY} !important;
        padding: 10px 14px !important;
    }}
    </style>
    """

def card_kpi_html(label: str, value: str, icon_name: str, subtitle: str, trend_text: str = "", trend_type: str = "neutral") -> str:
    """Generates clean HTML string for institutional KPI card."""
    svg = icon_svg(icon_name, size=18, color=ACCENT_PRIMARY)
    
    pill_html = ""
    if trend_text:
        cls = "kpi-pill-alert" if trend_type == "alert" else "kpi-pill-neutral"
        pill_html = f'<span class="kpi-pill {cls}">{trend_text}</span>'
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">{label}</span>
            <div class="kpi-icon-wrap">{svg}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-footer">
            <span>{subtitle}</span>
            {pill_html}
        </div>
    </div>
    """

def header_bar_html(is_live: bool, last_update_time: str) -> str:
    """Renders the top enterprise header bar."""
    status_class = "status-badge-active" if is_live else "status-badge-paused"
    dot_class = "dot-active" if is_live else "dot-paused"
    status_label = "ACTIVE TELEMETRY" if is_live else "SYSTEM PAUSED"
    
    logo_svg = icon_svg("building", size=20, color="#FFFFFF")
    
    return f"""
    <div class="finedge-header">
        <div class="finedge-brand">
            <div class="finedge-logo-box">
                {logo_svg}
            </div>
            <div>
                <div class="finedge-title">FinEdge</div>
                <div class="finedge-subtitle">Banking Intelligence & Security Operations Center</div>
            </div>
        </div>
        <div class="finedge-meta">
            <span class="status-badge status-badge-sim">SIMULATION ENVIRONMENT</span>
            <span class="status-badge {status_class}">
                <span class="status-indicator-dot {dot_class}"></span>
                {status_label}
            </span>
            <span style="font-size: 11px; color: {TEXT_MUTED}; font-weight: 500;">
                {last_update_time}
            </span>
        </div>
    </div>
    """

def plotly_dark_theme(fig, height: int = 250, show_legend: bool = False, x_tick: bool = True):
    """Applies standardized institutional dark styling to Plotly charts."""
    fig.update_layout(
        plot_bgcolor=BG_CARD,
        paper_bgcolor=BG_CARD,
        font=dict(family="Inter, sans-serif", color=TEXT_SECONDARY, size=11),
        height=height,
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=show_legend,
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=BORDER_SUBTLE,
        zeroline=False,
        showline=False,
        tickfont=dict(size=10, color=TEXT_MUTED),
        showticklabels=x_tick
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=BORDER_SUBTLE,
        zeroline=False,
        showline=False,
        tickfont=dict(size=10, color=TEXT_MUTED)
    )
    return fig
