from transformers import pipeline

def generate_solution(prompt, model='microsoft/CodeGPT-small-py'):
    generator = pipeline('text-generation', model=model)
    generated_code = generator(prompt, max_length=50)[0]['generated_text']
    return generated_code
