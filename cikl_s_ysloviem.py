# # start — означает, с какого числа начинается последовательность (по умолчанию- 0); stop — означает, до какого числа генерируется последовательность чисел (указанное число не включается в диапазон); step — означает, с каким шагом будут расти числа (по умолчанию
# # for i in range(99):
# #     print("доброе утро")

# # number = range(999999)
# # for i in number:
# #     print(i+1, "Класс школы")

# # [print(i)for i in range(1)]

# # for i in range(7, 77, 7):
# #     print(i)
# num = int(input("Введите цифру:"))
# if 1 <= num <= 10:
#     print(f"Таблица умножения для {num}")
# for i in range(1,11):
#     print(f"{num} * {i} = {num*i}")
# else:
#     print("Введите число от 1 до 10")

import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Таблица умножения")
        self.geometry("520x580")
        self.configure(bg="#f5f1e8")
        self.resizable(False, False)

        # Центрируем окно
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 520) // 2
        y = (self.winfo_screenheight() - 580) // 2
        self.geometry(f"+{x}+{y}")

        # Контейнер для экранов
        self.container = tk.Frame(self, bg="#f5f1e8")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Создаём экраны, но НЕ размещаем их сразу
        self.screens = {}
        for S in (WelcomeScreen, InputScreen, TableScreen):
            screen = S(self.container, self)
            self.screens[S.__name__] = screen
            # screen.place(...) — НЕ вызываем здесь!

        # Показываем только приветствие
        self.show_screen("WelcomeScreen")

    def show_screen(self, name):
        """Надёжное переключение экранов с плавной анимацией."""
        # 1. Скрываем ВСЕ экраны
        for s in self.screens.values():
            s.place_forget()

        # 2. Показываем нужный экран
        target = self.screens[name]
        target.place(relx=0, rely=0, relwidth=1, relheight=1)
        target.lift()  # Поднимаем поверх других

        # 3. Плавное появление (если -alpha поддерживается)
        try:
            self.attributes("-alpha", 0.0)

            def fade_in(alpha):
                if alpha >= 1.0:
                    self.attributes("-alpha", 1.0)
                    return
                self.attributes("-alpha", alpha)
                self.after(15, fade_in, alpha + 0.1)

            fade_in(0.0)
        except tk.TclError:
            # Если -alpha не работает, просто показываем экран
            self.attributes("-alpha", 1.0)


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f1e8")
        self.controller = controller

        tk.Label(
            self, text="👋", font=("Segoe UI Emoji", 72),
            bg="#f5f1e8"
        ).pack(pady=(60, 10))

        tk.Label(
            self, text="Таблица умножения",
            font=("Segoe UI", 26, "bold"),
            bg="#f5f1e8", fg="#3a3a3a"
        ).pack(pady=5)

        tk.Label(
            self, text="Простое и красивое приложение\nдля изучения умножения",
            font=("Segoe UI", 12),
            bg="#f5f1e8", fg="#6b6b6b",
            justify="center"
        ).pack(pady=10)

        tk.Button(
            self, text="Начать  →",
            font=("Segoe UI", 13, "bold"),
            bg="#6c8eaf", fg="white",
            activebackground="#567a9a", activeforeground="white",
            bd=0, padx=30, pady=10, cursor="hand2",
            command=lambda: controller.show_screen("InputScreen")
        ).pack(pady=40)


class InputScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f1e8")
        self.controller = controller

        tk.Label(
            self, text="Введите число",
            font=("Segoe UI", 22, "bold"),
            bg="#f5f1e8", fg="#3a3a3a"
        ).pack(pady=(40, 10))

        tk.Label(
            self, text="от 1 до 10",
            font=("Segoe UI", 12),
            bg="#f5f1e8", fg="#6b6b6b"
        ).pack()

        # Поле ввода
        self.entry = tk.Entry(
            self, font=("Segoe UI", 24),
            justify="center", bd=2, relief="solid",
            bg="white", fg="#3a3a3a",
            insertbackground="#3a3a3a"
        )
        self.entry.pack(pady=25, ipady=8, ipadx=20)

        self.error_label = tk.Label(
            self, text="", font=("Segoe UI", 11),
            bg="#f5f1e8", fg="#c0392b"
        )
        self.error_label.pack()

        btn_frame = tk.Frame(self, bg="#f5f1e8")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame, text="← Назад",
            font=("Segoe UI", 11),
            bg="#e0d9c8", fg="#3a3a3a",
            activebackground="#d0c8b5",
            bd=0, padx=15, pady=6, cursor="hand2",
            command=lambda: controller.show_screen("WelcomeScreen")
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="Показать таблицу  →",
            font=("Segoe UI", 11, "bold"),
            bg="#6c8eaf", fg="white",
            activebackground="#567a9a", activeforeground="white",
            bd=0, padx=15, pady=6, cursor="hand2",
            command=self.show_table
        ).pack(side="left", padx=10)

        # Enter = показать таблицу
        self.entry.bind("<Return>", lambda e: self.show_table())

        # Автофокус на поле ввода при показе экрана
        self.bind("<Map>", lambda e: self.entry.focus_set())

    def show_table(self):
        text = self.entry.get().strip()
        if not text.isdigit():
            self.error_label.config(text="Пожалуйста, введите число")
            return
        num = int(text)
        if not (1 <= num <= 10):
            self.error_label.config(text="Число должно быть от 1 до 10")
            return
        self.error_label.config(text="")
        # Передаём число в экран таблицы и переключаемся
        self.controller.screens["TableScreen"].build_table(num)
        self.controller.show_screen("TableScreen")


class TableScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f1e8")
        self.controller = controller

        self.title_label = tk.Label(
            self, text="Таблица умножения",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f1e8", fg="#3a3a3a"
        )
        self.title_label.pack(pady=(20, 10))

        # Таблица
        self.table_frame = tk.Frame(self, bg="#f5f1e8")
        self.table_frame.pack(pady=10, fill="both", expand=True)

        tk.Button(
            self, text="← Назад к вводу",
            font=("Segoe UI", 11),
            bg="#e0d9c8", fg="#3a3a3a",
            activebackground="#d0c8b5",
            bd=0, padx=20, pady=8, cursor="hand2",
            command=lambda: controller.show_screen("InputScreen")
        ).pack(pady=20)

    def build_table(self, num):
        # Очищаем предыдущую таблицу
        for w in self.table_frame.winfo_children():
            w.destroy()

        self.title_label.config(text=f"Таблица умножения для {num}")

        # Заголовок столбцов
        header = tk.Frame(self.table_frame, bg="#6c8eaf")
        header.pack(fill="x", pady=(0, 5))
        for col, txt in enumerate(["×", "Множитель", "Результат"], start=0):
            tk.Label(
                header, text=txt,
                font=("Segoe UI", 12, "bold"),
                bg="#6c8eaf", fg="white",
                width=14, pady=6
            ).grid(row=0, column=col, padx=1)

        # Строки
        for i in range(1, 11):
            bg = "#ffffff" if i % 2 == 1 else "#f0ebdc"
            row = tk.Frame(self.table_frame, bg=bg)
            row.pack(fill="x", pady=1)

            tk.Label(
                row, text=f"{num} × {i} =",
                font=("Segoe UI", 13),
                bg=bg, fg="#3a3a3a",
                width=14, anchor="e", padx=10
            ).pack(side="left")

            tk.Label(
                row, text=str(num * i),
                font=("Segoe UI", 14, "bold"),
                bg=bg, fg="#c0392b",
                width=10, anchor="w", padx=10
            ).pack(side="left")


if __name__ == "__main__":
    app = App()
    app.mainloop()
