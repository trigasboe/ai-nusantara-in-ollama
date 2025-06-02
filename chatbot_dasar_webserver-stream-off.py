import requests
import json

#def chat_with_ollama(prompt, model_name="nusantara-0.8b-indo-chat"):
def chat_with_ollama(prompt, model_name="nusantara:0.8b-q8_0"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False # Set true jika ingin streaming respons
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Akan memunculkan HTTPException untuk respons status buruk (4xx atau 5xx)
        result = response.json()
        return result["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None

if __name__ == "__main__":
    print("Selamat datang di Chatbot Nusantara-0.8b-Indo-Chat! Ketik 'keluar' untuk mengakhiri.")
    while True:
        user_input = input("Anda: ")
        if user_input.lower() == "keluar":
            print("Sampai jumpa!")
            break
        
        response = chat_with_ollama(user_input)
        if response:
            print(f"Bot: {response}")
        else:
            print("Bot: Maaf, ada masalah saat berkomunikasi dengan model.")
