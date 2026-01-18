import os
import subprocess

# --- KONFIGURACJA ---
NAZWA_TELEFONU = "S23"  # Program będzie szukał urządzenia z tą nazwą
CZESTOTLIWOSC = "107.9"
# --------------------

def start_radio():
    print(f"Szukam telefonu: {NAZWA_TELEFONU}...")
    
    # Komenda wyszukująca ID urządzenia Bluetooth po nazwie
    find_source = f"pactl list sources | grep -B 20 'device.description = .*{NAZWA_TELEFONU}' | grep 'Name:' | cut -d' ' -f2"
    
    try:
        source_id = subprocess.check_output(find_source, shell=True).decode().strip()
        
        if source_id:
            print(f"Znalazłem! Łączę z: {source_id}")
            # PEŁNA KOMENDA: Bluetooth -> Sox (odcinanie zacięć) -> Nadajnik (wysoki priorytet)
            cmd = (
                f"pacat -r -d {source_id} | "
                f"sox -t raw -r 44100 -e signed-integer -b 16 -c 2 - -t wav -b 16 -r 22050 -c 1 - | "
                f"sudo chrt -f 99 ./pi_fm_rds -freq {CZESTOTLIWOSC} -audio -"
            )
            os.system(cmd)
        else:
            print(f"BŁĄD: Nie widzę połączonego telefonu '{NAZWA_TELEFONU}'.")
            print("Upewnij się, że Bluetooth w S23 jest połączony z Raspberry Pi.")
            
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    start_radio()

