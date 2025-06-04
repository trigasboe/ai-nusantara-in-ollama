# ai-nusantara-in-ollama
Integrasi Model Nusantara ke server lokal Ollama memungkinkan pengguna menjalankan LLM Bahasa Indonesia secara offline di PC. Hal ini diperlukan untuk menyiapkan file model (GGUF), membuat file Modelfile (untuk parameter &amp; template), dan melakukan perintah ollama create. Hasilnya, model bisa diakses via CLI/API Ollama dengan url: "http://localhost:11434/api/generate".

Penjelasan lengkap dan detail ada pada file (GEMINI) Integrasi Nusantara ke Ollama ver01.pdf bisa diakses di tautan:
https://github.com/trigasboe/ai-nusantara-in-ollama/blob/main/(GEMINI)%20Integrasi%20Nusantara%20ke%20Ollama%20ver01.pdf

# Hasil (stream-on)
1. Running ollama yang sudah terinstal di windows.
       ![image](https://github.com/user-attachments/assets/8c7a096f-5dde-41c1-a789-074feb44a65d)
            
2. (Bisa melalui CMD windows) Ketik perintah:
           - Bash: ollama --version                   ➡ untuk melihat versi ollama
           - Bash: ollama list                        ➡ untuk melihat daftar model yang terintegrasi di ollama
           - Bash: ollama run nusantara:0.8b-q8_0     ➡ Menjalankan model nusantara:0.8b-q8_0
           - Tuliskan sembarang kalimat perintah (prompt) untuk menguji model.
             ![image](https://github.com/user-attachments/assets/f273f244-9ec5-4b22-a2d3-d8ee71c8d039)

4. Jalankan kode Python: chatbot_dasar_webserver-stream-on.py (misal menggunakan IDE Thonny)

![image](https://github.com/user-attachments/assets/e82d902a-3c6c-452e-82d7-324c263ec2fb)



# Hasil (stream-on aplikasi desktop -- Library tkinter --)
1. Jalankan kode Python: chatbot_desktop_webserver-stream-on4.py

![image](https://github.com/user-attachments/assets/98014eb3-6469-4014-8d52-090a2215abb1)
