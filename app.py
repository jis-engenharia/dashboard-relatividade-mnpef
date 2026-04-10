import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(page_title="Relatividade Restrita - Jefferson Inocêncio", page_icon="📡")
st.title("📡 Dashboard de Física Contemporânea: Relatividade Restrita")
st.caption("MNPEF / IFF - Desenvolvido por: Jefferson Inocêncio")
st.caption("Comparação entre o referencial em repouso S e o referencial em movimento S′")

# ─────────────────────────────────────────────
# Sidebar — Parâmetros
# ─────────────────────────────────────────────
st.sidebar.header("⚙️ Parâmetros Ajustáveis")

h = st.sidebar.slider(
    "Distância h (metros)",
    min_value=1.0, max_value=1000.0, value=100.0, step=1.0,
    help="Distância percorrida pela luz no referencial em repouso"
)

v_pct = st.sidebar.slider(
    "Velocidade v ",
    min_value=0.0, max_value=300.0, value=15.0, step=0.1,
    help="Velocidade do referencial S′ em relação a S"
)

st.sidebar.markdown("**Velocidade da luz **")
modo_c = st.sidebar.radio(
    "Modo",
    ["Real  (≈ 3×10⁸ m/s)", "Fantasia (qualquer valor)"],
    horizontal=True
)

if modo_c == "Real  (≈ 3×10⁸ m/s)":
    c = st.sidebar.slider(
        "c (×10⁸ m/s)",
        min_value=1.000, max_value=3.000, value=3.0, step=0.001,
        format="%.3f"
    ) * 1e8
else:
    c = st.sidebar.number_input(
        "c (m/s) — ex: 30",
        min_value=1.0, max_value=3e8, value=30.0, step=1.0,
        format="%.1f",
        help="c = 30 m/s torna os efeitos relativísticos visíveis no cotidiano!"
    )

v = v_pct


# ─────────────────────────────────────────────
# Cálculos Físicos
# ─────────────────────────────────────────────
beta  = v / c                               # v/c
gamma = 1 / np.sqrt(1 - beta**2)           # Fator de Lorentz

# Referencial em Repouso (S')
delta_t_S  = h / c                          # tempo para a luz percorrer h
delta_s2_S = (c * delta_t_S)**2 - h**2     # intervalo espaço-tempo em S

# Referencial em Movimento (S)
delta_t_prime  = gamma * delta_t_S          # tempo dilatado em S′
L_prime        = c * delta_t_prime                  # comprimento contraído em S′
delta_s2_M     = (c * delta_t_prime)**2 - L_prime**2  # intervalo em S′ (deve = S)

# ─────────────────────────────────────────────
# Exibição — Dois Referenciais
# ─────────────────────────────────────────────
st.subheader("⚖️ Comparação entre os Referenciais")

col_S, col_divider, col_M = st.columns([1, 0.05, 1])

with col_S:
    st.markdown("### 🔵 Referencial S — em Repouso")
    s1, s2 = st.columns(2)
    s1.metric("Δt (tempo próprio)", f"{delta_t_S:.3e} s", help="h / c")
    s2.metric("Distância h", f"{h:.1f} m")
    s3, s4 = st.columns(2)
    s3.metric("Δs² (intervalo)", f"{delta_s2_S:.3e} m²", help="c²Δt² − h²")
    s4.metric("Fator γ", "1.0000", help="Referencial em repouso: γ = 1")

with col_M:
    st.markdown("### 🔴 Referencial S′ — em Movimento")
    m1, m2 = st.columns(2)
    m1.metric("Δt′ (tempo dilatado)", f"{delta_t_prime:.3e} s",
              delta=f"+{(delta_t_prime - delta_t_S):.3e} s",
              help="γ · Δt")
    m2.metric("L′ (comprimento contraído)", f"{L_prime:.3f} m",
              delta=f"{(L_prime - h):.3f} m",
              help="h / γ")
    m3, m4 = st.columns(2)
    m3.metric("Δs² (intervalo)", f"{delta_s2_M:.3e} m²", help="c²Δt′² − L′²")
    m4.metric("Fator γ", f"{gamma:.4f}", help="1 / √(1 − v²/c²)")

# Invariante
st.divider()
inv_col1, inv_col2, inv_col3 = st.columns([1, 2, 1])
with inv_col2:
    delta_inv = abs(delta_s2_S - delta_s2_M)
    if delta_inv < abs(delta_s2_S) * 1e-6 + 1e-20:
        st.success(
            f"✅ **Invariância confirmada!** Δs²(S) = Δs²(S′) = **{delta_s2_S:.3e} m²**\n\n"
            "O intervalo espaço-tempo é igual nos dois referenciais — essa é a essência da Relatividade Restrita."
        )
    else:
        st.warning(f"Δs²(S) = {delta_s2_S:.3e}  ≠  Δs²(S′) = {delta_s2_M:.3e}")

# ─────────────────────────────────────────────
# Interpretação física
# ─────────────────────────────────────────────
with st.expander("🧠 Interpretação Física"):
    if gamma >= 7:
        st.error(f"🚨 γ = {gamma:.2f} — extremamente próximo de c. Efeitos relativísticos massivos.")
    elif gamma >= 2:
        st.warning(f"⚠️ γ = {gamma:.2f} — tempo dilata {gamma:.2f}× e comprimento contrai {1/gamma:.2%}.")
    elif gamma >= 1.01:
        st.info(f"ℹ️ γ = {gamma:.4f} — Dois observadores em movimento relativo medem tempos diferentes para o mesmo fenômeno.")
    else:
        st.success("✅ Regime praticamente clássico. Newton ainda se sente em casa.")

    st.markdown(f"""
| Grandeza | Fórmula | Valor |
|---|---|---|
| Velocidade v | {v_pct} | {v:} m/s |
| β = v/c | v / c | {beta:.4f} |
| γ (Lorentz) | 1 / √(1−β²) | {gamma:.6f} |
| Δt (repouso S) | h / c | {delta_t_S:.3e} s |
| Δt′ (movimento S′) | γ · Δt | {delta_t_prime:.3e} s |
| h′ (S′) | cγΔt′ | {L_prime:.4f} m |
| Δs² (S) | c²Δt² − h² | {delta_s2_S:.3e} m² |
| Δs² (S′) | c²Δt′² − h′² | {delta_s2_M:.3e} m² |
""")

st.divider()

# ─────────────────────────────────────────────
# Gráficos
# ─────────────────────────────────────────────
st.subheader("📊 Gráficos")

v_arr   = np.linspace(0.0, 300.0, 400)
gamma_arr = 1 / np.sqrt(1 - v_arr**2)
dt_S_arr  = h / c
dt_M_arr  = gamma_arr * (h * c)
h_arr   = np.linspace(1, 1000, 400)
ds2_S_arr = (c * (h_arr / c))**2 - h_arr**2
ds2_M_arr = (c * (gamma * (h_arr / c)))**2 - (h_arr / gamma)**2

BLUE  = '#185FA5'
CORAL = '#993C1D'
RED   = '#E24B4A'
GRAY  = '#888780'

fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('#0e1117')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

plot_style = dict(facecolor='#1a1d24', labelcolor='#cccccc')

def style_ax(ax, xlabel, ylabel, title):
    ax.set_facecolor('#1a1d24')
    ax.tick_params(colors='#aaaaaa', labelsize=8)
    ax.spines[:].set_color('#333344')
    ax.set_xlabel(xlabel, color='#aaaaaa', fontsize=9)
    ax.set_ylabel(ylabel, color='#aaaaaa', fontsize=9)
    ax.set_title(title, color='#dddddd', fontsize=10, pad=8)
    ax.grid(True, color='#2a2a3a', linewidth=0.5, linestyle='--')

# ── Gráfico 1: γ vs v/c ──────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(v_arr, gamma_arr, color=BLUE, linewidth=2, label='γ(v)')
ax1.axvline(x=beta, color=RED, linestyle='--', linewidth=1, alpha=0.8, label=f'v atual = {v_pct}')
ax1.axhline(y=gamma, color='#EF9F27', linestyle='--', linewidth=1, alpha=0.8, label=f'γ = {gamma:.3f}')
ax1.scatter([beta], [gamma], color=RED, s=60, zorder=5)
ax1.set_xlim(0, 1)
style_ax(ax1, 'v / c', 'γ (Fator de Lorentz)', 'γ vs Velocidade')
ax1.legend(fontsize=7, facecolor='#1a1d24', labelcolor='#cccccc', edgecolor='#333344')

# ── Gráfico 2: Δt e Δt′ vs v/c ──────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(v_arr, np.full_like(v_arr, dt_S_arr), color=BLUE, linewidth=2, linestyle='-',  label='Δt — repouso S')
ax2.plot(v_arr, dt_M_arr,                       color=CORAL, linewidth=2, linestyle='--', label="Δt′ — movimento S′")
ax2.axvline(x=beta, color=RED, linestyle=':', linewidth=1, alpha=0.7)
ax2.scatter([beta], [delta_t_S],     color=BLUE,  s=60, zorder=5)
ax2.scatter([beta], [delta_t_prime], color=CORAL, s=60, zorder=5)
style_ax(ax2, 'v / c', 'Tempo (s)', 'Δt e Δt′ vs Velocidade')
ax2.legend(fontsize=7, facecolor='#1a1d24', labelcolor='#cccccc', edgecolor='#333344')

# ── Gráfico 3: Δs² vs h ──────────────────────
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(h_arr, ds2_S_arr, color=BLUE,  linewidth=2, linestyle='-',  label='Δs² — repouso S')
ax3.plot(h_arr, ds2_M_arr, color=CORAL, linewidth=2, linestyle='--', label="Δs² — movimento S′")
ax3.axvline(x=h, color=RED, linestyle=':', linewidth=1, alpha=0.7)
ax3.axhline(y=0, color=GRAY, linewidth=0.8, linestyle=':')
ax3.scatter([h], [delta_s2_S], color=BLUE,  s=60, zorder=5)
ax3.scatter([h], [delta_s2_M], color=CORAL, s=60, zorder=5)
style_ax(ax3, 'Altura h (m)', 'Δs² (m²)', 'Intervalo Δs² vs h (invariância)')
ax3.legend(fontsize=7, facecolor='#1a1d24', labelcolor='#cccccc', edgecolor='#333344')

# ── Gráfico 4: L′ vs v/c ─────────────────────
ax4 = fig.add_subplot(gs[1, 0])
L_prime_arr = h / gamma_arr
ax4.plot(v_arr, np.full_like(v_arr, h), color=BLUE,  linewidth=2, linestyle='-',  label='h — repouso S′ ')
ax4.plot(v_arr, L_prime_arr,            color=CORAL, linewidth=2, linestyle='--', label="h′ — movimento S")
ax4.axvline(x=beta, color=RED, linestyle=':', linewidth=1, alpha=0.7)
ax4.scatter([beta], [h],       color=BLUE,  s=60, zorder=5)
ax4.scatter([beta], [L_prime], color=CORAL, s=60, zorder=5)
style_ax(ax4, 'v / c', 'Comprimento (m)', 'Contração do Comprimento vs v')
ax4.legend(fontsize=7, facecolor='#1a1d24', labelcolor='#cccccc', edgecolor='#333344')

# ── Gráfico 5: Diagrama espaço-tempo (Minkowski) ─
ax5 = fig.add_subplot(gs[1, 1])
t_line = np.linspace(0, delta_t_S * 1.5, 200)
ax5.plot(np.zeros_like(t_line), c * t_line, color=BLUE,  linewidth=2, label="Linha de mundo S'")
ax5.plot(beta * c * t_line,     c * t_line, color=CORAL, linewidth=2, linestyle='--', label="Linha de mundo S")
ax5.plot([0, h], [0, c * delta_t_S], color='#EF9F27', linewidth=1.5, linestyle=':', label='Trajetória da luz')
ax5.scatter([0],  [c * delta_t_S],  color=BLUE,  s=50, zorder=5)
ax5.scatter([v * delta_t_prime], [c * delta_t_prime], color=CORAL, s=50, zorder=5)
style_ax(ax5, 'Posição x (m)', 'ct (m)', 'Diagrama Espaço-Tempo (Minkowski)')
ax5.legend(fontsize=7, facecolor='#1a1d24', labelcolor='#cccccc', edgecolor='#333344')

# ── Gráfico 6: Energia cinética relativística ─
ax6 = fig.add_subplot(gs[1, 2])
m = 1.0  # massa de referência = 1 kg
KE_rel  = (gamma_arr - 1) * m * c**2
KE_class = 0.5 * m * (v_arr * c)**2
ax6.plot(v_arr, KE_rel,   color=BLUE,  linewidth=2, label='Ec relativística')
ax6.plot(v_arr, KE_class, color=CORAL, linewidth=2, linestyle='--', label='Ec clássica (Newton)')
KE_atual = (gamma - 1) * m * c**2
ax6.axvline(x=beta, color=RED, linestyle=':', linewidth=1, alpha=0.7)
ax6.scatter([beta], [KE_atual], color=RED, s=60, zorder=5)
style_ax(ax6, 'v / c', 'Energia cinética (J)', 'Ec Relativística vs Clássica (m=1kg)')
ax6.legend(fontsize=7, facecolor='#1a1d24', labelcolor='#cccccc', edgecolor='#333344')

st.pyplot(fig)
plt.close(fig)

# ─────────────────────────────────────────────
# Rodapé
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
**Fórmulas utilizadas:**
`γ = 1/√(1−v²/c²)` &nbsp;|&nbsp;
`Δt = h/c` &nbsp;|&nbsp;
`Δt′ = γ·Δt` &nbsp;|&nbsp;
`h′ = cγΔt′` &nbsp;|&nbsp;
`Δs² = c²Δt² − h²` &nbsp;|&nbsp;
`Ec = (γ−1)mc²`
""")
