import io

def process_trusted_sites(input_data):
    # Definiera de 50 sidor som bedöms som mest tillförlitliga (ID:n från filen)
    # Urvalet baseras på etablerade myndigheter, utbildning och global infrastruktur.
    trusted_ids = {
        1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 17, 21, 22, 23, 26, 29, 30, 31,
        32, 33, 34, 35, 37, 38, 53, 55, 63, 64, 65, 66, 67, 82, 83, 90, 130, 131,
        133, 150, 151, 152, 191, 193, 194, 195, 197, 257, 271, 272
    }

    lines = input_data.strip().split('\n')
    header = lines[0]
    output = [header]

    for line in lines[1:]:
        parts = line.split(',')
        if len(parts) < 3:
            continue

        site_id = int(parts[0])
        name = parts[1]
        links = parts[2] # I originalet ligger länkarna på index 2 eftersom bool saknas

        # Sätt True om ID finns i listan, annars False
        is_trusted = "True" if site_id in trusted_ids else "False"

        # Skapa den nya raden enligt formatet: <Nr>,<namn>,<bool Trusted>,<länkningar>
        new_line = f"{site_id},{name},{is_trusted},{links}"
        output.append(new_line)

    return "\n".join(output)

# Läs in data (Här antar vi att filen heter SidorExempel.txt)
try:
    with open('SidorExempel.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    processed_content = process_trusted_sites(content)

    with open('SidorExempel_Uppdaterad.txt', 'w', encoding='utf-8') as file:
        file.write(processed_content)

    print("Filen har skapats: SidorExempel_Uppdaterad.txt")
except FileNotFoundError:
    print("Kunde inte hitta källfilen.")
