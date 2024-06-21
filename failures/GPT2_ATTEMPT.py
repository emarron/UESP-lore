import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset, DatasetDict

# Load tokenizer and model
model_name = "gpt2"  # Use GPT-2 as a cheaper alternative
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set pad token to eos token if not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

tokenizer.padding_side = "right"

# Load and prepare the dataset
dataset = load_dataset('json', data_files='chunked_dataset.jsonl')

# Split the dataset into training and validation sets
train_test_split = dataset['train'].train_test_split(test_size=0.1)
dataset = DatasetDict({
    'train': train_test_split['train'],
    'test': train_test_split['test']
})

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

model = AutoModelForCausalLM.from_pretrained(model_name)

# Training arguments
args = TrainingArguments(
    output_dir="gpt2_chat_generation",
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
    report_to=[],  # Disable all integrations, including wandb

)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=args,
    tokenizer=tokenizer,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"]  # Use the smaller validation set for evaluation
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("trained_model")
