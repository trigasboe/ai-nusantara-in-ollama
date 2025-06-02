import requests
import json


#def chat_with_ollama(prompt, model_name = "llama3:latest"):
def chat_with_ollama(prompt, model_name = "nusantara:0.8b-q8_0"):
    
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": True  # <--- Perubahan Kunci: Aktifkan streaming
    }
    
    full_response_content = [] # Untuk menyimpan seluruh respons jika diperlukan nanti
    try:
        # Menggunakan stream=True pada requests.post juga
        response_stream = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        response_stream.raise_for_status() # Akan memunculkan HTTPException untuk respons status buruk (4xx atau 5xx)
        
        # Iterasi per baris dari stream
        for line in response_stream.iter_lines():
            if line:
                try:
                    # Setiap baris adalah objek JSON terpisah
                    json_chunk = json.loads(line.decode('utf-8'))
                    token = json_chunk.get("response", "")
                    print(token, end="", flush=True) # Cetak token segera, flush=True penting
                    full_response_content.append(token)
                    
                    # Ollama mengirimkan 'done: true' di chunk terakhir
                    if json_chunk.get("done"):
                        print() # Tambahkan baris baru setelah selesai
                        break
                except json.JSONDecodeError:
                    # Kadang ada baris kosong atau non-JSON, abaikan jika perlu
                    # atau tangani secara spesifik jika formatnya diketahui
                    print(f"\n[Error decoding JSON chunk: {line.decode('utf-8')}]")
                    continue # Lanjutkan ke baris berikutnya
        
        return "".join(full_response_content) # Mengembalikan seluruh respons yang telah digabungkan

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None
    except Exception as e: # Menangkap kesalahan lain yang mungkin terjadi selama streaming
        print(f"\nAn unexpected error occurred during streaming: {e}")
        return "".join(full_response_content) # Kembalikan apa yang sudah terkumpul sejauh ini

if __name__ == "__main__":
    print(f"Selamat datang di Chatbot ! Ketik 'keluar' untuk mengakhiri.")
    while True:
        user_input = input("Anda: ")
        if user_input.lower() == "keluar":
            print("Sampai jumpa!")
            break
        
        print("Bot: ", end="") # Cetak "Bot: " sekali sebelum respons streaming
        response_text = chat_with_ollama(user_input)
        
        if response_text is None: # Ini akan terjadi jika ada RequestException
            # Pesan error sudah dicetak di dalam chat_with_ollama
            # Kita bisa tambahkan pesan umum di sini jika mau, tapi mungkin redundan
            print("Maaf, ada masalah saat berkomunikasi dengan model.")
        elif not response_text and response_text is not None: # Jika fungsi mengembalikan string kosong (bukan None)
             # Ini berarti tidak ada token yang diterima, tapi tidak ada error koneksi
             # Fungsi chat_with_ollama sudah print() newline jika 'done'
             # jadi kita mungkin tidak perlu print apa-apa lagi, atau pesan spesifik
             print("Model tidak memberikan respons.")