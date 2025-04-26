import streamlit as st

def calcular_inss(salario_bruto):
    faixas = [
        (1518.00, 0.075),
        (2793.88, 0.09),
        (4190.83, 0.12),
        (8157.41, 0.14)
    ]
    teto_inss = 951.63
    desconto = 0.0
    limites = [0] + [faixa[0] for faixa in faixas]

    for i in range(1, len(limites)):
        if salario_bruto > limites[i]:
            base_calculo = limites[i] - limites[i-1]
            desconto += base_calculo * faixas[i-1][1]
        else:
            base_calculo = salario_bruto - limites[i-1]
            desconto += base_calculo * faixas[i-1][1]
            break

    if salario_bruto > faixas[-1][0]:
        desconto = teto_inss

    return round(desconto, 2)

# --- Interface Streamlit ---
st.set_page_config(page_title="Simulador INSS 2025")

st.title("Simulador de Desconto INSS - 2025")

salario_texto = st.text_input("Digite o salário bruto (R$):")

if salario_texto:
    try:
        salario = float(salario_texto.replace(",", "."))
    except ValueError:
        salario = 0.0
        st.warning("Digite um valor numérico válido para o salário.")
else:
    salario = 0.0

if st.button("Calcular INSS"):
    if salario > 0:
        desconto_inss = calcular_inss(salario)
        salario_liquido = salario - desconto_inss

        st.success(f"Desconto de INSS: R$ {desconto_inss:.2f}")
        st.info(f"Valor Líquido (sem outros descontos): R$ {salario_liquido:.2f}")
    else:
        st.warning("Por favor, insira um salário válido acima de R$ 0,00.")
