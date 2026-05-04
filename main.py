import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("900x650")
        
        self.books = []
        self.load_data()
        
        self.create_widgets()
        self.refresh_display()
    
    def create_widgets(self):
        # Заголовок
        title = ctk.CTkLabel(self.root, text="📚 Book Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=10)
        
        # Форма ввода
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ctk.CTkEntry(input_frame, width=200)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Автор:").grid(row=0, column=2, padx=5, pady=5)
        self.author_entry = ctk.CTkEntry(input_frame, width=150)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = ctk.CTkEntry(input_frame, width=150)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Страниц:").grid(row=1, column=2, padx=5, pady=5)
        self.pages_entry = ctk.CTkEntry(input_frame, width=100)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)
        
        self.add_btn = ctk.CTkButton(input_frame, text="➕ Добавить книгу", command=self.add_book,
                                      fg_color="#4CAF50", hover_color="#45a049")
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Фильтры
        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Фильтр по жанру:").pack(side="left", padx=5)
        self.genre_filter = ctk.CTkComboBox(filter_frame, values=["Все"], width=150, state="readonly")
        self.genre_filter.pack(side="left", padx=5)
        self.genre_filter.set("Все")
        self.genre_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        ctk.CTkLabel(filter_frame, text="Страниц >").pack(side="left", padx=(20, 5))
        self.pages_filter = ctk.CTkEntry(filter_frame, width=80)
        self.pages_filter.pack(side="left", padx=5)
        self.pages_filter.bind('<KeyRelease>', lambda e: self.apply_filters())
        
        self.reset_btn = ctk.CTkButton(filter_frame, text="Сбросить", command=self.clear_filters,
                                        fg_color="#9E9E9E", width=100)
        self.reset_btn.pack(side="left", padx=20)
        
        # Таблица
        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Создаём Treeview через ttk
        from tkinter import ttk
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                  yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("Название", width=250)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=120)
        self.tree.column("Страницы", width=80)
        
        self.tree.pack(fill="both", expand=True)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Кнопки
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.del_btn = ctk.CTkButton(btn_frame, text="🗑 Удалить", command=self.delete_book,
                                      fg_color="#f44336", hover_color="#da190b")
        self.del_btn.pack(side="left", padx=5)
        
        self.save_btn = ctk.CTkButton(btn_frame, text="💾 Сохранить", command=self.save_data,
                                       fg_color="#2196F3")
        self.save_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(btn_frame, text="⚠️ Очистить всё", command=self.clear_all,
                                        fg_color="#FF9800")
        self.clear_btn.pack(side="right", padx=5)
        
        # Статистика
        self.stats_label = ctk.CTkLabel(self.root, text="", font=("Arial", 10))
        self.stats_label.pack(pady=5)
    
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        
        if not all([title, author, genre, pages]):
            from tkinter import messagebox
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        try:
            pages = int(pages)
            if pages <= 0:
                raise ValueError
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", "Страниц должно быть число > 0!")
            return
        
        self.books.append({"title": title, "author": author, "genre": genre, "pages": pages})
        
        self.title_entry.delete(0, "end")
        self.author_entry.delete(0, "end")
        self.genre_entry.delete(0, "end")
        self.pages_entry.delete(0, "end")
        
        self.update_genre_list()
        self.save_data()
        self.refresh_display()
        
        from tkinter import messagebox
        messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")
    
    def update_genre_list(self):
        genres = sorted(set(b["genre"] for b in self.books))
        self.genre_filter.configure(values=["Все"] + genres)
    
    def apply_filters(self):
        filtered = self.books.copy()
        
        genre = self.genre_filter.get()
        if genre and genre != "Все":
            filtered = [b for b in filtered if b["genre"] == genre]
        
        pages_val = self.pages_filter.get().strip()
        if pages_val:
            try:
                pages_num = int(pages_val)
                filtered = [b for b in filtered if b["pages"] > pages_num]
            except:
                pass
        
        self.display_books(filtered)
    
    def display_books(self, books):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for book in books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))
        
        total_pages = sum(b["pages"] for b in books)
        self.stats_label.configure(text=f"📊 Показано: {len(books)} книг | Всего страниц: {total_pages} | Всего в базе: {len(self.books)}")
    
    def refresh_display(self):
        self.update_genre_list()
        self.apply_filters()
    
    def clear_filters(self):
        self.genre_filter.set("Все")
        self.pages_filter.delete(0, "end")
        self.apply_filters()
    
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            from tkinter import messagebox
            messagebox.showwarning("Внимание", "Выберите книгу!")
            return
        
        from tkinter import messagebox
        item = self.tree.item(selected[0])
        title = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить '{title}'?"):
            self.books = [b for b in self.books if b["title"] != title]
            self.save_data()
            self.refresh_display()
    
    def clear_all(self):
        if not self.books:
            return
        from tkinter import messagebox
        if messagebox.askyesno("Внимание", "Удалить ВСЕ книги?"):
            self.books.clear()
            self.save_data()
            self.refresh_display()
    
    def save_data(self):
        try:
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=2)
        except:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", "Не удалось сохранить!")
    
    def load_data(self):
        if os.path.exists("books.json"):
            try:
                with open("books.json", "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except:
                self.books = []

if __name__ == "__main__":
    root = ctk.CTk()
    app = BookTracker(root)
    root.mainloop()
