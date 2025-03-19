import openpyxl
import csv

def check_colored_rows(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active
    data = []
    for row in sheet.iter_rows():
        row_color = None
        row_data = [cell.value for cell in row]  
        MSG_file = row_data[8]
        info = row_data[10]
        label_mutatie = False
        label_reparatie = False
        for cell in row:
            color = None

            if cell.fill.patternType == 'solid':
                # Haal de RGB-waarde op van de kleur
                color = cell.fill.start_color.rgb
            if color == 'FFFFFF00':
                label_mutatie = True
            if color == 'FFFF0000':
                label_reparatie = True
        if info != 'mutatie':
            data.append([MSG_file, label_mutatie, label_reparatie])
        else:
            print('mutatie')
    with open('output_colored_rows.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['MSG_file', 'label_mutatie', 'label_reparatie'])
        writer.writerows(data)



       
        


# Gebruik de functie
source_file = '/workspaces/nlptest/input_nn_kleurlabels.xlsx' 

check_colored_rows(source_file)
