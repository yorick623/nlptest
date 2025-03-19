import torch
from torch.utils.data import Dataset, DataLoader
from outdated.EmailDataset import EmailDataset
from outdated.neural_network import EmailClassifier
import torch.nn as nn
import pickle

# Stel je features en labels in
tfidf_matrix, labels = load_tfidf_matrix("tfidf_data.pkl")  # Gegevens laden
batch_size = 32
num_classes = len(set(labels))  # Het aantal unieke categorieën in je labels
data_loader = create_data_loader_from_matrix(tfidf_matrix, labels, batch_size=batch_size)
input_size = tfidf_matrix.shape[1]  # Het aantal TF-IDF-features
hidden_size = 128  # Kies een geschikte verborgen grootte (experimenteer hiermee)
output_size = num_classes  # Aantal unieke categorieën (bijv. spam vs. niet-spam)
learning_rate = 0.001  # Standaard startpunt voor het leerproces

def load_tfidf_matrix(filename="tfidf_data.pkl"):
    with open(filename, "rb") as file:
        data = pickle.load(file)
    print(f"TF-IDF-matrix geladen vanuit {filename}")
    return data["tfidf_matrix"], data["feature_names"]


def create_data_loader(features, labels, batch_size):
    dataset = EmailDataset(features, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
import torch.optim as optim

def initialize_model(input_size, hidden_size, output_size, learning_rate):
    model = EmailClassifier(input_size, hidden_size, output_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    return model, criterion, optimizer
    
def train_model(model, data_loader, criterion, optimizer, num_epochs):
    model.train()
    for epoch in range(num_epochs):
        for inputs, labels in data_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
def evaluate_model(model, data_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in data_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return correct / total

def create_data_loader_from_matrix(tfidf_matrix, labels, batch_size):
    features = torch.tensor(tfidf_matrix.toarray(), dtype=torch.float32)  
    labels = torch.tensor(labels, dtype=torch.long)  
    dataset = torch.utils.data.TensorDataset(features, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)


# Model, verliesfunctie en optimizer initialiseren
model, criterion, optimizer = initialize_model(input_size, hidden_size, output_size, learning_rate)

num_epochs = 10  # Kies een geschikt aantal epochs
train_model(model, data_loader, criterion, optimizer, num_epochs)

accuracy = evaluate_model(model, data_loader)
print(f"Modelnauwkeurigheid: {accuracy * 100:.2f}%")


