import json
import os
from tkinter import *
from tkinter import ttk, messagebox

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        self.movies = []
        self.load_data()

        # Поля ввода
        fields_frame = LabelFrame(root, text="Информация о фильме", padx=10, pady=10)
        fields_frame.pack(fill="x", padx=10, pady=5)

        Label(fields_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = Entry(fields_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        Label(fields_frame, text="Жанр:").grid(row=0, column=2, sticky="w")
        self.genre_entry = Entry(fields_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=2)

        Label(fields_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w")
        self.year_entry = Entry(fields_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        Label(fields_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w")
        self.rating_entry = Entry(fields_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        add_btn = Button(fields_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=1, column=4, padx=10)

        # Фильтры
        filter_frame = LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w")
        self.filter_genre_entry = Entry(filter_frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)
        
        Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky="w")
        self.filter_year_entry = Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5)
        
        filter_btn = Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=10)
        
        reset_btn = Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("Название", width=250)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except:
                self.movies = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        # Проверка года
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        year = int(year_str)

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        movie = {
            "Название": title,
            "Жанр": genre,
            "Год": year,
            "Рейтинг": rating
        }
        self.movies.append(movie)
        self.save_data()
        self.refresh_table()
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, END)
        self.genre_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.rating_entry.delete(0, END)

    def refresh_table(self, filtered_movies=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        data = filtered_movies if filtered_movies is not None else self.movies
        for movie in data:
            self.tree.insert("", END, values=(
                movie["Название"],
                movie["Жанр"],
                movie["Год"],
                movie["Рейтинг"]
            ))

    def apply_filter(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()

        filtered = self.movies[:]
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["Жанр"].lower()]
        if year_filter:
            if year_filter.isdigit():
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["Год"] == year_int]
            else:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть числом")
                return
        self.refresh_table(filtered)

    def reset_filter(self):
        self.filter_genre_entry.delete(0, END)
        self.filter_year_entry.delete(0, END)
        self.refresh_table()


if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()