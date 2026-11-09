"""
Portal Web de Helpdesk — Interface premium em Streamlit
========================================================
A interface mantém o CRUD original através de banco.py, mas adiciona uma
experiência visual mais refinada: hero, indicadores, formulário em card,
estados vazios, feedbacks e uma tabela interativa com hierarquia visual.
"""

import streamlit as st
from banco import inserir_chamado, listar_chamados, atualizar_status, deletar_chamado


st.set_page_config(
    page_title="Helpdesk • Central de Chamados",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Design system
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #111827;
    --muted: #667085;
    --soft: #f6f8fb;
    --line: #e7ebf0;
    --card: rgba(255,255,255,.92);
    --brand: #5b4cf6;
    --brand-dark: #4035c9;
    --success: #16a36b;
    --warning: #d98b00;
    --danger: #d94f4f;
    --shadow-sm: 0 8px 24px rgba(17, 24, 39, .06);
    --shadow-md: 0 18px 50px rgba(17, 24, 39, .08);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(91,76,246,.08), transparent 28%),
        radial-gradient(circle at 90% 8%, rgba(28,181,148,.06), transparent 24%),
        #f8fafc;
}

.block-container {
    max-width: 1460px;
    padding: 2.2rem 2.8rem 3.5rem;
}

header[data-testid="stHeader"] {
    background: rgba(248,250,252,.72);
}

/* Esconde a navegação nativa para manter o visual limpo. */
#MainMenu, footer { visibility: hidden; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--line);
    border-radius: 22px;
    box-shadow: var(--shadow-sm);
    background: var(--card);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2.25rem;
    margin-bottom: 1.25rem;
    border: 1px solid rgba(91,76,246,.11);
    border-radius: 26px;
    background:
        radial-gradient(circle at 88% 18%, rgba(91,76,246,.16), transparent 25%),
        linear-gradient(135deg, #ffffff 0%, #f8f7ff 62%, #f3f5ff 100%);
    box-shadow: var(--shadow-md);
}

.hero::after {
    content: '';
    position: absolute;
    right: -70px;
    bottom: -100px;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(91,76,246,.06);
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .42rem .75rem;
    border-radius: 999px;
    background: #eeecff;
    color: #4c3fd2;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.hero-title {
    margin: .85rem 0 .35rem;
    color: var(--ink);
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2rem, 3.2vw, 3.35rem);
    line-height: 1.02;
    font-weight: 800;
    letter-spacing: -.045em;
}

.hero-subtitle {
    max-width: 760px;
    margin: 0;
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.65;
}

.section-head {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 1rem;
    margin: 1.5rem 0 .8rem;
}

.section-title {
    margin: 0;
    color: var(--ink);
    font-family: 'Manrope', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: -.02em;
}

.section-subtitle {
    margin: .2rem 0 0;
    color: var(--muted);
    font-size: .9rem;
}

.metric-card {
    position: relative;
    min-height: 120px;
    padding: 1.15rem 1.2rem;
    border: 1px solid var(--line);
    border-radius: 20px;
    background: rgba(255,255,255,.9);
    box-shadow: var(--shadow-sm);
}

.metric-label {
    color: #7a8495;
    font-size: .77rem;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
}

.metric-value {
    margin-top: .35rem;
    color: var(--ink);
    font-family: 'Manrope', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -.04em;
}

.metric-note {
    margin-top: .15rem;
    color: var(--muted);
    font-size: .82rem;
}

.metric-dot {
    position: absolute;
    top: 18px;
    right: 18px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--brand);
    box-shadow: 0 0 0 7px rgba(91,76,246,.08);
}

.form-shell {
    padding: 1.35rem 1.45rem 1.15rem;
    border: 1px solid var(--line);
    border-radius: 22px;
    background: rgba(255,255,255,.92);
    box-shadow: var(--shadow-sm);
}

.helper {
    margin-top: -.15rem;
    margin-bottom: .95rem;
    color: var(--muted);
    font-size: .88rem;
}

.small-badge {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: .3rem .62rem;
    background: #f1f3f7;
    color: #616b7c;
    font-size: .74rem;
    font-weight: 700;
}

.empty-state {
    padding: 3.2rem 1.5rem;
    text-align: center;
    border: 1px dashed #d7dce5;
    border-radius: 22px;
    background: rgba(255,255,255,.72);
}

.empty-icon {
    width: 54px;
    height: 54px;
    margin: 0 auto .9rem;
    display: grid;
    place-items: center;
    border-radius: 17px;
    background: #eeecff;
    font-size: 1.4rem;
}

.empty-title {
    color: var(--ink);
    font-family: 'Manrope', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
}

.empty-copy {
    max-width: 460px;
    margin: .35rem auto 0;
    color: var(--muted);
    line-height: 1.6;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    border: 0;
    border-radius: 12px;
    min-height: 46px;
    padding: 0 1.05rem;
    background: linear-gradient(135deg, var(--brand) 0%, #7d6cff 100%);
    color: #fff;
    font-weight: 800;
    box-shadow: 0 10px 24px rgba(91,76,246,.24);
    transition: .18s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 28px rgba(91,76,246,.28);
}

input, textarea, [data-baseweb="select"] > div {
    border-radius: 12px !important;
}

label p {
    color: #344054 !important;
    font-weight: 700 !important;
}

[data-testid="stDataEditor"] {
    border: 1px solid var(--line);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    background: #fff;
}

[data-testid="stDataEditor"] [role="columnheader"] {
    font-weight: 800;
}

.status-legend {
    display: flex;
    flex-wrap: wrap;
    gap: .55rem;
    justify-content: flex-end;
}

.dot-label {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    padding: .35rem .6rem;
    border-radius: 999px;
    background: #f4f5f7;
    color: #667085;
    font-size: .76rem;
    font-weight: 700;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.dot.open { background: #e4a11b; }
.dot.progress { background: #5b8def; }
.dot.done { background: #1fa971; }

@media (max-width: 900px) {
    .block-container { padding: 1rem 1rem 2.5rem; }
    .hero { padding: 1.55rem 1.2rem; }
    .hero-title { font-size: 2rem; }
    .section-head { display: block; }
    .status-legend { justify-content: flex-start; margin-top: .65rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


def metric_card(label: str, value: int, note: str, accent: str) -> str:
    return f"""
    <div class=\"metric-card\">
        <div class=\"metric-dot\" style=\"background:{accent};box-shadow:0 0 0 7px color-mix(in srgb, {accent} 11%, transparent);\"></div>
        <div class=\"metric-label\">{label}</div>
        <div class=\"metric-value\">{value}</div>
        <div class=\"metric-note\">{note}</div>
    </div>
    """


# -----------------------------------------------------------------------------
# Dados
# -----------------------------------------------------------------------------
df = listar_chamados()

if not df.empty:
    total = len(df)
    abertos = int((df["status"] == "Aberto").sum())
    andamento = int((df["status"] == "Em Andamento").sum())
    resolvidos = int((df["status"] == "Resolvido").sum())
else:
    total = abertos = andamento = resolvidos = 0

# -----------------------------------------------------------------------------
# Hero
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
    <div class="hero-kicker">● Central de atendimento</div>
    <div class="hero-title">Helpdesk que parece produto.<br>Feito para resolver.</div>
    <p class="hero-subtitle">
        Organize solicitações, acompanhe prioridades e mantenha cada chamado
        no lugar certo — em uma interface simples, rápida e profissional.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Indicadores
# -----------------------------------------------------------------------------
st.markdown('<div class="section-head"><div><div class="section-title">Visão geral</div><div class="section-subtitle">Status atual da operação</div></div></div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4, gap="medium")
with m1:
    st.markdown(metric_card("Chamados", total, "Total registrado", "#5b4cf6"), unsafe_allow_html=True)
with m2:
    st.markdown(metric_card("Abertos", abertos, "Aguardando atendimento", "#e4a11b"), unsafe_allow_html=True)
with m3:
    st.markdown(metric_card("Em andamento", andamento, "Sendo tratados agora", "#5b8def"), unsafe_allow_html=True)
with m4:
    st.markdown(metric_card("Resolvidos", resolvidos, "Atendimentos concluídos", "#1fa971"), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Novo chamado
# -----------------------------------------------------------------------------
st.markdown(
    '<div class="section-head"><div><div class="section-title">Abrir novo chamado</div><div class="section-subtitle">Descreva o problema para encaminhar ao atendimento.</div></div><span class="small-badge">Novo atendimento</span></div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="form-shell">', unsafe_allow_html=True)
    with st.form("form_novo_chamado", clear_on_submit=True):
        col_left, col_right = st.columns([1.55, 1], gap="large")
        with col_left:
            titulo = st.text_input("Título", placeholder="Ex.: Não consigo acessar o sistema financeiro")
            descricao = st.text_area(
                "Descrição",
                placeholder="Explique o que aconteceu, quando começou e qualquer detalhe que ajude na resolução.",
                height=150,
            )
        with col_right:
            prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], index=1)
            st.markdown(
                '<div class="helper">Use <strong>Alta</strong> para situações que bloqueiam o trabalho. Você poderá atualizar o status diretamente na lista.</div>',
                unsafe_allow_html=True,
            )
            enviado = st.form_submit_button("Abrir chamado", use_container_width=True)

        if enviado:
            if not titulo.strip() or not descricao.strip():
                st.warning("Preencha o título e a descrição antes de abrir o chamado.")
            else:
                inserir_chamado(titulo.strip(), descricao.strip(), prioridade)
                st.success("Chamado aberto com sucesso. Ele já está disponível na central.")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Lista / CRUD
# -----------------------------------------------------------------------------
st.markdown(
    '<div class="section-head"><div><div class="section-title">Central de chamados</div><div class="section-subtitle">Edite o status na própria tabela ou remova um registro quando necessário.</div></div><div class="status-legend"><span class="dot-label"><span class="dot open"></span>Aberto</span><span class="dot-label"><span class="dot progress"></span>Em andamento</span><span class="dot-label"><span class="dot done"></span>Resolvido</span></div></div>',
    unsafe_allow_html=True,
)

if df.empty:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">🎫</div>
            <div class="empty-title">Sua central está pronta para começar</div>
            <div class="empty-copy">Ainda não existe nenhum chamado cadastrado. Abra o primeiro atendimento acima para começar a acompanhar a operação.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.data_editor(
        df,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True, width="small"),
            "titulo": st.column_config.TextColumn("Título", disabled=True, width="large"),
            "descricao": st.column_config.TextColumn("Descrição", disabled=True, width="large"),
            "prioridade": st.column_config.TextColumn("Prioridade", disabled=True, width="medium"),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=["Aberto", "Em Andamento", "Resolvido"],
                width="medium",
                required=True,
            ),
        },
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_chamados",
    )

    mudancas = st.session_state.get("editor_chamados", {})
    houve_alteracao = False

    for indice, valores in mudancas.get("edited_rows", {}).items():
        if "status" in valores:
            chamado_id = int(df.iloc[indice]["id"])
            atualizar_status(chamado_id, valores["status"])
            houve_alteracao = True

    for indice in mudancas.get("deleted_rows", []):
        chamado_id = int(df.iloc[indice]["id"])
        deletar_chamado(chamado_id)
        houve_alteracao = True

    if houve_alteracao:
        st.rerun()

st.markdown(
    '<div style="margin-top:1.5rem;color:#98a2b3;text-align:center;font-size:.78rem;">Helpdesk • Central de Chamados · Operação simples, controle total.</div>',
    unsafe_allow_html=True,
)
