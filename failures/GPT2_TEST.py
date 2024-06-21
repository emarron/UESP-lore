import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the fine-tuned model and tokenizer
model_name = "trained_model"  # The directory where the model is saved
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Ensure the pad token is set
tokenizer.pad_token = tokenizer.eos_token

# Function to generate a response from the model
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=512,
        do_sample=True,
        top_p=0.95,
        top_k=60,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Chat with the model
print("Chat with the fine-tuned GPT-2 model. Type 'exit' to stop.")
while True:
    prompt = input("You: ")
    if prompt.lower() == 'exit':
        break
    response = generate_response(prompt)
    print(f"Model: {response}")
