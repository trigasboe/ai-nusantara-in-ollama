import requests
import json
import tkinter as tk
from tkinter import scrolledtext, END, INSERT 
import threading

# --- Fungsi chat_with_ollama (TETAP SAMA SEPERTI SEBELUMNYA) ---
def chat_with_ollama(prompt, model_name, token_callback_gui, final_callback_gui):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": True
    }
    full_response_content = []
    error_occurred = False
    error_message_text = None
    first_token_sent_to_gui = False
    try:
        response_stream = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        response_stream.raise_for_status()
        for line in response_stream.iter_lines():
            if line:
                try:
                    json_chunk = json.loads(line.decode('utf-8'))
                    token = json_chunk.get("response", "")
                    if token: 
                        token_callback_gui(token, not first_token_sent_to_gui)
                        first_token_sent_to_gui = True
                    full_response_content.append(token)
                    if json_chunk.get("done"):
                        break
                except json.JSONDecodeError:
                    error_message_text = f"\n[Error decoding JSON chunk: {line.decode('utf-8')}]"
                    if first_token_sent_to_gui: 
                         token_callback_gui(error_message_text, False) 
                    else: 
                        error_occurred = True
                    continue
    except requests.exceptions.RequestException as e:
        error_message_text = f"Error connecting to Ollama: {e}"
        error_occurred = True
    except Exception as e:
        error_message_text = f"An unexpected error occurred during streaming: {e}"
        error_occurred = True
    if error_occurred and not first_token_sent_to_gui:
         final_callback_gui(error_message_text if error_message_text else "Unknown error occurred before first token.")
    elif error_occurred and first_token_sent_to_gui:
        final_callback_gui(None) 
    else: 
        final_callback_gui(error_message_text if not first_token_sent_to_gui and error_message_text else None)

class ChatApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("@trigasboe - Chatbot -- nusantara:0.8b-q8_0 -- Ollama") # Judul diupdate sesuai kode Anda
        self.root.geometry("700x500")

        self.bg_color = "#282c34" 
        self.text_color = "#abb2bf" 
        self.entry_bg = "#1c1f24" 
        self.button_bg = "#61afef" 
        self.button_fg = "#282c34" 
        self.font_style = ("Arial", 11)
        self.prefix_font_style = (self.font_style[0], self.font_style[1] + 1, "bold")

        self.root.configure(bg=self.bg_color)
        self.first_bot_token_handled = False

        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, state='normal', bg=self.entry_bg, fg=self.text_color,
            font=self.font_style, insertbackground=self.text_color, relief=tk.FLAT, padx=5, pady=5
        )
        self.chat_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.chat_area.tag_configure("user_prefix_tag", font=self.prefix_font_style, foreground=self.button_bg) 
        self.chat_area.tag_configure("bot_prefix_tag", font=self.prefix_font_style, foreground="#98c379")    
        self.chat_area.tag_configure("error_tag", font=self.font_style, foreground="#e06c75") 
        
        self.chat_area.insert(INSERT, "Selamat datang di Chatbot Nusantara! Silakan ketik pesan Anda.\n\n")
        self.chat_area.insert(END, "Anda: ", "user_prefix_tag") 
        self.chat_area.insert(END, "▸ ") 
        self.chat_area.config(state='disabled') 

        input_frame = tk.Frame(main_frame, bg=self.bg_color, pady=5)
        input_frame.pack(fill=tk.X)
        
        self.user_input_entry = tk.Entry(
            input_frame, width=70, bg=self.entry_bg, fg=self.text_color, font=self.font_style,
            insertbackground=self.text_color, relief=tk.FLAT, highlightthickness=1,
            highlightbackground=self.text_color, highlightcolor=self.button_bg
            )
        self.user_input_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True, ipady=5)
        self.user_input_entry.bind("<Return>", self.send_message_event)

        self.send_button = tk.Button(
            input_frame, text="Kirim", command=self.send_message_event, bg=self.button_bg,
            fg=self.button_fg, font=(self.font_style[0], self.font_style[1], "bold"),
            relief=tk.FLAT, padx=10, pady=4, activebackground="#509bde", activeforeground=self.button_fg
            )
        self.send_button.pack(side=tk.RIGHT)

        self.user_input_entry.focus_set()

    def display_message(self, sender, message, tag=None): # Metode ini dipertahankan
        self.chat_area.config(state='normal')
        # Jika sender "Anda", gunakan tag yang sesuai
        actual_tag = tag
        if sender == "Anda":
            actual_tag = "user_prefix_tag"
        elif sender == "Bot": # Untuk konsistensi jika dipanggil untuk Bot dari sini
             actual_tag = "bot_prefix_tag"

        if actual_tag:
            self.chat_area.insert(END, f"{sender}: ", actual_tag)
        else:
            self.chat_area.insert(END, f"{sender}: ")

        self.chat_area.insert(END, f"{message}\n") 
        self.chat_area.config(state='disabled')
        self.chat_area.see(END)

    def send_message_event(self, event=None):
        user_message = self.user_input_entry.get()
        if user_message.strip():
            self.chat_area.config(state='normal')
            
            tag_ranges = self.chat_area.tag_ranges("user_prefix_tag")
            if tag_ranges:
                insertion_point_after_prefix = tag_ranges[-1] 
                self.chat_area.delete(insertion_point_after_prefix, END)
                self.chat_area.insert(END, f" {user_message}\n") 
            else:
                self.chat_area.insert(END, "Anda: ", "user_prefix_tag")
                self.chat_area.insert(END, f" {user_message}\n")

            self.chat_area.see(END)
            self.chat_area.config(state='disabled')
            
            self.user_input_entry.delete(0, END)

            self.user_input_entry.config(state='disabled')
            self.send_button.config(state='disabled')

            self.chat_area.config(state='normal')
            self.chat_area.insert(END, "\n") 
            self.chat_area.insert(END, "Bot: ", "bot_prefix_tag") 
            self.chat_area.insert(END, "[Sedang memproses...]", "bot_placeholder_tag") 
            self.chat_area.insert(END, "\n") 
            self.chat_area.config(state='disabled')
            self.chat_area.see(END)
            
            self.first_bot_token_handled = False 

            threading.Thread(target=chat_with_ollama,
                             args=(user_message, "nusantara:0.8b-q8_0", 
                                   self.handle_ollama_token, self.handle_ollama_final),
                             daemon=True).start()

    def _handle_ollama_token_gui(self, token_text, is_first_token):
        self.chat_area.config(state='normal')
        if is_first_token and not self.first_bot_token_handled:
            if self.chat_area.tag_ranges("bot_placeholder_tag"):
                placeholder_start, _ = self.chat_area.tag_ranges("bot_placeholder_tag")
                self.chat_area.delete(placeholder_start, f"{placeholder_start}+{len('[Sedang memproses...]')}c")
            self.chat_area.insert(INSERT, token_text) 
            self.first_bot_token_handled = True
        else:
            self.chat_area.insert(END, token_text)
        
        self.chat_area.see(END)
        self.chat_area.config(state='disabled')

    def handle_ollama_token(self, token_text, is_first_token):
        self.root.after(0, self._handle_ollama_token_gui, token_text, is_first_token)

    def _handle_ollama_final_gui(self, error_message=None):
        self.chat_area.config(state='normal') 

        if error_message:
            error_tag_to_apply = "error_tag"
            if not self.first_bot_token_handled and self.chat_area.tag_ranges("bot_placeholder_tag"):
                placeholder_start, _ = self.chat_area.tag_ranges("bot_placeholder_tag")
                self.chat_area.delete(placeholder_start, f"{placeholder_start}+{len('[Sedang memproses...]')}c")
                self.chat_area.insert(INSERT, error_message, error_tag_to_apply) 
            elif not self.first_bot_token_handled:
                 self.chat_area.insert(INSERT, error_message, error_tag_to_apply) 
            else: 
                self.chat_area.insert(END, error_message, error_tag_to_apply)
        
        current_text_content = self.chat_area.get("1.0", "end-1c") 
        if current_text_content and not current_text_content.endswith('\n'):
            self.chat_area.insert(END, "\n")

        # --- MODIFIKASI DI SINI ---
        self.chat_area.insert(END, "\n") # Tambahkan baris kosong sebagai jeda
        # --- SELESAI MODIFIKASI ---

        self.chat_area.insert(END, "Anda: ", "user_prefix_tag") 
        self.chat_area.insert(END, "▸ ") 

        self.chat_area.see(END) 
        self.chat_area.config(state='disabled') 

        self.user_input_entry.config(state='normal')
        self.send_button.config(state='normal')
        
        self.user_input_entry.focus_set() 
        
        self.first_bot_token_handled = False

    def handle_ollama_final(self, error_message=None):
        self.root.after(0, self._handle_ollama_final_gui, error_message)

if __name__ == "__main__":
    app_window = tk.Tk() 
    app_gui = ChatApp(app_window) 
    app_window.mainloop()