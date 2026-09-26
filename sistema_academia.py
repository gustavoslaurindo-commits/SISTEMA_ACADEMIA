import streamlit as st
from banco import criar_tabela, inserir_checkin, listar_checkins, excluir_checkin

st.set_page_config(
    page_title="Sistema de Cadastro de Academia",
    layout="wide"
)

st.title("Sistema de Cadastro de Academia")

criar_tabela()

st.subheader("Cadastrar novo check-in")

with st.form("form_cadastro", clear_on_submit=True):
    col_a, col_b = st.columns(2)

    with col_a:
        aluno = st.text_input("Aluno:")
        modalidade = st.selectbox(
            "Modalidade:",
            ["Musculação", "Crossfit", "Pilates", "Natação", "Luta Livre"]
        )
        instrutor = st.text_input("Instrutor:")

    with col_b:
        valor_mensalidade = st.number_input(
            "Valor da mensalidade (R$):",
            min_value=0.0,
            step=10.0
        )
        data_checkin = st.date_input("Data do check-in:")

    enviado = st.form_submit_button("Salvar check-in")

    if enviado:
        if aluno.strip() == "" or instrutor.strip() == "":
            st.error("Preencha o aluno e o instrutor antes de salvar.")
            # Exibe uma mensagem de erro para o usuário.
        else:
            # Se aluno e instrutor estiverem preenchidos,
            # executa o cadastro.
            inserir_checkin(
                aluno,
                modalidade,
                instrutor,
                valor_mensalidade,
                str(data_checkin)
            )
            st.success(f"Check-in de {aluno} cadastrado com sucesso!")
            st.rerun()

st.divider()

st.subheader("Análise automática")

df = listar_checkins()

if len(df) == 0:
    st.info(
        "Nenhum check-in cadastrado ainda. "
        "Use o formulário acima para começar."
    )
else:
    st.write("Filtros:")
    filtro_col1, filtro_col2 = st.columns(2)
    
    with filtro_col1:
        # Opção "Todas" adicionada para não filtrar nenhuma modalidade específica.
        filtro_modalidade = st.selectbox(
            "Filtrar por Modalidade:",
            ["Todas", "Musculação", "Crossfit", "Pilates", "Natação", "Luta Livre"]
        )
        
    with filtro_col2:
        maior_valor = float(df["valor_mensalidade"].max())
        if maior_valor == 0.0:
            maior_valor = 100.0 # Previne erro no slider se o banco estiver com valor zero.
            
        # Slider para selecionar o valor máximo da mensalidade.
        filtro_valor = st.slider(
            "Valor máximo da mensalidade (R$):",
            min_value=0.0,
            max_value=maior_valor,
            value=maior_valor
        )
        
    # Atualiza o dataframe com base nos filtros selecionados.
    df_filtrado = df
    if filtro_modalidade != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidade"] == filtro_modalidade]
        
    df_filtrado = df_filtrado[df_filtrado["valor_mensalidade"] <= filtro_valor]

    if len(df_filtrado) == 0:
        st.warning("Nenhum registro encontrado com esses filtros.")
    else:
        col1, col2, col3 = st.columns(3)
        
        # Cálculo das métricas principais.
        faturamento_total = df_filtrado["valor_mensalidade"].sum()
        ticket_medio = df_filtrado["valor_mensalidade"].mean()
        total_checkins = len(df_filtrado)

        col1.metric(
            "Receita total",
            f"R$ {faturamento_total:.2f}"
        )
        col2.metric(
            "Ticket médio",
            f"R$ {ticket_medio:.2f}"
        )
        col3.metric(
            "Check-ins cadastrados",
            total_checkins
        )

        grafico_modalidade, grafico_instrutor = st.columns(2)

        with grafico_modalidade:
            st.write("**Total por modalidade**")
            # Agrupa os valores por modalidade e exibe no gráfico de barras.
            total_por_modalidade = df_filtrado.groupby("modalidade")["valor_mensalidade"].sum()
            st.bar_chart(total_por_modalidade)

        with grafico_instrutor:
            st.write("**Total por instrutor**")
            # Agrupa os valores por instrutor e exibe no gráfico de barras.
            total_por_instrutor = df_filtrado.groupby("instrutor")["valor_mensalidade"].sum()
            st.bar_chart(total_por_instrutor)

        st.subheader("Todos os check-ins cadastrados")
        st.dataframe(df_filtrado, use_container_width=True)

    with st.expander("Excluir um check-in"):
        id_para_excluir = st.number_input(
            "ID do check-in a excluir:",
            min_value=0,
            step=1
        )

        if st.button("Excluir"):
            excluir_checkin(id_para_excluir)
            st.success(f"Check-in com id {id_para_excluir} excluído.")
            st.rerun()


            