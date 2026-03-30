import streamlit as st

st.title("Financial Health & Audit Readiness Tool")

st.header("Enter your business details")

revenue = st.number_input("Monthly Revenue (£)", min_value=0.0)
expenses = st.number_input("Monthly Expenses (£)", min_value=0.0)

if st.button("Calculate"):
    if revenue > 0:
        profit_margin = (revenue - expenses) / revenue * 100
        st.subheader("Results")
        st.write(f"Profit Margin: {profit_margin:.2f}%")
        
        if profit_margin > 20:
            st.success("Healthy business")
        elif profit_margin > 10:
            st.warning("Moderate risk")
        else:
            st.error("High risk")
    else:
        st.write("Please enter revenue")
