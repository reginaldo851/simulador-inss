import streamlit as st

def calcular_inss_prolabore(valor):
    teto = 8157.41  # Novo teto do INSS
    base = min(valor, teto)
    return round(base * 0.11, 2)

def calcular_irrf(base_irrf):
    if base_irrf <= 2428.80:
        aliquota = 0
        deducao = 0
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

def formatar(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.set_page_config(page_title="Simulador de Pró-Labore dos Sócios")

st.title("Simulador de Pró-Labore dos Sócios - INSS + IRRF (2025)")

valor_texto = st.text_input("Informe o valor bruto do pró-labore (R$):")

if valor_texto:
    try:
        valor_bruto = float(valor_texto.replace(",", "."))
    except ValueError:
        valor_bruto = 0.0
        st.warning("Digite um valor numérico válido.")
else:
    valor_bruto = 0.0

if st.button("Calcular"):
    if valor_bruto > 0:
        inss = calcular_inss_prolabore(valor_bruto)
        base_irrf = valor_bruto - inss
        irrf = calcular_irrf(base_irrf)
        liquido = valor_bruto - inss - irrf

        st.subheader("Resultado:")
        st.write(f"Pró-Labore Bruto: {formatar(valor_bruto)}")
        st.write(f"Desconto de INSS (11%): {formatar(inss)}")
        st.write(f"Base de Cálculo IRRF: {formatar(base_irrf)}")
        st.write(f"Desconto de IRRF: {formatar(irrf)}")
        st.success(f"Pró-Labore Líquido: {formatar(liquido)}")

        st.caption("**Maio/2025** - Desenvolvido por Reginaldo Ramos | Explica no Quadro! Esta é uma ferramenta auxiliar para a atividade de planejamento fiscal e tributário. Sempre consultar a legislação aplicável para o cálculo e recolhimento dos tributos devidos pela empresa.")
    else:
        st.warning("Por favor, insira um valor maior que zero.")
