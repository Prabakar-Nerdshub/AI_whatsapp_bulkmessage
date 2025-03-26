import pdfplumber
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import Trainer, TrainingArguments
from datasets import Dataset
from django.db import models
from transformers import pipeline
#Gpt-2 model
'''
if __name__ == "__main__":
# Load the GPT-2 model and tokenizer
    qa = pipeline("question-answering")
    model_name = 'gpt2'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Set the pad token to be the same as the eos token
    tokenizer.pad_token = tokenizer.eos_token

    # Extract text from the PDF
    text = ""
    with pdfplumber.open('/home/praba/Desktop/AI_ChatBot/backend/AI_Chatbot_api/dataset/harry.pdf') as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() if page.extract_text() else ""
            text += page_text + "\n"

    # Split the text into paragraphs using regex
    paragraphs = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.strip())

    # Limit to first 1000 paragraphs
    limit_paragraphs = 1000
    limited_paragraphs = paragraphs[:limit_paragraphs]

    # Create question-answer pairs
    questions = []
    answers = []
    for paragraph in limited_paragraphs:
        if paragraph.strip():
            questions.append(f"\n{paragraph}")
            answers.append(paragraph)

    # Create Dataset
    data = {"question": questions, "context": answers}
    dataset = Dataset.from_dict(data)


    # Tokenization function
    def tokenize_function(examples):
        input_encodings = tokenizer(
            examples['question'],
            examples['context'],
            truncation=True,
            padding='max_length',
            max_length=512,
            return_tensors='pt'
        )
        input_ids = input_encodings['input_ids']
        labels = input_ids.clone()
        labels[labels == tokenizer.pad_token_id] = -100
        input_encodings['labels'] = labels
        return input_encodings


    # Tokenize the dataset
    tokenized_datasets = dataset.train_test_split(test_size=0.2).map(tokenize_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./gpt2-harry-potter-qa",
        per_device_train_batch_size=2,  #Sets the batch size to 2 for each device (e.g., GPU or CPU) during training.
        num_train_epochs=3,             #The total number of times the model will iterate over the entire training dataset
        learning_rate=0.001,            #The learning rate is a setting that controls the size of each step the model takes while trying to improve.
        weight_decay=0.01,              #Regularization technique to prevent overfitting by penalizing large weights
        warmup_steps=500,               #helps stabilize the training at the beginning by avoiding large weight updates right away
        #save_steps=10_000,             #add this if we need save checkpoint
        logging_dir='./logs',           #Directory where TensorBoard logs will be saved. This allows for visualization of metrics during training
        evaluation_strategy="epoch",    #Configures evaluation to happen at the end of every epoch
        save_strategy="epoch",          #Saves the model at the end of each epoch, which is helpful for checkpointing
        load_best_model_at_end=True,    #Loads the best-performing model at the end of training instead of the last model trained.
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['test'],
    )

    # Fine-tune the model
    trainer.train()

    # Save the model and tokenizer
    trainer.save_model("./gpt2-harry-potter-qa")
    tokenizer.save_pretrained("./gpt2-harry-potter-qa")'''


'''class ChatHistory(models.Model):
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message: {self.message} | Response: {self.response}"'''
'''
#llama model

import pdfplumber
import re
from transformers import AutoModelForCausalLM, AutoTokenizer    
from transformers import Trainer, TrainingArguments
from datasets import Dataset

# LLaMA 3.2 3B Model Fine-Tuning
if __name__ == "__main__":
    # Load the LLaMA model and tokenizer
    model_name = "meta-llama/Llama-2-3b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Set the pad token to the eos token
    tokenizer.pad_token = tokenizer.eos_token

    # Extract text from the PDF
    text = ""
    with pdfplumber.open('/home/praba/Desktop/AI_ChatBot/backend/AI_Chatbot_api/dataset/harry.pdf') as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() if page.extract_text() else ""
            text += page_text + "\n"

    # Split the text into paragraphs using regex
    paragraphs = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.strip())

    # Limit to first 1000 paragraphs
    limit_paragraphs = 1000
    limited_paragraphs = paragraphs[:limit_paragraphs]

    # Create question-answer pairs
    questions = []
    answers = []
    for paragraph in limited_paragraphs:
        if paragraph.strip():
            questions.append(f"\n{paragraph}")
            answers.append(paragraph)

    # Create Dataset
    data = {"question": questions, "context": answers}
    dataset = Dataset.from_dict(data)

    # Tokenization function
    def tokenize_function(examples):
        input_encodings = tokenizer(
            examples['question'],
            examples['context'],
            truncation=True,
            padding='max_length',
            max_length=512,
            return_tensors='pt'
        )
        input_ids = input_encodings['input_ids']
        labels = input_ids.clone()
        labels[labels == tokenizer.pad_token_id] = -100
        input_encodings['labels'] = labels
        return input_encodings

    # Tokenize the dataset
    tokenized_datasets = dataset.train_test_split(test_size=0.2).map(tokenize_function, batched=True)

    # Define training arguments optimized for RTX 3050
    training_args = TrainingArguments(
        output_dir="./llama-harry-potter-qa",
        per_device_train_batch_size=1,   # RTX 3050 has limited VRAM; use small batch sizes
        gradient_accumulation_steps=4,  # Accumulate gradients to simulate larger batch size
        num_train_epochs=3,             # Number of training epochs
        learning_rate=5e-5,             # Adjusted learning rate
        weight_decay=0.01,              # Regularization to prevent overfitting
        warmup_steps=500,               # Stabilize training at the beginning
        logging_dir='./logs',           # TensorBoard logs
        evaluation_strategy="epoch",    # Evaluate after each epoch
        save_strategy="epoch",          # Save the model after each epoch
        fp16=True,                      # Enable mixed precision to reduce memory usage
        load_best_model_at_end=True,    # Load the best-performing model at the end
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['test'],
    )

    # Fine-tune the model
    trainer.train()

    # Save the model and tokenizer
    trainer.save_model("./llama-harry-potter-qa")
    tokenizer.save_pretrained("./llama-harry-potter-qa")'''
# models.py
from django.db import models

class Message(models.Model):
    phone_number = models.CharField(max_length=15)
    message_content = models.TextField()
    status = models.CharField(max_length=20, default="pending")  # Example field for message status

    def __str__(self):
        return f"Message to {self.phone_number} - Status: {self.status}"


