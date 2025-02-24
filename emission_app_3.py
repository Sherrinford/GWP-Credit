import streamlit as st
import math

# --------------------------------------------------
# 1) PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(page_title="Emission Credit Calculator", layout="wide")

# --------------------------------------------------
# 2) CUSTOM CSS FOR SMALLER FONTS & STYLES
# --------------------------------------------------
st.markdown("""
<meta name="color-scheme" content="light"/>
<style>
/* Tell the browser to use a light color scheme */
:root {
    color-scheme: light !important;
}

/* Force main backgrounds to white */
html, body, [class*="css"] {
    background-color: #FFFFFF !important;
    color: #111 !important;
    font-size: 16px !important;
    line-height: 1.4 !important;
}

/* Make sure Streamlit's main container also has white bg */
[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
}

/* Make the sidebar distinct if desired */
[data-testid="stSidebar"] {
    background-color: #F0FFF0 !important;
}

/* Adjust font size for LaTeX (KaTeX) elements */
.katex-html .katex, .katex-display > .katex {
    font-size: 1.2em !important;
}

/* Desktop headings */
.header-style { 
    font-size: 32px !important; 
    font-weight: bold; 
    color: #2F4F4F; 
    margin-bottom: 1rem !important;
}
.subheader-style { 
    font-size: 24px !important; 
    color: #2E8B57; 
    border-bottom: 3px solid #2E8B57; 
    margin-top: 1.5rem !important;
    margin-bottom: 1.5rem !important;
}

/* Metric box styling */
.metric-box { 
    padding: 15px; 
    background: #F0FFF0; 
    border-radius: 12px; 
    margin: 12px 0; 
    font-size: 16px !important;
}

/* Expander header */
.streamlit-expanderHeader {
    font-size: 20px !important;
}

/* Responsive adjustments for mobile devices */
@media (max-width: 600px) {
    /* Slightly smaller text on narrow screens */
    html, body, [class*="css"] {
        font-size: 14px !important;
    }
    .header-style { 
        font-size: 24px !important; 
    }
    .subheader-style { 
        font-size: 20px !important; 
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    .metric-box { 
        padding: 10px; 
        font-size: 14px !important;
    }
    .streamlit-expanderHeader {
        font-size: 18px !important;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3) WEBPAGE HEADER
# --------------------------------------------------
st.markdown('<p class="header-style">🌍 CO₂-Equivalent Credit Calculator</p>', unsafe_allow_html=True)

# --------------------------------------------------
# 4) SIDEBAR WITH LOGO AND INPUTS
# --------------------------------------------------
with st.sidebar:
    # Logo at the top of the sidebar
    st.image("mylogo.png", width=120)
    
    st.header("⚙️ Input Parameters")
    E_CO2 = st.number_input("CO₂ Emissions Avoided (tonnes)", value=10.0, min_value=0.0)
    E_CH4 = st.number_input("CH₄ Emissions Avoided (tonnes)", value=1.0, min_value=0.0)
    
    col1, col2 = st.columns(2)
    with col1:
        GWP100 = st.number_input("GWP100 Factor", value=28.0, min_value=0.0)
    with col2:
        T = st.slider("Time Horizon (years)", 1, 50, 5)
    
    st.markdown("---")
    st.markdown("**Advanced RfP Parameters**")
    
    tau_CH4 = st.number_input("CH₄ Atmospheric Lifetime (years)", value=12.0)
    RE_ratio = st.number_input("Radiative Efficiency Ratio (RE₍CH₄₎/RE₍CO₂₎)", value=173.0)

# --------------------------------------------------
# 5) "Why 173?" EXPANDER
# --------------------------------------------------
with st.expander("Why 173?"):
    st.markdown(r"""
    ### Detailed Derivation of the 173 Ratio

    From IPCC data, the 20-year Global Warming Potential (GWP₂₀) for CH₄ is about 84.  
    This means:

    $$
    \text{GWP}_{20}(\text{CH}_4) 
      = \frac{\int_0^{20} \text{RF}_{\text{CH}_4}(t)\, dt}{\int_0^{20} \text{RF}_{\text{CO}_2}(t)\, dt}
      \approx 84
    $$

    **Step 1: Integrated forcing for CH₄**  
    If we assume an atmospheric lifetime $\tau_{\text{CH}_4} = 12$ years, the integrated forcing 
    for a pulse of methane over 20 years is:

    $$
    I_{\text{CH}_4} 
      = \int_0^{20} \left(\text{RE}_{\text{CH}_4} \times e^{-t/\tau_{\text{CH}_4}}\right)\, dt 
      = \text{RE}_{\text{CH}_4} \times \tau_{\text{CH}_4} \left(1 - e^{-20/\tau_{\text{CH}_4}} \right)
    $$

    **Step 2: Integrated forcing for CO₂**  
    For CO₂, we approximate its forcing as constant over 20 years:

    $$
    I_{\text{CO}_2} 
      \approx 20 \times \text{RE}_{\text{CO₂}}
    $$

    **Step 3: GWP₂₀**  
    Thus,

    $$
    \text{GWP}_{20}(\text{CH}_4) 
      = \frac{I_{\text{CH}_4}}{I_{\text{CO₂}}}
      = \frac{\text{RE}_{\text{CH}_4} \times \tau_{\text{CH}_4}\left(1 - e^{-20/\tau_{\text{CH}_4}}\right)}{20\, \text{RE}_{\text{CO₂}}}
      \approx 84
    $$

    Plugging in $\tau_{\text{CH}_4} = 12$ years:

    $$
    12 \times \left(1 - e^{-20/12}\right) \approx 9.72, 
    \quad 
    \frac{9.72}{20} \approx 0.486
    $$

    Therefore,

    $$
    84 
      = \left(\frac{\text{RE}_{\text{CH}_4}}{\text{RE}_{\text{CO}_2}} \right)\times 0.486
    \quad\Longrightarrow\quad
    \left(\frac{\text{RE}_{\text{CH}_4}}{\text{RE}_{\text{CO}_2}}\right) 
      \approx \frac{84}{0.486} 
      \approx 173
    $$

    This shows that, *instantaneously*, CH₄'s radiative efficiency is about 173 times that of CO₂. 
    Over 20 years, factoring in methane decay, the net effect is a GWP₂₀ of ~84.
    """)

# --------------------------------------------------
# 6) CALCULATION FUNCTIONS
# --------------------------------------------------
def calculate_gwp100_credits(E_CO2, E_CH4, gwp100):
    """Simple GWP100 calculation."""
    return E_CO2 + E_CH4 * gwp100

def calculate_rfp_credits(E_CO2, E_CH4, T, tau_CH4, re_ratio):
    """
    1) Integrated CH4 forcing: I_CH4 = tau_CH4 * (1 - e^(-T/tau_CH4))
    2) Effective conversion factor: C_RfP = (I_CH4 / T) * (RE_CH4 / RE_CO₂)
    3) Credits: E_CO₂ + E_CH₄ * C_RfP
    """
    integrated_CH4 = tau_CH4 * (1 - math.exp(-T / tau_CH4))
    conv_factor = re_ratio * (integrated_CH4 / T)
    return (E_CO2 + E_CH4 * conv_factor, conv_factor, integrated_CH4)

# --------------------------------------------------
# 7) PERFORM CALCULATIONS
# --------------------------------------------------
credits_gwp = calculate_gwp100_credits(E_CO2, E_CH4, GWP100)
credits_rfp, conv_factor, integrated_CH4 = calculate_rfp_credits(E_CO2, E_CH4, T, tau_CH4, RE_ratio)

# --------------------------------------------------
# 8) MAIN DISPLAY
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="subheader-style">📐 GWP100 Method</p>', unsafe_allow_html=True)
    
    # Show the GWP100 equation
    st.latex(r'''
        \text{Credits}_{\text{GWP100}} 
        = E_{CO_2} 
        + \left(E_{CH_4} \times \text{GWP100}\right)
    ''')
    
    st.markdown(f'''
    <div class="metric-box">
        <strong>🔢 Calculation Steps:</strong>
        <ul>
            <li>CO₂ Contribution: {E_CO2} tonnes</li>
            <li>CH₄ Contribution: {E_CH4} × {GWP100} = {E_CH4*GWP100:.1f} tonnes</li>
        </ul>
        <strong>🏁 Total Credits: {credits_gwp:.1f} tonnes CO₂e</strong>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="subheader-style">⚡ Radiative Forcing Protocol</p>', unsafe_allow_html=True)
    with st.expander("View Calculation Steps ▶"):
        st.markdown("**Step 1: Integrated CH₄ Forcing**")
        st.latex(r'''
            I_{CH_4} 
            = \tau_{CH_4} 
            \times 
            \left(1 - e^{-T/\tau_{CH_4}}\right)
        ''')
        st.markdown(f'''
            - τ_CH₄ = {tau_CH4} years  
            - T = {T} years  
            - Integrated CH₄ Forcing = {integrated_CH4:.2f} (unitless)
        ''')

        st.markdown("**Step 2: Effective Conversion Factor**")
        st.latex(r'''
            C_{RfP} 
            = \frac{I_{CH_4}}{T} 
            \times 
            \frac{RE_{CH_4}}{RE_{CO₂}}
        ''')
        st.markdown(f'''
            - RE Ratio = {RE_ratio}  
            - Effective Conversion Factor = {conv_factor:.2f}
        ''')

    st.markdown(f'''
    <div class="metric-box">
        <strong>🌱 Final Calculation:</strong>
        <ul>
            <li>CO₂ Contribution: {E_CO2} tonnes</li>
            <li>CH₄ Contribution: {E_CH4} × {conv_factor:.2f} = {E_CH4*conv_factor:.1f} tonnes</li>
        </ul>
        <strong>🏁 Total Credits: {credits_rfp:.1f} tonnes CO₂e</strong>
    </div>
    ''', unsafe_allow_html=True)

# --------------------------------------------------
# 9) COMPARISON SECTION
# --------------------------------------------------
st.markdown("---")
col_a, col_b, col_c = st.columns([1,2,1])
with col_b:
    st.markdown('<p class="subheader-style">📊 Method Comparison</p>', unsafe_allow_html=True)
    st.metric(label="GWP100 Credits", value=f"{credits_gwp:.1f} tCO₂e")
    st.metric(label="RfP Credits", value=f"{credits_rfp:.1f} tCO₂e", 
             delta=f"{(credits_rfp - credits_gwp):.1f} tCO₂e difference")
    st.caption(f"Comparison over {T}-year period")

# --------------------------------------------------
# 10) THEORY SECTION
# --------------------------------------------------
with st.expander("📖 Methodological Details"):
    st.markdown(r'''
    ### GWP100 Method
    $$
    \text{Credits}_{\text{GWP100}} 
      = E_{CO₂} 
      + \left(E_{CH₄} \times \text{GWP100}\right)
    $$
    Where:
    - $E_{CO₂}$ = CO₂ emissions avoided  
    - $E_{CH₄}$ = CH₄ emissions avoided  
    - GWP100 = Global Warming Potential over 100-year horizon  

    ### Radiative Forcing Protocol (RfP)
    **Integrated Forcing:**
    $$
    I_{CH₄} 
      = \tau_{CH₄} 
      \times 
      \left(1 - e^{-T/\tau_{CH₄}} \right)
    $$
    
    **Effective Conversion Factor:**
    $$
    C_{RfP} 
      = \frac{I_{CH₄}}{T} 
      \times 
      \frac{RE_{CH₄}}{RE_{CO₂}}
    $$
    
    **Final Credit Calculation:**
    $$
    \text{Credits}_{RfP} 
      = E_{CO₂} 
      + \left(E_{CH₄} \times C_{RfP}\right)
    $$
    ''')
