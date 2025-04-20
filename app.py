import tkinter as tk
import random
import asyncio
import json
import os

COLORS = ['red', 'green', 'blue', 'yellow']
SEQUENCE_DELAY = 800  
RECORD_FILE = 'record.json'


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Запомни порядок")

        self.sequence = []
        self.user_sequence = []
        self.round = 0
        self.record = {"name": "", "score": 0}
        self.player_name = ""

        self.load_record()

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Запомни порядок", font=("Helvetica", 20)).pack(pady=10)
        tk.Button(self.root, text="Начать игру", command=self.name_prompt, width=20).pack(pady=5)
        tk.Button(self.root, text="Рекорд", command=self.show_record, width=20).pack(pady=5)
        tk.Button(self.root, text="Выйти", command=self.root.quit, width=20).pack(pady=5)

    def name_prompt(self):
        self.clear_window()

        tk.Label(self.root, text="Введите имя:", font=("Helvetica", 14)).pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Button(self.root, text="Начать", command=self.start_game).pack(pady=5)

    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            return

        self.sequence = []
        self.round = 0
        self.clear_window()
        self.create_game_ui()
        self.root.after(500, self.next_round)

    def create_game_ui(self):
        self.buttons = {}
        self.feedback = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.feedback.pack(pady=5)

        self.round_label = tk.Label(self.root, text=f"Раунд: {self.round}", font=("Helvetica", 14))
        self.round_label.pack(pady=5)

        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10)

        for i, color in enumerate(COLORS):
            btn = tk.Button(grid_frame, bg=color, width=10, height=3,
                            command=lambda c=color: self.handle_click(c))
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.buttons[color] = btn

    def handle_click(self, color):
        self.user_sequence.append(color)
        idx = len(self.user_sequence) - 1

        if self.user_sequence[idx] != self.sequence[idx]:
            self.feedback.config(text="Неверно! Игра окончена.")
            self.check_record()
            self.root.after(2000, self.create_main_menu)
            return

        if len(self.user_sequence) == len(self.sequence):
            self.feedback.config(text="Правильно!")
            self.root.after(1000, self.next_round)

    def next_round(self):
        self.user_sequence = []
        self.round += 1
        self.round_label.config(text=f"Раунд: {self.round}")
        self.sequence.append(random.choice(COLORS))
        self.show_sequence(0)

    def show_sequence(self, index):
        if index < len(self.sequence):
            color = self.sequence[index]
            self.buttons[color].config(relief="sunken")
            self.root.after(SEQUENCE_DELAY, lambda: self.reset_button(color))
            self.root.after(SEQUENCE_DELAY + 100, lambda: self.show_sequence(index + 1))
        else:
            self.feedback.config(text="Ваш ход!")

    def reset_button(self, color):
        self.buttons[color].config(relief="raised")

    def show_record(self):
        self.clear_window()
        tk.Label(self.root, text="Рекорд:", font=("Helvetica", 16)).pack(pady=5)
        name = self.record.get("name", "—")
        score = self.record.get("score", 0)
        tk.Label(self.root, text=f"{name}: {score} раундов").pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.create_main_menu).pack()

    def check_record(self):
        if self.round > self.record.get("score", 0):
            self.record = {"name": self.player_name, "score": self.round - 1}
            self.save_record()

    def load_record(self):
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, 'r', encoding='utf-8') as f:
                self.record = json.load(f)

    def save_record(self):
        with open(RECORD_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.record, f)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
