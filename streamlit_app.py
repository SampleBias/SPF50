import streamlit as st
import sys
import os

# Add the parent directory to sys.path to allow importing from ATLAS_H
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ATLAS_H.attacks import attack_loader, attack_registry, attacks
from ATLAS_H.attacks import app_config, client_config
from ATLAS_H.attacks import fuzzer_execution
from ATLAS_H.attacks import chat_clients, interactive_chat
from ATLAS_H.attacks import text_utils, results_table

st.set_page_config(page_title="ATLAS_H Attack Interface", layout="wide")

st.title("ATLAS_H Attack Interface")

# Load configurations
app_conf = app_config.load_config()
client_conf = client_config.load_config()

# Sidebar for attack selection
st.sidebar.header("Attack Selection")
available_attacks = attack_registry.get_available_attacks()
selected_attack = st.sidebar.selectbox("Select an attack", available_attacks)

# Main area for attack execution and results
col1, col2 = st.columns(2)

with col1:
    st.header("Attack Execution")
    if st.button("Execute Attack"):
        with st.spinner("Executing attack..."):
            attack = attack_loader.load_attack(selected_attack)
            results = attacks.execute_attack(attack)
            st.session_state.results = results
        st.success("Attack executed successfully!")

    # Fuzzer integration
    st.subheader("Fuzzer")
    if st.checkbox("Enable Fuzzing"):
        fuzzer_params = st.text_input("Fuzzer Parameters")
        if st.button("Run Fuzzer"):
            with st.spinner("Running fuzzer..."):
                fuzzer_results = fuzzer_execution.run_fuzzer(fuzzer_params)
            st.write(fuzzer_results)

with col2:
    st.header("Results")
    if 'results' in st.session_state:
        st.table(results_table.create_table(st.session_state.results))
    else:
        st.info("No results to display. Execute an attack first.")

# Interactive chat interface
st.header("Interactive Chat")
chat_client = chat_clients.get_client(client_conf)
chat_interface = interactive_chat.ChatInterface(chat_client)

user_input = st.text_input("Your message")
if st.button("Send"):
    with st.spinner("Processing..."):
        response = chat_interface.send_message(user_input)
    st.write("Response:", response)

# Text utils demonstration
st.header("Text Utilities")
sample_text = st.text_area("Enter text for processing")
if st.button("Process Text"):
    processed_text = text_utils.process_text(sample_text)
    st.write("Processed Text:", processed_text)

# Footer
st.markdown("---")
st.caption("ATLAS_H Attack Interface - Use responsibly")