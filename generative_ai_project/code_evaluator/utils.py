from transformers import pipeline

def generate_solution(prompt, model='microsoft/CodeGPT-small-py'):
    # Enhance the prompt for clarity
    refined_prompt = "Python code to: " + prompt

    # Initialize the model generator
    generator = pipeline('text-generation', model=model)

    # Adjust generation parameters
    # Increase max_length for potentially longer solutions
    # Set temperature to control randomness
    generated_code = generator(refined_prompt, temperature=0.7, top_k=50, truncation=True)[0]['generated_text']

    # Post-process the output to refine the generated code
    cleaned_code = post_process_generated_code(generated_code)

    return cleaned_code

def post_process_generated_code(code):
    # Remove repeated phrases
    lines = code.split('\n')
    unique_lines = list(set(lines))
    processed_code = '\n'.join(unique_lines)

    # Trim excess content (keeping a certain number of lines)
    max_lines = 10  # Adjust this based on your needs
    processed_code = '\n'.join(processed_code.split('\n')[:max_lines])

    return processed_code.strip()


def evaluate_solution(generated_code, expected_code):
    return {'match': generated_code.strip() == expected_code.strip()}
