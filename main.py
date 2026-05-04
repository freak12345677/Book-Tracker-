# console_version.py - консольная версия Book Tracker
import json
import os

class BookTrackerConsole:
    def __init__(self):
        self.books = []
        self.load_data()
        self.run()
    
    def run(self):
        while True:
            print("\n" + "="*50)
            print("📚 BOOK TRACKER - Консольная версия")
            print("="*50)
            print("1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Фильтр по жанру")
            print("4. Фильтр по страницам")
            print("5. Удалить книгу")
            print("6. Сохранить и выйти")
            
            choice = input("\nВыберите действие: ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_books(self.books)
            elif choice == "3":
                self.filter_by_genre()
            elif choice == "4":
                self.filter_by_pages()
            elif choice == "5":
                self.delete_book()
            elif choice == "6":
                self.save_data()
                print("Данные сохранены! До свидания!")
                break
            else:
                print("Неверный выбор!")
    
    def add_book(self):
        print("\n--- Добавление книги ---")
        title = input("Название: ").strip()
        author = input("Автор: ").strip()
        genre = input("Жанр: ").strip()
        
        while True:
            try:
                pages = int(input("Страницы: ").strip())
                if pages > 0:
                    break
                else:
                    print("Страницы должны быть > 0!")
            except ValueError:
                print("Введите число!")
        
        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        })
        self.save_data()
        print(f"\n✅ Книга '{title}' добавлена!")
    
    def show_books(self, books):
        if not books:
            print("\n📭 Нет книг в списке!")
            return
        
        print("\n" + "="*80)
        print(f"{'№':<3} {'Название':<30} {'Автор':<20} {'Жанр':<15} {'Стр':<6}")
        print("="*80)
        
        for i, book in enumerate(books, 1):
            print(f"{i:<3} {book['title']:<30} {book['author']:<20} {book['genre']:<15} {book['pages']:<6}")
        
        total_pages = sum(b["pages"] for b in books)
        print("="*80)
        print(f"Всего книг: {len(books)} | Всего страниц: {total_pages}")
    
    def filter_by_genre(self):
        genres = sorted(set(b["genre"] for b in self.books))
        if not genres:
            print("Нет книг для фильтрации!")
            return
        
        print(f"\nДоступные жанры: {', '.join(genres)}")
        genre = input("Введите жанр: ").strip()
        
        filtered = [b for b in self.books if b["genre"].lower() == genre.lower()]
        
        if filtered:
            self.show_books(filtered)
        else:
            print(f"Книги жанра '{genre}' не найдены!")
    
    def filter_by_pages(self):
        try:
            pages = int(input("Минимальное количество страниц: "))
            filtered = [b for b in self.books if b["pages"] > pages]
            
            if filtered:
                self.show_books(filtered)
            else:
                print(f"Нет книг с количеством страниц > {pages}!")
        except ValueError:
            print("Введите число!")
    
    def delete_book(self):
        if not self.books:
            print("Нет книг для удаления!")
            return
        
        self.show_books(self.books)
        try:
            idx = int(input("\nВведите номер книги для удаления: ")) - 1
            if 0 <= idx < len(self.books):
                removed = self.books.pop(idx)
                self.save_data()
                print(f"✅ Книга '{removed['title']}' удалена!")
            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите число!")
    
    def save_data(self):
        try:
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        if os.path.exists("books.json"):
            try:
                with open("books.json", "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except:
                self.books = []

if __name__ == "__main__":
    app = BookTrackerConsole()