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

'''from pymongo.mongo_client import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('vedhamaniprabakar')
password = urllib.parse.quote_plus('prabavj1503')
print(password)
print("Prabavj@1503")
uri = "mongodb+srv://username:password@cluster0.bnrac.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)'''

#"C:\Users\Admin\Desktop\01contact_details.xlsx"
#curl -X POST -F "file=@C:\Users\Admin\Desktop\01contact_details.xlsx" http://127.0.0.1:8000/api/upload

from django.http import JsonResponse
from bson import ObjectId
import gridfs
import pandas as pd
from io import BytesIO
from pymongo import MongoClient
from pymongo.server_api import ServerApi


db_password = 'prabavj1503'
uri = f"mongodb+srv://vedhamaniprabakar:{db_password}@cluster0.bnrac.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["bulk_messaging_db"]
fs = gridfs.GridFS(db)

file_id = ObjectId('67c6cd2da64d10febc118884')

# ✅ Fetch file from GridFS
grid_out = fs.get(file_id)
file_content = BytesIO(grid_out.read())  # Convert binary to file-like object

# ✅ Determine File Type (CSV / Excel)
filename = grid_out.filename.lower()
if filename.endswith(".csv"):
    df = pd.read_csv(file_content)
elif filename.endswith((".xls", ".xlsx")):
    df = pd.read_excel(file_content, engine="openpyxl")  # ✅ Use openpyxl for XLSX
phone_numbers = df.iloc[:, 1].dropna().astype(str).tolist()
print(phone_numbers)
pn = []
for i in phone_numbers:
    pn.append('91'+str(i))

print(pn)