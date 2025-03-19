import os
import pandas as pd
from tqdm import tqdm
from msg_parser import MsOxMessage
from bs4 import BeautifulSoup

directory_path = "/workspaces/nlptest/mail"
csv_filename = "handmatig_gelabelde_emails.csv"

LABELS = {
    "0": "tag_mutatie",
    "1": "reparatie_verzoek",
    "2": "niet_van_toepassing"
}

def load_existing_labels():
    """Laadt bestaande labels als het CSV-bestand al bestaat."""
    if os.path.exists(csv_filename):
        return pd.read_csv(csv_filename).set_index("filename").to_dict("index")
    return {}

def save_label(email):
    """Slaat een gelabelde e-mail direct op in de CSV."""
    df = pd.DataFrame([email])
    if not os.path.exists(csv_filename):
        df.to_csv(csv_filename, index=False)
    else:
        df.to_csv(csv_filename, mode="a", header=False, index=False)

def clean_email_content(content):
    """Verwijdert HTML-tags en lege regels uit de inhoud."""
    # Verwijder HTML door gebruik te maken van BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    clean_content = soup.get_text()  # Haal alleen de tekst op, zonder HTML

    # Verwijder lege regels
    clean_content = "\n".join([line.strip() for line in clean_content.split("\n") if line.strip()])

    return clean_content

def process_all_email_data(msg_folder):
    """Laadt alle e-mails en kijkt welke al gelabeld zijn."""
    existing_labels = load_existing_labels()
    email_data_list = []

    for filename in tqdm(os.listdir(msg_folder), desc="E-mails verwerken"):
        if filename.endswith(".msg") and filename not in existing_labels:
            filepath = os.path.join(msg_folder, filename)
            try:
                msg = MsOxMessage(filepath)
                email_data = {
                    "filename": filename,
                    "subject": msg.subject if msg.subject else "Geen onderwerp",
                    "body": clean_email_content(msg.body if msg.body else "Geen inhoud"),
                    "label": ""  # Standaard geen label
                }
                email_data_list.append(email_data)
            except Exception as e:
                print(f"Fout bij verwerken van bestand {filename}: {e}")
    
    return email_data_list

def label_emails(email_data_list):
    """Toont e-mails één voor één en slaat de labels direct op als integer."""
    for email in email_data_list:
        print("\n" + "="*50)
        print(f"Bestand: {email['filename']}")
        print(f"Onderwerp: {email['subject']}")
        print(f"Inhoud:\n{email['body']}")
        print("="*50)

        while True:
            label_input = input("Voer label in (0 = tag_mutatie, 1 = reparatie_verzoek, 2 = niet_van_toepassing) of druk Enter om over te slaan: ").strip()
            if label_input == "":
                print("E-mail overgeslagen.")
                break
            elif label_input in LABELS:
                email["label"] = int(label_input)
                save_label(email)
                print(f"Label '{LABELS[label_input]}' opgeslagen als {label_input} voor {email['filename']}.")
                break
            else:
                print("Ongeldige invoer. Voer 0, 1 of 2 in.")

# Stap 1: Verwerk alle e-mails die nog niet gelabeld zijn
email_data_list = process_all_email_data(directory_path)

# Stap 2: Handmatig labelen via de terminal
label_emails(email_data_list)
