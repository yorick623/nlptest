import os
import random
import extract_msg
from email.utils import parseaddr
import pandas as pd
import re
import spacy
nlp = spacy.load("nl_core_news_sm")

directory = "/workspaces/nlptest/mail_input"  


def split_on_first_match(input_string, search_list):
    
    for term in search_list:
        
        match = re.search(r"(.*?)(?=\s" + re.escape(term) + ")", input_string)
        if match:
            return match.group(1).strip(), input_string[match.end():].strip()  

    
    return input_string, ""




def clean_text(text):
    
    text = re.sub(r'<.*?>', '', text)
    
   
    text = re.sub(r'\s+', ' ', text).strip()

    text = re.sub(r'WAARSCHUWING:.*?phishing', '', text, flags=re.DOTALL)

    text = re.sub(r'\[cid:[^\]]*\]', '', text)

    text = re.sub(r'https?://[^\s]+', '', text)

    text = re.sub(r'\[ thread::.*?:: \]', '', text)
    
    text = text.replace('\u200b', '')
    
    return text
def extract_email_details(msg_file):
    
    msg = extract_msg.Message(msg_file)
    all_senders = []
    subject = msg.subject
    sender = msg.sender
    body = msg.body
    date = msg.date
    to = msg.to
    cc = msg.cc
    body = clean_text(body)
    
    forwarded_senders = []
    all_senders.append(sender)
    
    forwarded_senders = re.findall(r"Van: ([^\n]+?)(?=\sAan:)", body)
    if forwarded_senders:
        
        for sender in forwarded_senders:
            sender = re.search(r"([^\s]+(?:\s[^\s]+)*)(?=\s(?:Verzonden|>))", sender).group(1)
            sender = sender.rstrip(' >')
            all_senders.append(sender)
        
        
    else:
        forwarded_senders = []  
    list = body.split("Van: ")
    list = [f"Van: {part}" if idx > 0 else part for idx, part in enumerate(list)]
    part_0 = f"Van: {sender} Verzonden: {date} Aan: {to} CC: {cc} Onderwerp: {subject}\n\n"
    
    
    part_0 += list[0]
    list[0] = part_0

    binnengekomen_bericht = nlp(part_0)


    forwarded_message = []
    for message in list[1:]:
        if message is not None:
            if re.search(r"(Onderwerp:)", message):
                message = re.sub(r"(Onderwerp:)", r"\1\n\n", message)
            forwarded_message.append(message)
    

    email_data = {
        "msg_file": msg_file,
        "binnengekomen bericht": binnengekomen_bericht,
        "forwarded_message":     forwarded_message
    }


    return email_data




def process_email_folder(folder_path):
    email_data = []
    
    for filename in os.listdir(folder_path)[:10]:
        if filename.endswith(".msg"):
            print(f"\nProcessing: {filename}")
            msg_file = os.path.join(folder_path, filename) 
            try:
                email_details = extract_email_details(msg_file)
                
                if email_details is None:
                    print(f"Skipping invalid email file: {filename}")
                    continue  

                #
                email_data.append(email_details)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                os.remove(msg_file)
                continue  

    return email_data

def remove_illegal_chars(text):
    if isinstance(text, str):
        return "".join(char for char in text if ord(char) >= 32 or char in "\n\r\t")
    return text  
import re

import re

import re

import re

def check_label(bericht):
    
    werkbon_re = r"(werkbon|werk order|werk opdracht|service opdracht|technische interventie|servicebezoek|onderhoudsrapport|storingsticket|klus|klusbon|servicecontract)"
    factuur_re = r"(factuur|rekening|betalingsbewijs|betaalopdracht|bedrag|invoice)"
    bestelling_re = r"(bestelling|orderbevestiging|verzoek tot levering|leveringsbevestiging|bestellingsnummer|order)"

    
    tag_re = r"(tag|pasje|badge|toegangskaart|identificatiekaart|kaartje|deeltags|personaliseren|tag mutatie|toegangscontrole|rechten op pas|tag muteren|toegang geven|toegangsrechten|tagtoegang)"
    mutatie_re = r"(mutatie|rechten wijzigen|toevoegen aan deur|toegang intrekken|deuren beheren|deuren toegang|rechten aanpassen|toegangsrechten verwijderen|deurtags mutatie)"
    persoon_toevoegen_re = r"(toevoegen aan deuren|toevoegen aan tag|toegang tot deuren|toegangsrechten verlenen|personen toevoegen|gebruikers toevoegen|tag toevoegen|deuren recht geven)"
    inplannen_re = r"(inplannen|afspraak maken|afspraak inplannen|plannen|plannen van afspraak|planning maken|afspraak plannen|onderhoud inplannen|reparatie inplannen|afspraak boeken|planning afspreken|afspraken maken|datum kiezen|tijd kiezen|reparatie plannen|afspraak vastleggen|afspraak bepalen|afspraak inplannen|moment kiezen|afspraken maken voor|afspraak vaststellen|afspraak inplannen met|tijdstip plannen|datum plannen|reparatie inplannen|afspraak aanmelden|onderhoud plannen|programma maken|afspraken plannen|geplande afspraak|afspraak bevestigen|afspraak voorstellen|afspraak uitvoeren|inplanbare|tussentijdse afspraak|agenda invullen)"
    reparatie_re = r"(reparatie|herstel|onderhoud|kapot|defect|storing|breuk|probleem|vervangen|maken|repareren|hersteld|afspraak maken|reparatieverzoek|technisch probleem|panne|niet werkend|storing melden|herstelverzoek|inspectie|technisch defect|probleem oplossen|defect melden|herstellen|beurt|reparatie aanvraag|reparatie verzoek|storing repareren|storing verhelpen|kapotte|niet functioneren|uitval|defecten|scheur|problemen met|onderhoudsverzoek|onderhoud aanvragen|storingen|kapotgaan|stoppen met werken|mankeert iets aan|minder goed functioneren|functioneert niet|kapotte apparatuur|storingen met|kapot product|reparatie melden|mankement|onderdelen vervangen|storing in het systeem)"

    
    email_toevoegen_re = r"(\bemail\s*(adres)?\s*(toevoegen|toegevoegd|registreren|toevoegen aan app|toevoegen aan systeem|registreren voor app|vermelden)\b)"
    bewoner_toevoegen_re = r"(bewoner toevoegen|bewoner inschrijven|bewoner registreren|bewoner toevoegen aan systeem|bewoner aanmelden|bewoner toegang geven|bewoner toevoegen aan app)"
    if re.search(reparatie_re, bericht, re.IGNORECASE) and re.search(inplannen_re, bericht, re.IGNORECASE):
        return "werkbon"  # Als het bericht zowel reparatie als inplannen bevat, label het als werkbon
    elif re.search(reparatie_re, bericht, re.IGNORECASE):
        return "reparatie"  # Als het bericht alleen reparatie bevat, label het als reparatie
    elif (re.search(werkbon_re, bericht, re.IGNORECASE) or re.search(factuur_re, bericht, re.IGNORECASE) or re.search(bestelling_re, bericht, re.IGNORECASE)) and not re.search(inplannen_re, bericht, re.IGNORECASE):
        return "reparatie"  # Als het bericht werkbon bevat maar niet inplannen, label het als reparatie
    elif (re.search(werkbon_re, bericht, re.IGNORECASE) or re.search(factuur_re, bericht, re.IGNORECASE) or re.search(bestelling_re, bericht, re.IGNORECASE)) and re.search(inplannen_re, bericht, re.IGNORECASE):
        return "werkbon"  # Als het bericht werkbon en inplannen bevat, label het als werkbon
    elif (re.search(tag_re, bericht, re.IGNORECASE) or re.search(mutatie_re, bericht, re.IGNORECASE) or re.search(persoon_toevoegen_re, bericht, re.IGNORECASE) 
          or re.search(email_toevoegen_re, bericht, re.IGNORECASE) or re.search(bewoner_toevoegen_re, bericht, re.IGNORECASE)):
        return "mutatie"  # Als het bericht een van de mutatie-gerelateerde termen bevat, label het als mutatie
    return "onbekend"  # Als geen enkele conditie overeenkomt, label het als onbekend




def create_excel_from_email_data(email_data, output_path):
    rows = []
    for email in email_data:
        msg_file = email.get('msg_file', 'Unknown') 
        berichten = []
        
        # Verwerk het 'binnengekomen bericht'
        binnengekomen = email["binnengekomen bericht"]
        if isinstance(binnengekomen, spacy.tokens.Doc):
            bericht_text = remove_illegal_chars(binnengekomen.text)
        else:
            bericht_text = remove_illegal_chars(binnengekomen)
        
        # Roep check_label aan en krijg het label voor het bericht
        label = check_label(bericht_text)
        berichten.append((msg_file, 0, bericht_text, bericht_text, label))

        # Voeg de forwarded berichten toe
        for idx, forwarded_msg in enumerate(email["forwarded_message"]):
            if isinstance(forwarded_msg, spacy.tokens.Doc):
                forwarded_text = remove_illegal_chars(forwarded_msg.text)
            else:
                forwarded_text = remove_illegal_chars(forwarded_msg)
            
            label = check_label(forwarded_text)
            berichten.append((msg_file, idx + 1, forwarded_text, forwarded_text, label))

        # Verwerk de berichten zodat 'bericht' alleen de tekst na de eerste \n\n bevat
        for bericht in berichten:
            bericht_info = bericht[2]  # Bericht_info is de tekst met alles
            bericht_text = bericht_info.split("\n\n", 1)[1] if "\n\n" in bericht_info else bericht_info
            rows.append((bericht[0], bericht[1], bericht_info, bericht_text, bericht[4]))

    
    df = pd.DataFrame(rows, columns=["msg_file", "bericht_diepte", "bericht_info","bericht", "label"])
    
    print(df)
    df.to_excel(output_path, index=False)


email_data = process_email_folder(directory)


output_path = "email_data.xlsx"  
create_excel_from_email_data(email_data, output_path)
print(f"Excel bestand opgeslagen als {output_path}")

