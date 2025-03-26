
#model
import os
import torch
from PyPDF2 import PdfReader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from datasets import Dataset
from peft import get_peft_model, LoraConfig, TaskType
from transformers import BitsAndBytesConfig

# Step 1: Convert PDF to text
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Path to your PDF
pdf_path = "/home/praba/Desktop/AI_ChatBot/backend/AI_Chatbot_api/dataset/budget_speech.pdf"
text_data = extract_text_from_pdf(pdf_path)

# Save extracted text to a file (for debugging or reuse)
with open("budget_speech.txt", "w") as f:
    f.write(text_data)

# Step 2: Tokenize the dataset
def create_dataset(text):
    lines = text.split("\n")
    return Dataset.from_dict({"text": lines})

dataset = create_dataset(text_data)

# Step 3: Load Meta's Llama 3.2-3B model and tokenizer
model_name = "meta-llama/Llama-3.2-3B"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Step 4: Apply LoRA for memory-efficient fine-tuning
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.1,
    bias="none",
)

model = get_peft_model(model, peft_config)

# Enable gradient checkpointing for reduced memory usage
model.gradient_checkpointing_enable()

# Step 5: Tokenize and preprocess the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Step 6: Define data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Step 7: Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="steps",
    eval_steps=500,
    save_steps=500,
    logging_steps=100,
    per_device_train_batch_size=1,  # Adjust to your GPU capacity
    gradient_accumulation_steps=16,  # Simulates larger batch size
    num_train_epochs=3,
    learning_rate=5e-5,
    fp16=True,  # Enable mixed precision
    save_total_limit=2,
    optim="adamw_torch",
    report_to="none",
)

# Step 8: Train the model
trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
    data_collator=data_collator,
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")

# Step 9: Quantize the model
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
)

quantized_model = AutoModelForCausalLM.from_pretrained(
    "./trained_model",
    quantization_config=bnb_config,
    device_map="auto",  # Automatically maps model to available devices
)

# Save the quantized model
quantized_model.save_pretrained("./quantized_model")
tokenizer.save_pretrained("./quantized_model")

print("Training and quantization complete. Models saved in './trained_model' and './quantized_model'")

