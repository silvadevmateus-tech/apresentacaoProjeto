import pandas as pd
from pathlib import Path
import streamlit as st
import plotly.express as px

def procurarBase():
    
    pasta_raiz = Path(__file__).resolve().parent
    arquivo_base = (pasta_raiz / "basesAva" / f"report_1790612574.xlsx")
    
    base = pd.read_excel(arquivo_base, dtype={"categoria": str})
    return base

def acessoAva():

    # =========================================================
    # CSS
    # =========================================================
    st.markdown("""
    <style>

    /* =====================================================
       CONTAINER
    ===================================================== */

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }


    /* =====================================================
       TÍTULOS
    ===================================================== */

    h1 {
        color: var(--text-color) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: var(--text-color) !important;
    }


    /* =====================================================
       CARDS
    ===================================================== */

    [data-testid="stMetric"] {

        background-color: var(--secondary-background-color);

        border: 1px solid rgba(128,128,128,0.20);

        border-radius: 14px;

        padding: 20px;

        box-shadow:
            0px 2px 8px rgba(0,0,0,0.08);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }


    [data-testid="stMetric"]:hover {

        transform: translateY(-3px);

        border-color: #61B5E8;

        box-shadow:
            0px 6px 18px rgba(0,0,0,0.15);
    }


    /* Label */

    [data-testid="stMetricLabel"] p {

        color: var(--text-color) !important;

        opacity: 0.70;

        font-size: 12px !important;

        font-weight: 600 !important;

        text-transform: uppercase;

        letter-spacing: 0.3px;
    }


    /* Valor */

    [data-testid="stMetricValue"] {

        color: var(--text-color) !important;

        font-size: 30px !important;

        font-weight: 700 !important;
    }


    [data-testid="stMetricValue"] div {

        color: var(--text-color) !important;
    }


    /* =====================================================
       DATAFRAME
    ===================================================== */

    [data-testid="stDataFrame"] {

        border: 1px solid rgba(128,128,128,0.20);

        border-radius: 12px;

        overflow: hidden;
    }


    /* =====================================================
       TABS
    ===================================================== */

    [data-baseweb="tab-list"] {
        gap: 8px;
    }

    [data-baseweb="tab"] p {

        color: var(--text-color) !important;

        opacity: 0.70;

        font-weight: 600;
    }

    [data-baseweb="tab"][aria-selected="true"] p {

        color: #61B5E8 !important;

        opacity: 1;
    }


    /* =====================================================
       DIVISOR
    ===================================================== */

    hr {

        border-color: rgba(128,128,128,0.20) !important;

        margin-top: 1.5rem;

        margin-bottom: 1.5rem;
    }


    /* =====================================================
       CAPTION
    ===================================================== */

    [data-testid="stCaptionContainer"] {

        color: var(--text-color) !important;

        opacity: 0.65;
    }


    [data-testid="stCaptionContainer"] p {

        color: var(--text-color) !important;
    }

    </style>
    """, unsafe_allow_html=True)


    # =========================================================
    # CABEÇALHO
    # =========================================================

    st.title("📊 Monitoramento de Acesso ao AVA")

    st.caption(
        "Acompanhamento dos acessos dos professores às disciplinas "
        "e identificação de salas sem registro de acesso."
    )


    # =========================================================
    # BASE
    # =========================================================

    base = procurarBase()

    base = base.loc[
        base["categoria"].str.contains(
            "2026",
            na=False
        )
    ]

    base = base.loc[
        ~base["categoria_curso"].str.contains(
            "- AM",
            na=False
        )
    ]

    with st.sidebar:
            st.title("⚙️ Filtros")
    
            st.caption("Utilize os filtros abaixo para refinar os dados.")
    
            periodo = st.selectbox(
                "Período letivo",
                ["Todos"] + sorted(
                    base["categoria"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )
            
        
            curso = st.selectbox(
                "Curso",
                ["Todos"] + sorted(
                    base["categoria_curso"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )
        
            st.divider()
    
            st.caption("Os indicadores e gráficos são atualizados conforme os filtros.")

    # =========================================================
    # INDICADORES
    # =========================================================
    if periodo != "Todos":
        base = base[
            base["categoria"].astype(str) == str(periodo)
        ]
    if curso != "Todos":
        base = base[
            base["categoria_curso"].astype(str) == str(curso)
        ]
            
    quantidadeRegistros = len(base)

    quantidadeProfessor = (
        base
        .drop_duplicates(subset="professor")
    )

    quantidadeNuncaAcessou = base[
        base["ultimo_acesso"] == "Nunca acessou"
    ]


    # Evita divisão por zero
    if quantidadeRegistros > 0:

        percentualSemAcesso = (
            len(quantidadeNuncaAcessou)
            * 100
            / quantidadeRegistros
        )

    else:

        percentualSemAcesso = 0


    # =========================================================
    # AGRUPAMENTOS
    # =========================================================

    totalSemAcessoCurso = (
        quantidadeNuncaAcessou
        .groupby("categoria_curso")["ultimo_acesso"]
        .count()
        .sort_values(ascending=False)
        .reset_index(
            name="QTD_SALAS_SEM_ACESSO"
        )
    )


    totalSemAcessoProfessor = (
        quantidadeNuncaAcessou
        .groupby("professor")["ultimo_acesso"]
        .count()
        .sort_values(ascending=False)
        .reset_index(
            name="QTD_SALAS_SEM_ACESSO"
        )
    )


    periodoSemAcesso = (
        quantidadeNuncaAcessou
        .groupby("categoria")["ultimo_acesso"]
        .count()
        .sort_values(ascending=False)
        .reset_index(
            name="QTD_SALAS_SEM_ACESSO"
        )
    )


    # =========================================================
    # CARDS
    # =========================================================

    st.subheader("Visão geral")

    indicador1, indicador2, indicador3, indicador4 = st.columns(4)


    indicador1.metric(
        "📚 Total de disciplinas",
        f"{quantidadeRegistros:,}".replace(",", ".")
    )


    indicador2.metric(
        "👨‍🏫 Professores",
        f"{len(quantidadeProfessor):,}".replace(",", ".")
    )


    indicador3.metric(
        "⚠️ Disciplinas sem acesso",
        f"{len(quantidadeNuncaAcessou):,}".replace(",", ".")
    )


    indicador4.metric(
        "📉 Percentual sem acesso",
        f"{percentualSemAcesso:.2f}%"
    )


    st.divider()


    # =========================================================
    # GRÁFICOS
    # =========================================================

    st.subheader("Análise de acessos")


    # ---------------------------------------------------------
    # GRÁFICO POR PERÍODO
    # ---------------------------------------------------------

    graficoPeriodo = px.bar(

        periodoSemAcesso,

        x="categoria",

        y="QTD_SALAS_SEM_ACESSO",

        text="QTD_SALAS_SEM_ACESSO",

        title="Disciplinas sem acesso por período"
    )
    
    graficoPeriodo.update_xaxes(
        type="category"
    )


    graficoPeriodo.update_traces(

        marker_color="#006BB6",

        textposition="inside"
    )


    graficoPeriodo.update_layout(

        height=380,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis_title="Período",

        yaxis_title="Quantidade",

        showlegend=True
    )


    # ---------------------------------------------------------
    # TOP PROFESSORES
    # ---------------------------------------------------------

    topProfessores = (
        totalSemAcessoProfessor
        .head(10)
        .sort_values(
            "QTD_SALAS_SEM_ACESSO",
            ascending=True
        )
    )


    graficoProfessor = px.bar(

        topProfessores,

        x="QTD_SALAS_SEM_ACESSO",

        y="professor",

        orientation="h",

        text="QTD_SALAS_SEM_ACESSO",

        title="Top 10 professores com mais disciplinas sem acesso"
    )


    graficoProfessor.update_traces(

        marker_color="#61B5E8",

        textposition="outside"
    )


    graficoProfessor.update_layout(

        height=380,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis_title="Quantidade",

        yaxis_title="",

        showlegend=False
    )


    # =========================================================
    # EXIBIÇÃO DOS GRÁFICOS
    # =========================================================

    grafico1, grafico2 = st.columns(2)


    with grafico1:

        st.plotly_chart(

            graficoPeriodo,

            width='stretch',

            theme="streamlit"
        )


    with grafico2:

        st.plotly_chart(

            graficoProfessor,

            width='stretch',

            theme="streamlit"
        )


    st.divider()


    # =========================================================
    # CURSOS
    # =========================================================

    st.subheader("Disciplinas sem acesso por curso")


    graficoCurso = px.bar(

        totalSemAcessoCurso.head(15),

        x="categoria_curso",

        y="QTD_SALAS_SEM_ACESSO",

        text="QTD_SALAS_SEM_ACESSO",

        title="Cursos com maior quantidade de disciplinas sem acesso"
    )


    graficoCurso.update_traces(

        marker_color="#006BB6",

        textposition="inside"
    )


    graficoCurso.update_layout(

        height=500,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=80
        ),

        xaxis_title="",

        yaxis_title="Quantidade",

        showlegend=False
    )


    st.plotly_chart(

        graficoCurso,

        width='stretch',

        theme="streamlit"
    )


    st.divider()


    # =========================================================
    # DETALHAMENTO
    # =========================================================

    st.subheader("Detalhamento")

    tab1, tab2, tab3 = st.tabs([

        "👨‍🏫 Professores",

        "📅 Períodos",

        "🎓 Cursos"

    ])


    # ---------------------------------------------------------
    # PROFESSORES
    # ---------------------------------------------------------

    with tab1:

        st.caption(
            "Quantidade de disciplinas sem acesso "
            "associadas a cada professor."
        )

        st.dataframe(

            totalSemAcessoProfessor,

            width='stretch',

            hide_index=True,

            column_config={

                "professor":
                    "Professor",

                "QTD_SALAS_SEM_ACESSO":
                    st.column_config.NumberColumn(
                        "Disciplinas sem acesso",
                        format="%d"
                    )
            }
        )


    # ---------------------------------------------------------
    # PERÍODOS
    # ---------------------------------------------------------

    with tab2:

        st.caption(
            "Distribuição das disciplinas sem acesso "
            "por período letivo."
        )

        st.dataframe(

            periodoSemAcesso,

            width='stretch',

            hide_index=True,

            column_config={

                "categoria":
                    "Período",

                "QTD_SALAS_SEM_ACESSO":
                    st.column_config.NumberColumn(
                        "Disciplinas sem acesso",
                        format="%d"
                    )
            }
        )


    # ---------------------------------------------------------
    # CURSOS
    # ---------------------------------------------------------

    with tab3:

        st.caption(
            "Quantidade de disciplinas sem acesso "
            "por curso."
        )

        st.dataframe(

            totalSemAcessoCurso,

            width='stretch',

            hide_index=True,

            column_config={

                "categoria_curso":
                    "Curso",

                "QTD_SALAS_SEM_ACESSO":
                    st.column_config.NumberColumn(
                        "Disciplinas sem acesso",
                        format="%d"
                    )
            }
        )


    st.divider()


    # =========================================================
    # REGISTROS SEM ACESSO
    # =========================================================

    with st.expander(
        f"🔎 Visualizar registros sem acesso ({len(quantidadeNuncaAcessou)})"
    ):

        st.dataframe(

            quantidadeNuncaAcessou,

            width='stretch',

            hide_index=True,

            height=500
        )