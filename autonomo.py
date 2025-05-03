import streamlit as st

def calcular_inss_autonomo(valor_servico, regime):
    teto_base = 8157.41
    teto_inss = teto_base * 0.20  # R$ 1.631,48

    if regime == "Completo":
        inss = valor_servico * 0.20
        if inss > teto_inss:
            inss = teto_inss
    elif regime == "Simplificado":
        inss = 1518.00 * 0.11  # R$ 166,98 fixos
    else:
        st.error("Regime inválido.")
        return 0.0

    return round(inss, 2)

def calcular_irrf(base_irrf):
    if base_irrf <= 2428.80:
        aliquota = 0.0
        deducao = 0.00
    elif base_irrf <= 2826.65:
        aliquota = 0.075
        deducao = 182.16
    elif base_irrf <= 3751.05:
        aliquota = 0.15
        deducao = 394.16
    elif base_irrf <= 4664.68:
        aliquota = 0.225
        deducao = 675.49
    else:
        aliquota = 0.275
        deducao = 908.73

    irrf = base_irrf * aliquota - deducao
    return round(max(irrf, 0), 2)

def calcular_iss(valor_servico, aliquota_iss):
    return round(valor_servico * (aliquota_iss / 100), 2)

def formatar(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

# Interface Streamlit
st.set_page_config(page_title="Simulador Autônomo (2025)")
st.title("Simulador Autônomo (2025)")

regime = st.selectbox("Escolha o regime de contribuição ao INSS:", ["Completo", "Simplificado"])
valor_servico = st.number_input("Informe o valor total do serviço (R$):", min_value=0.0, step=100.0, format="%.2f", placeholder="")
aliquota_iss = st.slider("Escolha a alíquota de ISS (%):", min_value=2.0, max_value=5.0, step=0.1)

# Estilização do botão azul
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0d6efd;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 6px;
        font-size: 16px;
    }
    div.stButton > button:first-child:hover {
        background-color: #0b5ed7;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("Calcular"):
    if valor_servico > 0:
        inss = calcular_inss_autonomo(valor_servico, regime)
        base_irrf = valor_servico - inss
        irrf = calcular_irrf(base_irrf)
        iss = calcular_iss(valor_servico, aliquota_iss)
        liquido = valor_servico - inss - irrf - iss

        st.subheader("Resumo do Cálculo:")
        st.write(f"Regime de Contribuição: {regime}")
        st.write(f"Valor Bruto do Serviço: {formatar(valor_servico)}")
        st.write(f"Desconto de INSS: {formatar(inss)}")
        st.write(f"Base de Cálculo do IRRF: {formatar(base_irrf)}")
        st.write(f"Desconto de IRRF: {formatar(irrf)}")
        st.write(f"Desconto de ISS ({aliquota_iss:.1f}%): {formatar(iss)}")
        st.success(f"Valor Líquido a Receber: {formatar(liquido)}")

        st.markdown(
            "<div style='text-align: justify; font-size: 0.9em;'>"
            "<strong>Cálculo atualizado em Maio/2025</strong> – Desenvolvido por Reginaldo Ramos | Explica no Quadro! "
            "Esta é uma ferramenta auxiliar para a atividade de planejamento fiscal e tributário. "
            "Sempre consultar a legislação aplicável para o cálculo e recolhimento dos tributos devidos."
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Por favor, informe um valor maior que zero.")
