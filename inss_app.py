import streamlit as st

st.title("Simulador de Cálculo do INSS 2025")

salario = st.number_input("Informe o salário bruto (R$):", min_value=0.0, step=10.0, format="%.2f")

if salario:
    if salario <= 1518.00:
        inss = salario * 0.075
    elif salario <= 2793.88:
        inss = (1518 * 0.075) + (salario - 1518) * 0.09
    elif salario <= 4190.83:
        inss = (1518 * 0.075) + (1275.88 * 0.09) + (salario - 2793.88) * 0.12
    else:
        teto = 8157.41
        faixa4 = min(salario, teto) - 4190.83
        inss = (1518 * 0.075) + (1275.88 * 0.09) + (1396.95 * 0.12) + (faixa4 * 0.14)
        if salario > teto:
            st.warning("Salário excede o teto da contribuição. Cálculo limitado até R$ 8.157,41.")

    st.success(f"Desconto estimado do INSS: R$ {inss:,.2f}")
