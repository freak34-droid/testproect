import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame_input)
        self.date_entry.grid(row=0, column=1)

        tk.Label(frame_input, text="Температура (°C):").grid(row=0, column=2)
        self.temp_entry = tk.Entry(frame_input)
        self.temp_entry.grid(row=0, column=3)

        tk.Label(frame_input, text="Описание:").grid(row=1, column=0)
        self.desc_entry = tk.Entry(frame_input, width=30)
        self.desc_entry.grid(row=1, column=1, columnspan=3, sticky='w')

        self.precip_var = tk.BooleanVar()
        self.precip_check = tk.Checkbutton(frame_input, text="Осадки", variable=self.precip_var)
        self.precip_check.grid(row=2, column=0)

        # Кнопка добавления
        add_button = tk.Button(self.root, text="Добавить запись", command=self.add_record)
        add_button.pack(pady=5)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=("date", "temp", "desc", "precip"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.pack()

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=1)
        tk.Button(filter_frame, text="Фильтр", command=self.filter_by_date).grid(row=0, column=2)
        tk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data).grid(row=0, column=3)

        tk.Label(filter_frame, text="Показать записи выше °C:").grid(row=1, column=0)
        self.filter_temp_entry = tk.Entry(filter_frame)
        self.filter_temp_entry.grid(row=1, column=1)
        tk.Button(filter_frame, text="Фильтр по температуре", command=self.filter_by_temp).grid(row=1, column=2)

        # Кнопки сохранения/загрузки
        save_btn = tk.Button(self.root, text="Сохранить в JSON", command=self.save_data)
        save_btn.pack(side=tk.LEFT, padx=10, pady=10)

        load_btn = tk.Button(self.root, text="Загрузить из JSON", command=self.load_data)
        load_btn.pack(side=tk.LEFT, padx=10, pady=10)

    def add_record(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precip_var.get()

        # Проверка формата даты
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты")
            return

        # Проверка температуры
        try:
            temperature = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        if not desc:
            messagebox.showerror("Ошибка", "Описание не должно быть пустым")
            return

        record = {
            "date": date_str,
            "temp": temperature,
            "desc": desc,
            "precip": precip
        }
        self.records.append(record)
        self.refresh_table()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    def refresh_table(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if records is None:
            records = self.records
        for rec in records:
            self.tree.insert('', tk.END, values=(
                rec["date"],
                rec["temp"],
                rec["desc"],
                "Да" if rec["precip"] else "Нет"
            ))

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранено", "Данные сохранены в data.json")

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.records = json.load(f)
            self.refresh_table()
        except FileNotFoundError:
            self.records = []

    def filter_by_date(self):
        date_filter = self.filter_date_entry.get()
        try:
            datetime.strptime(date_filter, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты для фильтра")
            return
        filtered = [rec for rec in self.records if rec["date"] == date_filter]
        self.refresh_table(filtered)

    def filter_by_temp(self):
        temp_str = self.filter_temp_entry.get()
        try:
            temp_threshold = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для фильтра по температуре")
            return
        filtered = [rec for rec in self.records if rec["temp"] > temp_threshold]
        self.refresh_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()