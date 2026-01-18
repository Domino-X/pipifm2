import os
import subprocess

def start_radio():
    # W PipeWire/PulseAudio '@DEFAULT_SOURCE@' to zawsze aktualnie grający telefon
    source = "@DEFAULT_SOURCE@"
    
    print(f"Przechwytuję aktywny strumień audio...")
    
    # Komenda, która bierze dźwięk z domyślnego źródła (Twojego S23)
    # i wysyła go do nadajnika FM
    cmd = (
        f"parec -d {source} --latency-msec=20 | "
        f"sox -t raw -r 44100 -e signed-integer -b 16 -c 2 - -t wav -b 16 -r 22050 -c 1 - | "
        f"sudo chrt -f 99 ./pi_fm_rds -freq 107.9 -audio -"
    )
    
    try:
        os.system(cmd)
    except Exception as e:
        print(f"Błąd uruchamiania: {e}")

if __name__ == "__main__":
    start_radio()
