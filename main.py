import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library — Личная кинотека")
        self.root.geometry("800x650")
        
        self.file_path = 'movies.json'
        self.movies = []
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # --- 1. ФОРМА ВВОДА ---
        input_frame = tk.LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Год выпуска:").grid(row=2, column=0, sticky="w")
        self.year_entry = tk.Entry(input_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="w")
        self.rating_entry = tk.Entry(input_frame, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=2)

        # 2. Кнопка добавления
        tk.Button(input_frame, text="Добавить фильм", command=self.add_movie, 
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

        # --- 3. СЕКЦИЯ ФИЛЬТРАЦИИ ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(filter_frame, text="По жанру:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="По году:").grid(row=0, column=2)
        self.filter_year = tk.Entry(filter_frame)
        self.filter_year.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Применить", command=self.update_table).grid(row=0, column=4, padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filters).grid(row=0, column=5, padx=5)

        # --- ТАБЛИЦА ВЫВОДА ---
        columns = ("title", "genre", "year", "rating")


self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=100)
        self.tree.column("rating", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    # 5. ПРОВЕРКА КОРРЕКТНОСТИ ВВОДА
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        if not all([title, genre, year_str, rating_str]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            year = int(year_str) # Год должен быть числом
            rating = float(rating_str) # Рейтинг должен быть числом
            if not (0 <= rating <= 10): # Рейтинг от 0 до 10
                raise ValueError("Рейтинг вне диапазона")
        except ValueError:
            messagebox.showerror("Ошибка", "Год — целое число, Рейтинг — от 0 до 10!")
            return

        movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(movie)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        for entry in [self.title_entry, self.genre_entry, self.year_entry, self.rating_entry]:
            entry.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        g_filter = self.filter_genre.get().lower().strip()
        y_filter = self.filter_year.get().strip()

        for m in self.movies:
            # Логика фильтрации
            if g_filter and g_filter not in m['genre'].lower():
                continue
            if y_filter and str(m['year']) != y_filter:
                continue
            
            self.tree.insert("", "end", values=(m['title'], m['genre'], m['year'], m['rating']))

    def reset_filters(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table()

    # 4. СОХРАНЕНИЕ И ЗАГРУЗКА JSON
    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.movies = json.load(f)
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()




