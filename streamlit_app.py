import streamlit as st
from attacks import generate_attack_payload, analyze_response_with_ollama

def get_available_attacks():
    return [
        'prompt_injection',
        'data_extraction',
        'model_behavior_manipulation',
        'output_manipulation',
        'denial_of_service'
    ]

def main():
    st.title("LLM Vulnerability Fuzzer - Manual Mode")

    # Attack selection
    attacks = get_available_attacks()
    selected_attack = st.selectbox("Choose an attack", attacks)

    # Step 1: Generate Payload
    if st.button("1. Generate Payload"):
        payload = generate_attack_payload(selected_attack)
        st.session_state['payload'] = payload
        st.subheader("Generated Payload:")
        st.text_area("Copy this payload and use it with your target LLM", payload, height=150)

    # Step 2: Input for LLM Response
    st.subheader("2. LLM Response")
    llm_response = st.text_area("Paste the target LLM's response here", height=200)

    # Step 3: Analyze Response
    if st.button("3. Analyze Response"):
        if llm_response:
            with st.spinner("Analyzing response..."):
                analysis_result = analyze_response_with_ollama(selected_attack, llm_response)
                
                st.subheader("Analysis Result:")
                st.text_area("Detailed Analysis", analysis_result['analysis'], height=200)
                
                st.metric("Vulnerability Score", analysis_result['vulnerability_score'])
                
                if analysis_result['vulnerability_detected']:
                    st.warning("Potential vulnerability detected!")
                else:
                    st.success("No obvious vulnerabilities detected.")
                
                st.subheader("Exploit Suggestions:")
                for suggestion in analysis_result['exploit_suggestions']:
                    st.write(f"- {suggestion}")
                
                st.subheader("Defense Analysis:")
                st.write(analysis_result['defense_analysis'])
                
                st.subheader("Recommended Next Steps:")
                for step in analysis_result['next_steps']:
                    st.write(f"- {step}")
        else:
            st.error("Please paste the LLM's response before analyzing.")

if __name__ == "__main__":
    main()