import json

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, BitsAndBytesConfig
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from trl import SFTTrainer

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

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.1",
    device_map='auto',
    quantization_config=nf4_config,
    use_cache=False
)

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# Define LoRA configuration
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA to the model
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)

# Training arguments
args = TrainingArguments(
    output_dir="mistral_instruct_generation",
    # num_train_epochs=5,
    max_steps=100,
    per_device_train_batch_size=4,
    warmup_steps=0.03,
    logging_steps=10,
    save_strategy="epoch",
    # evaluation_strategy="epoch",
    evaluation_strategy="steps",
    eval_steps=20,
    learning_rate=2e-4,
    bf16=True,
    lr_scheduler_type='constant',
)

# Initialize Trainer
max_seq_length = 2048

trainer = SFTTrainer(
    model=model,
    peft_config=peft_config,
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    packing=True,
    args=args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"]
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("trained_model")
