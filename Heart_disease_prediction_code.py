
"""both codes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wF6irUzJf278Hl2tTkN2H3oZEibzSm05
"""

# !pip install pandas
import pandas as pd
data_set = 'Heart Dataset.csv'
data = pd.read_csv(data_set)

"""PROMPTING CODE"""
pip install torch
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import AdamW

# Load the dataset
file_path = "Heart Dataset.csv"
data = pd.read_csv(file_path)

data.rename(
    columns={
        "chest pain type": "cp",
        "resting bp s": "trestbps",
        "fasting blood sugar": "fbs",
        "max heart rate": "thalach",
        "exercise angina": "exang",
        "Final Target": "target",
    },
    inplace=True,
)
data["text_data"] = data.apply(
    lambda row:f"Age: {row['age']}, Sex: {row['sex']}, Chest Pain Type: {row['cp']}, " \
               f"Resting BP: {row['trestbps']}, Cholesterol: {row['cholesterol']}, " \
               f"Fasting Blood Sugar: {row['fbs']}, Max Heart Rate: {row['thalach']}, " \
               f"Exercise Angina: {row['exang']}", axis=1
)

output_path = "Heart_Dataset_Textual.csv"  # Specify your desired output file name
data.to_csv(output_path, index=False)

print(f"Textual data saved to {output_path}")

X = data["text_data"]
y = data["target"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

def tokenize_data(texts, tokenizer, max_len=128):
    return tokenizer(
        list(texts), padding=True, truncation=True, max_length=max_len, return_tensors="pt"
    )

train_tokens = tokenize_data(X_train, tokenizer)
test_tokens = tokenize_data(X_test, tokenizer)

# Convert labels to tensors
train_labels = torch.tensor(y_train.values)
test_labels = torch.tensor(y_test.values)

# Training setup
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import AdamW

train_data = TensorDataset(train_tokens["input_ids"], train_tokens["attention_mask"], train_labels)
test_data = TensorDataset(test_tokens["input_ids"], test_tokens["attention_mask"], test_labels)

train_dataloader = DataLoader(train_data, batch_size=16, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=16)

optimizer = AdamW(model.parameters(), lr=2e-5)

epochs = 5
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_dataloader:
        input_ids, attention_mask, labels = [b.to("cpu") for b in batch]

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    avg_loss = total_loss / len(train_dataloader)
    print(f"Epoch {epoch + 1}/{epochs} - Training Loss: {avg_loss:.4f}")

model.eval()
predictions, true_labels = [], []

with torch.no_grad():
    for batch in test_dataloader:
        input_ids, attention_mask, labels = [b.to("cuda") for b in batch]
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        preds = torch.argmax(logits, dim=1)
        predictions.extend(preds.cpu().numpy())
        true_labels.extend(labels.cpu().numpy())

accuracy = accuracy_score(true_labels, predictions)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(true_labels, predictions))

def prompt_user_for_input():
    age = input("Enter age: ")
    sex = input("Enter sex (1 = male, 0 = female): ")
    cp = input("Enter chest pain type (1-4): ")
    trestbps = input("Enter resting blood pressure: ")
    chol = input("Enter cholesterol level: ")
    fbs = input("Enter fasting blood sugar (1 = true, 0 = false): ")
    thalach = input("Enter maximum heart rate achieved: ")
    exang = input("Enter exercise-induced angina (1 = yes, 0 = no): ")

    user_text = (f"Patient with age {age}, sex {sex}, chest pain type {cp}, "
                 f"resting blood pressure {trestbps}, cholesterol {chol}, "
                 f"fasting blood sugar {fbs}, max heart rate {thalach}, "
                 f"exercise-induced angina {exang}.")
    return user_text

user_text = prompt_user_for_input()
user_tokens = tokenize_data([user_text], tokenizer)

model.eval()
with torch.no_grad():
    input_ids = user_tokens["input_ids"].to("cuda")
    attention_mask = user_tokens["attention_mask"].to("cpu")
    outputs = model(input_ids, attention_mask=attention_mask)
    prediction = torch.argmax(outputs.logits, dim=1).item()

if prediction == 0:
    print("No heart disease detected.")
else:
    print("Heart disease detected. Consult with a medical professional.")