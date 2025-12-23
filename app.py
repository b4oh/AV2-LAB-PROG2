import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import json
from datetime import datetime, date, time
import pandas as pd
from fpdf import FPDF
import io

# --- Configuração da Página ---
st.set_page_config(
    page_title="SUMESE - Sistema de Gestão",
    page_icon="👮",
    layout="wide"
)

# --- Conexão com Firebase (Admin SDK) ---
@st.cache_resource
def init_firebase():
    # Verifica se já foi inicializado
    if not firebase_admin._apps:
        # Tenta ler as credenciais dos secrets
        if "firebase" in st.secrets:
            # st.secrets retorna um objeto AttrDict, precisamos de um dict normal para o certificado
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        else:
            st.error("Erro: Credenciais do Firebase não encontradas em st.secrets.")
            return None
    else:
        return firestore.client()

# --- Autenticação (Client-side via REST API) ---
def login_user(email, password):
    if "firebase_web" not in st.secrets:
        st.error("Erro: Chave de API Web do Firebase não configurada em st.secrets.")
        return None

    api_key = st.secrets["firebase_web"]["api_key"]
    request_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(request_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Inicializa DB
try:
    db = init_firebase()
except Exception as e:
    st.error(f"Falha ao conectar ao banco de dados: {e}")
    db = None

# --- Estado da Sessão ---
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    if not st.session_state.user:
        render_login()
    else:
        render_app()

def render_login():
    st.title("🔐 SUMESE - Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")

            if submit:
                user_info = login_user(email, password)
                if user_info:
                    st.session_state.user = user_info
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Email ou senha incorretos.")

def render_app():
    st.sidebar.title(f"Olá, {st.session_state.user.get('email', 'Usuário')}")

    menu = st.sidebar.radio("Navegação", ["Novo Registro", "Dashboard"])

    if st.sidebar.button("Sair"):
        st.session_state.user = None
        st.rerun()

    st.title("Sistema SUMESE - Módulo Escolta")

    if menu == "Novo Registro":
        render_form()
    elif menu == "Dashboard":
        render_dashboard()

def render_form():
    st.subheader("📝 Novo Registro de Saída")

    with st.form("registro_escolta"):
        col1, col2 = st.columns(2)

        with col1:
            data_registro = st.date_input("Data do Registro", value=date.today())
            unidade_origem = st.selectbox("Unidade de Origem", ["UEC", "USIP", "CENAM", "Outra"])
            socioeducandos = st.text_area("Socioeducandos (Nomes)", help="Liste os nomes separados por vírgula ou quebra de linha")
            destino = st.text_input("Destino", placeholder="Ex: CRIE, Fórum, Hospital")

        with col2:
            finalidade = st.text_input("Finalidade")
            st.markdown("### Horários")
            hc1, hc2, hc3 = st.columns(3)
            hora_marcada = hc1.time_input("Hora Marcada")
            hora_saida_real = hc2.time_input("Saída Real")
            hora_chegada = hc3.time_input("Chegada (Previsão/Real)")

        st.markdown("### Equipe")
        ec1, ec2, ec3 = st.columns(3)
        motorista = ec1.text_input("Motorista")
        agentes_protecao = ec2.text_area("Agentes de Proteção")
        agentes_escolta = ec3.text_area("Agentes de Escolta")

        st.markdown("---")
        st.markdown("### Uso de Algemas")

        usou_algemas = st.checkbox("Houve uso de algemas?")
        justificativa_algemas = ""

        if usou_algemas:
            justificativa_algemas = st.selectbox(
                "Justificativa (Obrigatório)",
                ["Resistência", "Perigo de Fuga", "Perigo à Integridade Física"]
            )
            st.warning("⚠️ O uso de algemas requer justificativa conforme Súmula Vinculante nº 11 do STF.")

        # Nota de rodapé legal
        st.markdown("""
        <small style="color: grey;">
        *Súmula Vinculante nº 11 do STF*: Só é lícito o uso de algemas em casos de resistência e de fundado receio de fuga ou de perigo à integridade física própria ou alheia, por parte do preso ou de terceiros, justificada a excepcionalidade por escrito...
        </small>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button("Salvar Registro")

        if submitted:
            if usou_algemas and not justificativa_algemas:
                st.error("É obrigatório selecionar uma justificativa para o uso de algemas.")
            else:
                salvar_registro(
                    data_registro, unidade_origem, socioeducandos, destino, finalidade,
                    hora_marcada, hora_saida_real, hora_chegada,
                    motorista, agentes_protecao, agentes_escolta,
                    usou_algemas, justificativa_algemas
                )

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)

    # Cabeçalho
    pdf.cell(0, 10, "REGISTRO DE SAÍDA DE SOCIOEDUCANDO", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    # Campos
    def add_field(label, value):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(50, 10, f"{label}: ", border=0)
        pdf.set_font("Arial", '', 12)
        # Handle datetime objects
        val_str = str(value)
        if hasattr(value, 'strftime'):
            val_str = value.strftime("%d/%m/%Y") if isinstance(value, datetime) else value.strftime("%H:%M")

        pdf.multi_cell(0, 10, val_str)

    add_field("Data", data["data_registro"])
    add_field("Unidade de Origem", data["unidade_origem"])
    add_field("Socioeducandos", data["socioeducandos"])
    add_field("Destino", data["destino"])
    add_field("Finalidade", data["finalidade"])

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Horários", ln=True)
    add_field("Hora Marcada", data["horarios"]["hora_marcada"])
    add_field("Saída Real", data["horarios"]["hora_saida_real"])
    add_field("Previsão/Chegada", data["horarios"]["hora_chegada"])

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Equipe", ln=True)
    add_field("Motorista", data["equipe"]["motorista"])
    add_field("Agentes de Proteção", data["equipe"]["agentes_protecao"])
    add_field("Agentes de Escolta", data["equipe"]["agentes_escolta"])

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Uso de Algemas", ln=True)
    usou = "Sim" if data["uso_algemas"]["usou"] else "Não"
    add_field("Houve uso?", usou)
    if data["uso_algemas"]["usou"]:
        add_field("Justificativa", data["uso_algemas"]["justificativa"])

    # Espaço para assinaturas
    pdf.ln(20)
    pdf.line(20, pdf.get_y(), 90, pdf.get_y())
    pdf.line(110, pdf.get_y(), 190, pdf.get_y())

    y = pdf.get_y()
    pdf.text(20, y + 5, "Motorista")
    pdf.text(110, y + 5, "Agentes")

    pdf.ln(20)
    pdf.line(65, pdf.get_y(), 145, pdf.get_y())
    y = pdf.get_y()
    pdf.text(65, y + 5, "Coordenador / Responsável")

    # Rodapé Legal
    pdf.set_y(-40)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 4, "Súmula Vinculante nº 11 do STF: Só é lícito o uso de algemas em casos de resistência e de fundado receio de fuga ou de perigo à integridade física própria ou alheia, por parte do preso ou de terceiros, justificada a excepcionalidade por escrito...")

    return pdf.output(dest='S').encode('latin-1')

def salvar_registro(data, origem, socios, dest, fin, h_marc, h_sai, h_cheg, mot, ag_prot, ag_esc, alg_uso, alg_just):
    if db is None:
        st.error("Erro: Banco de dados não conectado.")
        return

    # Estrutura dos dados
    doc_data = {
        "data_registro": datetime.combine(data, datetime.min.time()),
        "unidade_origem": origem,
        "socioeducandos": socios,
        "destino": dest,
        "finalidade": fin,
        "horarios": {
            "hora_marcada": h_marc.strftime("%H:%M"),
            "hora_saida_real": h_sai.strftime("%H:%M"),
            "hora_chegada": h_cheg.strftime("%H:%M")
        },
        "equipe": {
            "motorista": mot,
            "agentes_protecao": ag_prot,
            "agentes_escolta": ag_esc
        },
        "uso_algemas": {
            "usou": alg_uso,
            "justificativa": alg_just if alg_uso else None
        },
        "created_at": firestore.SERVER_TIMESTAMP
    }

    try:
        db.collection("registros_escolta").add(doc_data)
        st.success("Registro salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

def render_dashboard():
    st.subheader("📊 Últimos Registros")

    if db is None:
        st.error("Banco de dados indisponível.")
        return

    try:
        docs = db.collection("registros_escolta").order_by("created_at", direction=firestore.Query.DESCENDING).limit(20).stream()

        # Store full objects for PDF generation
        full_records = []
        display_data = []

        for doc in docs:
            d = doc.to_dict()
            full_records.append(d)

            # Flatten para exibição na tabela
            row = {
                "Data": d.get("data_registro").strftime("%d/%m/%Y") if d.get("data_registro") else "",
                "Origem": d.get("unidade_origem"),
                "Destino": d.get("destino"),
                "Socioeducandos": d.get("socioeducandos"),
                "Motorista": d.get("equipe", {}).get("motorista"),
                "Algemas": "Sim" if d.get("uso_algemas", {}).get("usou") else "Não"
            }
            display_data.append(row)

        if display_data:
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True)

            # Select record to generate PDF
            st.subheader("🖨️ Gerar Guia de Saída")
            selected_idx = st.selectbox("Selecione um registro para imprimir:", range(len(display_data)), format_func=lambda x: f"{display_data[x]['Data']} - {display_data[x]['Socioeducandos']}")

            # Convert selected record to PDF
            if st.button("Preparar PDF"):
                record = full_records[selected_idx]
                pdf_bytes = generate_pdf(record)
                st.download_button(
                    label="📥 Baixar Guia de Saída",
                    data=pdf_bytes,
                    file_name=f"guia_saida_{display_data[selected_idx]['Data'].replace('/','-')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("Nenhum registro encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

if __name__ == "__main__":
    main()
