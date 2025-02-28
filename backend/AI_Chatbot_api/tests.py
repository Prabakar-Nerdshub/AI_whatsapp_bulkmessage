# backend/AI_Chatbot_api/tests.py
'''from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_path = "/home/praba/Desktop/AI_ChatBot/backend/AI_Chatbot_api/gpt2-harry-potter-qa"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

def ask_question(question):
    if not question:
        return "No question provided."
    if len(question) > 100:
        return "Question is too long. Please ask a shorter question."
    try:
        inputs = tokenizer.encode(question, return_tensors="pt")
        outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"'''

# backend/AI_Chatbot_api/tests.py
'''import ollama

def ask_question(question):
    if not question:
        return "No question provided."
    if len(question) > 100:
        return "Question is too long. Please ask a shorter question."
    try:
        response = ollama.chat(
            #model='meta-llama/Llama-3.2-3B',
            #model = 'meta-llama/Llama-3.3-70B-Instruct'
            messages=[{'role': 'user', 'content': question}]
        )
        # Extract response content from Ollama's response format
        answer = response.get('message', {}).get('content', 'No response from model.')
        return answer.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"'''

