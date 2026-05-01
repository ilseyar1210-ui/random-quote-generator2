import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# ===== ПРЕДОПРЕДЕЛЁННЫЕ ЦИТАТЫ =====
PREDEFINED_QUOTES = [
    {"text": "Будь изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "мотивация"},
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "жизнь"},
    {"text": "Не важно, как медленно ты идёшь, главное — не останавливаться.", "author": "Конфуций", "theme": "мотивация"},
    {"text": "Сложнее всего начать действовать, остальное зависит от упорства.", "author": "Пауло Коэльо", "theme": "мотивация"},
    {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "успех"},
    {"text": "Единственный способ сделать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "theme": "работа"},
    {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "theme": "знание"},
    {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "theme": "творчество"},
    {"text": "Кто хочет — ищет способ, кто не хочет — ищет причину.", "author": "Сократ", "theme": "мотивация"},
    {"text": "Лучший способ предсказать будущее — изобрести его.", "author": "Алан Кей", "theme": "будущее"},
    {"text": "Счастье — это когда то, что ты думаешь, говоришь и делаешь, находится в гармонии.", "author": "Махатма Ганди", "theme": "счастье"},
    {"text": "Делай, что можешь, с тем, что имеешь, там, где ты есть.", "author": "Теодор Рузвельт", "theme": "действие"},
    {"text": "Программирование — это искусство говорить компьютеру, что делать.", "author": "Аноним", "theme": "it"},
    {"text": "Простой код — это хороший код.", "author": "Аноним", "theme": "it"},
    {"text": "Лучшее время для посадки дерева было 20 лет назад. Следующее лучшее время — сегодня.", "author": "Китайская пословица", "theme": "мотивация"}
]

HISTORY_FILE = "quotes_history.json"
CUSTOM_FILE = "custom_quotes.json"

class RandomQuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("850x650")
        self.root.resizable(False, False)

        self.history = self.load_history()
        self.custom_quotes = self.load_custom_quotes()

        self.current_filter_author = ""
        self.current_filter_theme = ""

        self.create_widgets()
        self.update_history_display()

    # ===== РАБОТА С JSON =====
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_custom_quotes(self):
        if os.path.exists(CUSTOM_FILE):
            try:
                with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_custom_quotes(self):
        try:
            with open(CUSTOM_FILE, "w", encoding="utf-8") as f:
                json.dump(self.custom_quotes, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить цитаты: {e}")

    def get_all_quotes(self):
        return PREDEFINED_QUOTES + self.custom_quotes

    # ===== ИНТЕРФЕЙС =====
    def create_widgets(self):
        # Рамка генерации
        gen_frame = ttk.LabelFrame(self.root, text="🎲 Генератор цитат", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        self.generate_btn = ttk.Button(gen_frame, text="✨ Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=5)

        self.quote_display = tk.Text(gen_frame, height=4, wrap="word", font=("Arial", 11, "italic"), relief="sunken", borderwidth=1)
        self.quote_display.pack(fill="x", padx=5, pady=5)
        self.quote_display.config(state="disabled")

        # Рамка добавления цитаты
        add_frame = ttk.LabelFrame(self.root, text="📝 Добавить свою цитату", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Текст цитаты:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.quote_text = tk.Text(add_frame, height=3, width=50, wrap="word")
        self.quote_text.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = ttk.Entry(add_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(add_frame, text="Тема:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.theme_entry = ttk.Entry(add_frame, width=20)
        self.theme_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.add_btn = ttk.Button(add_frame, text="➕ Добавить цитату", command=self.add_custom_quote)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация истории", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="По автору:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_author = ttk.Entry(filter_frame, width=20)
        self.filter_author.grid(row=0, column=1, padx=5, pady=5)
        self.filter_author.bind("<KeyRelease>", lambda e: self.apply_filter())

        ttk.Label(filter_frame, text="По теме:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_theme = ttk.Entry(filter_frame, width=20)
        self.filter_theme.grid(row=0, column=3, padx=5, pady=5)
        self.filter_theme.bind("<KeyRelease>", lambda e: self.apply_filter())

        self.reset_btn = ttk.Button(filter_frame, text="🔄 Сбросить", command=self.reset_filter)
        self.reset_btn.grid(row=0, column=4, padx=5, pady=5)

        # Рамка истории
        history_frame = ttk.LabelFrame(self.root, text="📜 История цитат", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("№", "Дата", "Цитата", "Автор", "Тема")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        self.tree.heading("№", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Цитата", text="Цитата")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Тема", text="Тема")

        self.tree.column("№", width=40)
        self.tree.column("Дата", width=150)
        self.tree.column("Цитата", width=350)
        self.tree.column("Автор", width=120)
        self.tree.column("Тема", width=100)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        self.delete_btn = ttk.Button(btn_frame, text="❌ Удалить выбранную", command=self.delete_selected)
        self.delete_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="🗑 Очистить историю", command=self.clear_history)
        self.clear_btn.pack(side="left", padx=5)

    # ===== ГЕНЕРАЦИЯ =====
    def generate_quote(self):
        all_quotes = self.get_all_quotes()
        if not all_quotes:
            messagebox.showwarning("Внимание", "Нет доступных цитат. Добавьте свои!")
            return

        quote = random.choice(all_quotes)

        self.quote_display.config(state="normal")
        self.quote_display.delete(1.0, tk.END)
        self.quote_display.insert(1.0, f"«{quote['text']}»\n\n— {quote['author']} (тема: {quote['theme']})")
        self.quote_display.config(state="disabled")

        self.history.append({
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_history()
        self.update_history_display()

    # ===== ДОБАВЛЕНИЕ (с валидацией) =====
    def add_custom_quote(self):
        text = self.quote_text.get(1.0, tk.END).strip()
        author = self.author_entry.get().strip()
        theme = self.theme_entry.get().strip()

        if not text:
            messagebox.showwarning("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showwarning("Ошибка", "Укажите автора цитаты!")
            return
        if not theme:
            messagebox.showwarning("Ошибка", "Укажите тему цитаты!")
            return

        self.custom_quotes.append({"text": text, "author": author, "theme": theme})
        self.save_custom_quotes()

        self.quote_text.delete(1.0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.theme_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Цитата добавлена!")

    # ===== ФИЛЬТРАЦИЯ =====
    def apply_filter(self):
        self.current_filter_author = self.filter_author.get().strip().lower()
        self.current_filter_theme = self.filter_theme.get().strip().lower()
        self.update_history_display()

    def reset_filter(self):
        self.filter_author.delete(0, tk.END)
        self.filter_theme.delete(0, tk.END)
        self.current_filter_author = ""
        self.current_filter_theme = ""
        self.update_history_display()

    # ===== ОТОБРАЖЕНИЕ =====
    def update_history_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered = self.history.copy()

        if self.current_filter_author:
            filtered = [h for h in filtered if self.current_filter_author in h["author"].lower()]
        if self.current_filter_theme:
            filtered = [h for h in filtered if self.current_filter_theme in h["theme"].lower()]

        filtered.reverse()

        for idx, record in enumerate(filtered, 1):
            display_text = record["text"][:60] + "..." if len(record["text"]) > 60 else record["text"]
            self.tree.insert("", "end", values=(
                idx,
                record["timestamp"],
                display_text,
                record["author"],
                record["theme"]
            ))

        # Обновляем заголовок
        if self.current_filter_author or self.current_filter_theme:
            status = []
            if self.current_filter_author:
                status.append(f"автор={self.current_filter_author}")
            if self.current_filter_theme:
                status.append(f"тема={self.current_filter_theme}")
            self.root.title(f"Random Quote Generator - Фильтр: {', '.join(status)}")
        else:
            self.root.title("Random Quote Generator")

    # ===== УДАЛЕНИЕ =====
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите цитату для удаления")
            return

        item = self.tree.item(selected[0])
        timestamp = item["values"][1]
        text = item["values"][2].replace("...", "")

        for i, record in enumerate(self.history):
            if record["timestamp"] == timestamp and record["text"].startswith(text):
                del self.history[i]
                break

        self.save_history()
        self.update_history_display()
        messagebox.showinfo("Успех", "Цитата удалена из истории")

    def clear_history(self):
        if not self.history:
            messagebox.showinfo("Инфо", "История уже пуста")
            return
        if messagebox.askyesno("Подтверждение", "Очистить всю историю цитат?"):
            self.history.clear()
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomQuoteGenerator(root)
    root.mainloop()
