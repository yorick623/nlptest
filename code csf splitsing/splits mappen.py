import os
import shutil
import pandas as pd

# Bestanden en directories
csv_file = '/workspaces/nlptest/output_colored_rows.csv'  
msg_directory = '/workspaces/nlptest/mail'  
label_directory = '/workspaces/nlptest/mail_label'
input_directory = '/workspaces/nlptest/mail_input'

# Laad CSV bestand
df = pd.read_csv(csv_file)

# Loop door alle rijen in de DataFrame
for _, row in df.iterrows():
    msg_filename = row['MSG_file']  
    label_mutatie = row['label_mutatie']  # De kolom voor mutatie-label
    label_reparatie = row['label_reparatie']  # De kolom voor reparatie-label

    # Controleer of de labels niet False zijn (True betekent dat ze gemarkeerd zijn)
    if label_mutatie or label_reparatie:
        # Als het bestand gemarkeerd is, verplaats het naar de map mail_label
        source_path = os.path.join(msg_directory, msg_filename)
        dest_path = os.path.join(label_directory, msg_filename)

        if os.path.exists(source_path):
            shutil.move(source_path, dest_path)
            print(f"Bestand {msg_filename} verplaatst naar mail_label")
        else:
            print(f"Bestand {msg_filename} niet gevonden in de bronmap.")
    else:
        # Als de labels beide False zijn, verplaats het bestand naar mail_input
        source_path = os.path.join(msg_directory, msg_filename)
        dest_path = os.path.join(input_directory, msg_filename)

        if os.path.exists(source_path):
            shutil.move(source_path, dest_path)
            print(f"Bestand {msg_filename} verplaatst naar mail_input")
        else:
            print(f"Bestand {msg_filename} niet gevonden in de bronmap.")
