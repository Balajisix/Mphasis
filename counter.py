import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = None

st.title("Counter App - Creating a Session")

start_ip = st.number_input("Enter start number", value=1, step=1)

if st.button("Increase"):
    if st.session_state.counter is None:
        st.session_state.counter = int(start_ip)
    else:
        st.session_state.counter += 1
    st.success(f"Increasing {st.session_state.counter}")

if st.button("Reset"):
    st.session_state.counter = None