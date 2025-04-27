import streamlit as st

def calcular_inss(salario_bruto):
    """
    Função para calcular o desconto de INSS com base na tabela de 2025.
    """
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

def calcular_irrf(base_irrf):
    """
    Função para calcular o desconto de IRRF com base na tabela de 2025.
    """
    if base_irrf <= 2428.80:
        aliquota = 0
        parcela_deduzir = 0
    elif base_irrf <= 2826.65:
        aliquota = 0.075
        parcela_deduzir = 182.16
    elif base_irrf <= 3751.05:
        aliquota = 0.15
        parcela_deduzir = 394.16
    elif base_irrf <= 4664.68:
        aliquota = 0.225
        parcela_deduzir = 675.49
    else:
        aliquota = 0.275
        parcela_deduzir = 908.73

    irrf_bruto = base_irrf * aliquota
    irrf = irrf_bruto - parcela_deduzir

    if irrf < 0:
        irrf = 0.0

    return round(irrf, 2)

def formatar_valor(valor):
    """
    Formata o número para o padrão brasileiro: milhar com ponto e decimal com vírgula.
    """
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

# --- Interface Streamlit ---
st.set_page_config(page_title="Simulador INSS + IRRF 2025")

st.title("Simulador de Desconto INSS + IRRF - 2025")

salario_texto = st.text_input("Digite o salário bruto (R$):")

if salario_texto:
    try:
        salario_bruto = float(salario_texto.replace(",", "."))
    except ValueError:
        salario_bruto = 0.0
        st.warning("Digite um valor numérico válido para o salário.")
else:
    salario_bruto = 0.0

if st.button("Calcular"):
    if salario_bruto > 0:
        desconto_inss = calcular_inss(salario_bruto)

        # Aplica a regra especial para a base de cálculo do IRRF
        valor_minimo_inss_para_irrf = 607.20

        if desconto_inss < valor_minimo_inss_para_irrf:
            base_irrf = salario_bruto - valor_minimo_inss_para_irrf
        else:
            base_irrf = salario_bruto - desconto_inss

        desconto_irrf = calcular_irrf(base_irrf)
        salario_liquido = salario_bruto - desconto_inss - desconto_irrf

        st.subheader("Resultado:")
        st.write(f"Salário Bruto: {formatar_valor(salario_bruto)}")
        st.write(f"Desconto de INSS: {formatar_valor(desconto_inss)}")
        st.write(f"Base de Cálculo IRRF: {formatar_valor(base_irrf)}")
        st.write(f"Desconto de IRRF: {formatar_valor(desconto_irrf)}")
        st.success(f"Salário Líquido: {formatar_valor(salario_liquido)}")
    else:
        st.warning("Por favor, insira um salário válido acima de R$ 0,00.")
