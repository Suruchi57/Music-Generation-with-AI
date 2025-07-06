import tkinter as tk
from tkinter import messagebox
import threading
from preprocess import get_notes
from train import train_model
from generate import generate_music
import pygame

def run_preprocess():
    get_notes()
    messagebox.showinfo("Done", "MIDI data processed.")

def run_training():
    train_model()
    messagebox.showinfo("Done", "Model trained.")

def run_generation():
    midi_file = generate_music()
    messagebox.showinfo("Done", f"Music generated and saved to {midi_file}")
    play_midi(midi_file)

def play_midi(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def main():
    root = tk.Tk()
    root.title("AI Music Generator")
    root.geometry("300x200")

    tk.Button(root, text="1. Preprocess MIDI", command=lambda: threading.Thread(target=run_preprocess).start()).pack(pady=10)
    tk.Button(root, text="2. Train Model", command=lambda: threading.Thread(target=run_training).start()).pack(pady=10)
    tk.Button(root, text="3. Generate Music", command=lambda: threading.Thread(target=run_generation).start()).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
