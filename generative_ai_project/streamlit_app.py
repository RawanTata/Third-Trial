import streamlit as st
import requests
import pandas as pd

# Django server details
DJANGO_SERVER = "http://127.0.0.1:8000/"  # Update with your Django server URL

# Endpoint to trigger code generation and evaluation
GENERATE_AND_EVALUATE_ENDPOINT = f"{DJANGO_SERVER}/generate_and_evaluate"

def trigger_generation_and_evaluation():
    try:
        response = requests.post(GENERATE_AND_EVALUATE_ENDPOINT)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the Django server: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error: {e}")
        return None

def display_evaluation_results(results):
    if results:
        st.subheader("Evaluation Results:")
        for exercise_id, metrics in results.items():
            st.write(f"### Exercise ID: {exercise_id}")

            # Extract and display matrix data if available in evaluation metrics
            # matrix_data = metrics.get('matrix_data')
            # if matrix_data is not None:
            #     st.write("#### Matrix Data:")
            #     st.write(matrix_data)
            # else:
            #     st.warning("Matrix data not available for this exercise.")

            # Display other metrics
            df = pd.DataFrame({
                'Metric': ['Correctness', 'Efficiency', 'Best Practices'],
                'Value': [metrics.get('correctness', 'N/A'),
                          metrics.get('efficiency', 'N/A'),
                          metrics.get('best_practices', 'N/A')]
            })
            st.table(df)

            # Visualization (if metrics are numerical)
            # Modify this part as needed based on your metric types
            if all(isinstance(metrics[key], bool) for key in metrics):
                st.bar_chart(df.set_index('Metric'))

    else:
        st.warning("Error fetching evaluation results.")


def main():
    st.title("AI Code Generator Evaluation")

    # Project Description
    st.markdown(
        """
        **Project Goal: Code Generation using Generative AI**

        Large language models, like the GPT4 behind ChatGPT, are increasingly used for code generation. 
        The goal of this project is to build a database and a test environment to assess the capabilities of language models.

        **Technologies:**
        
        Examples of code-generating models:
        - [StarCoder](https://huggingface.co/blog/starcoder)
        - [Microsoft Phi-1](https://huggingface.co/microsoft/phi-1)

        **Result:**
        
        For this purpose, typical exercises in Python or Javascript will be recorded in a database. 
        The project aims to test different language models on these tasks effectively and evaluate the results, which will be presented in information graphics.
        """
    )

    # Trigger generation and evaluation
    if st.button("Generate and Evaluate"):
        st.info("Generating and evaluating solutions. Please wait...")
        evaluation_results = trigger_generation_and_evaluation()
        if evaluation_results:
            st.success("Generation and evaluation successful!")
            display_evaluation_results(evaluation_results)
        else:
            st.warning("Error during generation and evaluation. Please check the server logs.")

if __name__ == "__main__":
    main()
