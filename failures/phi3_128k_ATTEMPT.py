import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training

# Load tokenizer and model with trust_remote_code=True
model_name = "microsoft/Phi-3-vision-128k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Set pad token to eos token if not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

tokenizer.padding_side = "right"

# Load and prepare the dataset
dataset = load_dataset('json', data_files='chunked_dataset.jsonl')

# Tokenize dataset
def preprocess_function(examples):
    inputs = examples["prompt"]
    targets = examples["response"]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=512, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True, num_proc=1)

model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# Define LoRA configuration
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Prepare the model for LoRA training
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)

# Training arguments
args = TrainingArguments(
    output_dir="phi3_lora_instruct_generation",
    max_steps=1000,  # Adjust based on your dataset size
    per_device_train_batch_size=4,
    warmup_steps=0.03,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="steps",
    eval_steps=20,
    learning_rate=2e-4,
    fp16=True,
    lr_scheduler_type='constant',
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=args,
    tokenizer=tokenizer,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"]
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("trained_model")
