import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Formulário Operacional", layout="centered")

# ---------- MODELOS E VARIÁVEIS ESPECÍFICAS ---------- #
modelos = {
    "AMRJ": ["CAIS", "SEÇÃO", "POB", "ETA", "CALADO", "TEMPO DE PORTO", "ATRACAÇÃO", "ATIVIDADES"],
    "BACS": ["CAIS", "CABEÇOS", "POB", "ETA", "CALADO", "TEMPO DE PORTO", "ATRACAÇÃO", "ATIVIDADES"],
    "BNRJ": ["PIER", "BERÇO", "POB", "ETA", "CALADO", "TEMPO DE PORTO", "ATRACAÇÃO", "ATIVIDADES"],
    "Cais Comercial": ["ÁREA DE OPERAÇÃO (ARMAZEM/PÁTIO)", "CABEÇOS", "POB", "ETA", "CALADO", "TEMPO DE PORTO", "ATRACAÇÃO", "ATIVIDADES"],
    "FUNDEIO": ["ETA", "CALADO", "ATIVIDADES"],
    "T.MULT": ["CABEÇOS", "POB", "ETA", "CALADO", "TEMPO DE PORTO", "ATRACAÇÃO", "ATIVIDADES"],
    "TECON": ["PÁTIO", "CABEÇOS", "POB", "ETA", "CALADO", "TEMPO DE PORTO", "ATRACAÇÃO", "ATIVIDADES"]
}

mensagens_finais = {
    "AMRJ": "Desejando boas-vindas ao Arsenal da marinha, AMRJ.",
    "BACS": "Desejando boas-vindas a BACS.",
    "BNRJ": "Desejando boas-vindas a BNRJ.",
    "Cais Comercial": "Desejando boas-vindas ao Porto do Rio de Janeiro.",
    "FUNDEIO": "Desejando boas-vindas ao TECON no Porto do Rio de Janeiro.",
    "T.MULT": "Desejando boas-vindas ao Porto do Açu.",
    "TECON": "Desejando boas-vindas ao TECON no Porto do Rio de Janeiro."
}

DIAS_SEMANA_PT = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

local_atracacao = {
    "AMRJ": "AMRJ-(Arsenal de Marinha)",
    "BACS": "Porto de Niteroi - BACS",
    "BNRJ": "Porto de Niteroi - BNRJ",
    "Cais Comercial": "Porto do Rio de Janeiro - Cais Comercial",
    "FUNDEIO": "Porto do Rio de Janeiro - FUNDEIO",
    "T.MULT": "Porto do Açu, T-MULT",
    "TECON": "Porto do Rio de Janeiro - TECON"
}
equipamentos_disponiveis = {
    "Yokohamas": ["Empresa Fornecedora", "OBS"],
    "Guindaste": ["Capacidade", "Empresa Fornecedora", "OBS"],
    "Cerco Preventivo": ["Empresa Fornecedora", "OBS"],
    "Empilhadeira": ["Capacidade", "Empresa Fornecedora", "OBS"],
}

st.title("📋 Formulário de Planejamento Operacional")
modelo = st.selectbox("Selecione o modelo da operação:", list(modelos.keys()))
st.divider()

st.subheader("1. 🚢 Informações Iniciais")
roa = st.text_input("Número do ROA")
navio = st.text_input("Nome da embarcação")
data = st.date_input("Data da operação", format="DD/MM/YYYY")
dia_semana = DIAS_SEMANA_PT[data.strftime("%A")]
st.markdown(f"**Dia da semana:** {dia_semana}")

valores_modelo = {}
for campo in modelos[modelo]:
    if "ARMAZEM" in campo.upper() or "ÁREA DE OPERAÇÃO" in campo.upper():
        tipo_area = st.radio("Área de operação:", ["Armazém", "Pátio"])
        numero_area = st.text_input(f"{tipo_area.upper()}")
        valores_modelo["ÁREA DE OPERAÇÃO"] = f"{numero_area}"
    else:
        valores_modelo[campo] = st.text_input(campo)

st.divider()
st.subheader("2. 👷 Equipe da Operação")
turno_dia = st.checkbox("Incluir equipe do turno do dia/tarde")
turno_noite = st.checkbox("Incluir equipe do turno da noite")
equipe = {}

if turno_dia:
    st.markdown("### ☀️ Turno do Dia/Tarde")
    num_total_dia = st.number_input("Quantidade total da equipe (incluindo supervisor) - Turno Dia", min_value=1, step=1, key="dia")
    supervisor_dia = st.text_input("Supervisor (Turno Dia)")
    equipe_dia = [st.text_input(f"Integrante {i+1} (Turno Dia)", key=f"int_dia_{i}") for i in range(num_total_dia - 1)]
    equipe["dia"] = {"supervisor": supervisor_dia, "integrantes": equipe_dia}
    horario_saida = st.text_input("Horário de saída da base")

if turno_noite:
    st.markdown("### 🌙 Turno da Noite")
    num_total_noite = st.number_input("Quantidade total da equipe (incluindo supervisor) - Turno Noite", min_value=1, step=1, key="noite")
    supervisor_noite = st.text_input("Supervisor (Turno Noite)")
    equipe_noite = [st.text_input(f"Integrante {i+1} (Turno Noite)", key=f"int_noite_{i}") for i in range(num_total_noite - 1)]
    equipe["noite"] = {"supervisor": supervisor_noite, "integrantes": equipe_noite}
    if turno_dia:
        horario_rendicao = st.text_input("Horário de rendição")
    else:
        horario_saida = st.text_input("Horário de saída da base")

st.divider()
st.subheader("3. 🚜 Equipamentos da Operação")
if "equipamentos_usados" not in st.session_state:
    st.session_state.equipamentos_usados = []

equipamento_adicionar = st.selectbox("Selecione o equipamento para adicionar:", list(equipamentos_disponiveis.keys()))
if st.button("Adicionar equipamento"):
    st.session_state.equipamentos_usados.append({"tipo": equipamento_adicionar, "dados": {}})

remover_idx = None
for idx, item in enumerate(st.session_state.equipamentos_usados, start=1):
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"#### Equipamento N°{idx}: {item['tipo']}")
        dados = {}
        for campo in equipamentos_disponiveis[item["tipo"]]:
            if campo == "OBS":
                qtd_obs = st.number_input(
                    f"Quantidade de OBS ({item['tipo']} #{idx})",
                    min_value=1, max_value=3, value=1,
                    key=f"obs_qtd_{idx}"
                )
                for i in range(qtd_obs):
                    chave_obs = "OBS" if i == 0 else f"OBS{i + 1}"
                    dados[chave_obs] = st.text_input(
                        f"{chave_obs} ({item['tipo']} #{idx})",
                        key=f"{item['tipo']}_{chave_obs}_{idx}"
                    )
            else:
                dados[campo] = st.text_input(
                    f"{campo} ({item['tipo']} #{idx})",
                    key=f"{item['tipo']}_{campo}_{idx}"
                )

        item["dados"] = dados
    with col2:
        if st.button("Remover", key=f"remove_{idx}"):
            remover_idx = idx - 1

if remover_idx is not None:
    st.session_state.equipamentos_usados.pop(remover_idx)
    st.rerun()

# ---------- TEXTO FINAL ---------- #


# Campo para o link do Marine Traffic
st.divider()
st.subheader("4. Marine Traffic")
link_marine = st.text_input("Link do Marine Traffic da embarcação")

# Botão para gerar o formulário
if st.button("📄 Gerar Formulário"):
    formulario = f"""
*FORMULÁRIO DE PLANEJAMENTO OPERACIONAL – ROA {roa}*

*Navio:* {navio}
*Data:* {data.strftime('%d/%m/%Y')} - {dia_semana}
*Local da atracação:* {local_atracacao[modelo]}
"""

    for campo in modelos[modelo]:
        if campo == "ÁREA DE OPERAÇÃO (ARMAZEM/PÁTIO)":
            formulario += f"*{tipo_area.upper()}:* {valores_modelo['ÁREA DE OPERAÇÃO']}\n"
        else:
            formulario += f"*{campo}:* {valores_modelo[campo]}\n"

    if turno_dia:
        formulario += "\n*Equipe:*\nTurno do dia/tarde:\nSupervisor:\n-@{}\n".format(equipe["dia"]["supervisor"])
        if len(equipe["dia"]["integrantes"]) > 0:
            formulario += "Equipe Operacional:\n"
        for integrante in equipe["dia"]["integrantes"]:
            formulario += f"-@{integrante}\n"
        formulario += f"\nHorário de saída da base: {horario_saida}\n"

    if turno_noite:
        formulario += "\n*Turno da Noite:*\nSupervisor:\n-@{}\n".format(equipe["noite"]["supervisor"])
        if len(equipe["noite"]["integrantes"]) > 0:
            formulario += "Equipe Operacional:\n"
        for integrante in equipe["noite"]["integrantes"]:
            formulario += f"-@{integrante}\n"
        if turno_dia:
            formulario += f"\nHorário de Rendição: {horario_rendicao}\n"

    formulario += "\n*Equipamentos e serviços:*\n"
    for idx, item in enumerate(st.session_state.equipamentos_usados, start=1):
        formulario += f"\nEquipamento N°{idx}:\nNome do equipamento: {item['tipo']}\n"
        for campo, valor in item["dados"].items():
            formulario += f"{campo}: {valor}\n"

    formulario += """

EM CASO DE SUBCONTRATAÇÃO SEMPRE REGISTRAR O HORÁRIO DE ENTRADA E SAÍDA DO EQUIPAMENTO. 

*Canal de Comunicação (Rádio):*
Canal de comunicação para operação: 72/74
Canal de comunicação para amarradores: 10/13

*Checklist pré-operação:*
-Verificar se o Cais está livre;
-Confirmar disponibilidade dos Cabeços;
-Confirmar o estado das Defensas. 
-Confirmar o estado dos equipamentos tanto de içamento quanto sublocados; 

*Procedimento operacional:*
-Registrar com foto o estado do cais, defensas e cabeços e divulgar no grupo do ROA e do Cliente;              
-Segregar área da escada com cones;                              
-Registrar com foto a área da escada com cones;                   
-Realizar o preenchimento do DDS;                                 
-Registrar com foto o estado dos equipamentos sublocados;    
-Registrar com foto a quantidade em m³ do abastecimento de água no local  
"""

    if any(eq['tipo'] == 'Guindaste' for eq in st.session_state.equipamentos_usados):
        formulario += "-Levar o cabo extensor do Guindaste.\n-Verificar o local de patolamento para o guindaste evitando patolar próximo de cabos.\n"

    if link_marine:
        formulario += f"-Acompanhar a chegada do navio via Marine Traffic: {link_marine}"


    formulario += f"\nSempre fazer contato pelo rádio com o comandante se apresentando, deixando o contato e {mensagens_finais[modelo]}"
    st.download_button(
        label="📥 Exportar como .txt",
        data=formulario.strip(),
        file_name=f"ROA{roa}_{modelo}_{navio}.txt",
        mime="text/plain"
    )

    st.text_area("📄 Texto final do formulário:", value=formulario.strip(), height=700)



