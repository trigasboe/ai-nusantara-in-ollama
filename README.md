# ai-nusantara-in-ollama
Integrasi Model Nusantara ke server lokal Ollama memungkinkan pengguna menjalankan LLM Bahasa Indonesia secara offline di PC. Ini melibatkan penyiapan file model (GGUF), pembuatan Modelfile (untuk parameter &amp; template), dan perintah ollama create. Hasilnya, model bisa diakses via CLI/API Ollama.

Penjelasan lengkap dan detail ada pada file (GEMINI) Integrasi Nusantara ke Ollama ver01.pdf bisa diakses di tautan:
https://github.com/trigasboe/ai-nusantara-in-ollama/blob/main/(GEMINI)%20Integrasi%20Nusantara%20ke%20Ollama%20ver01.pdf

# Hasil (stream-on)
Bash: ollama run nusantara:0.8b-q8_0
Python: chatbot_dasar_webserver-stream-on.py

![image](https://github.com/user-attachments/assets/e82d902a-3c6c-452e-82d7-324c263ec2fb)

# Hasil (stream-on aplikasi desktop -- tkinter --)
Bash: ollama run nusantara:0.8b-q8_0
Python: chatbot_desktop_webserver-stream-on4.py

![image](https://github.com/user-attachments/assets/98014eb3-6469-4014-8d52-090a2215abb1)
