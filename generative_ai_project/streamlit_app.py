import streamlit as st
import requests

# Django server details
DJANGO_SERVER = "http://127.0.0.1:8000/"  # Update with your Django server URL

# Endpoint to trigger code generation and evaluation
GENERATE_AND_EVALUATE_ENDPOINT = f"{DJANGO_SERVER}/generate_and_evaluate"

def trigger_generation_and_evaluation():
    try:
        response = requests.post(GENERATE_AND_EVALUATE_ENDPOINT)
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the Django server: {e}")
        return None

def display_evaluation_results(results):
    if results:
        st.subheader("Evaluation Results:")
        st.write(results)
    else:
        st.warning("Error fetching evaluation results.")

def main():
    st.title("AI Code Generator Evaluation")

    # Description and main goal of the project
    st.markdown(
        """
        This Streamlit app is designed to evaluate an AI code generator. The main goals of the project include:
        
        - Generating code solutions for specific programming exercises.
        - Evaluating the correctness, efficiency, and adherence to best practices of the generated code.
        """
    )

    # Trigger generation and evaluation
    if st.button("Generate and Evaluate"):
        st.info("Generating and evaluating solutions. Please wait...")
        evaluation_results = trigger_generation_and_evaluation()
        display_evaluation_results(evaluation_results)

if __name__ == "__main__":
    main()
