import streamlit as st
import pandas as pd
# Sidebar
with st.sidebar:
    st.title("VLSI Logic Analyzer")

    st.markdown("""
    ### About
    A Python-based mini EDA tool for
    analyzing Boolean logic circuits.

    ### Features
    - Boolean expression analysis
    - Truth table generation
    - Logic depth estimation
    - Propagation delay estimation
    - Automatic circuit visualization

    ### Supported Logic
    - AND
    - OR
    - NOT

    ### Boolean Notation
    `.` → AND  
    `+` → OR  
    `'` → NOT
    """)
from logicanalyzer import (
    find_variables,
    generate_truth_table,
    calculate_logic_depth,
    estimate_delay,
    validate_expression,
    count_gates
)
from circuitvisualizer import draw_circuit

# Page Title
st.title("VLSI Logic Circuit Analyzer")

st.write("Enter a Boolean expression and the tool will analyze"
         "the logic gates used in the circuit"
)

# Input section
st.subheader("Boolean Expression")

st.markdown("### Enter Boolean Expression")

st.caption(
    "Supported formats: A AND B, A OR B, NOT A, A.B, A+B, A'"
)

st.info(
    "Example: A.B + C'  →  AND, OR and NOT logic"
)
expression = st.text_input(
    "Enter Boolean Expression:",
    "(A AND B)"
)
#Analyze button
if st.button("Analyze"):

    valid, message = validate_expression(expression)

    if not valid:
        st.error(message)

    else:
        variables, rows = generate_truth_table(expression)

        st.subheader("Circuit Information")

        depth = calculate_logic_depth(expression)
        delay = estimate_delay(expression)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Inputs", len(variables))

        with col2:
            st.metric("Logic Depth", depth)

        with col3:
            st.metric("Estimated Delay", f"{delay} ns")
        with col4:
            st.metric("Logic Gates", count_gates(expression))


        st.write(f"**Input Variables:** {', '.join(variables)}")

        st.subheader("Truth Table")

        df = pd.DataFrame(rows)

        st.dataframe(df, width="stretch")

        st.subheader("Circuit Diagram")

        try:
            figure = draw_circuit(expression)
            st.pyplot(figure)

        except Exception:
            st.error("Unable to generate the circuit diagram.")
else:
    st.warning("please enter a boolean expression")
