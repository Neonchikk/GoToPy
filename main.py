import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import io
from test_ast_print import (
    test_simple_expressions,
    test_arithmetic_operations,
    test_conditional_statements,
    test_functions,
    test_complex,
    test_floating_point,
)
from test_ast_type import (
    test_simple_expressions as test_simple_expressions_type,
    test_arithmetic_operations as test_arithmetic_operations_type,
    test_conditional_statements as test_conditional_statements_type,
    test_functions as test_functions_type,
    test_complex as test_complex_type,
    test_floating_point as test_floating_point_type,
)
from test_interpreter import (
    test_arithmetic_operations as test_arithmetic_operations_interpreter,
    test_conditional_statements as test_conditional_statements_interpreter,
    test_for_loop,
    test_functions as test_functions_interpreter,
    test_factorial,
    test_string_operations,
    test_boolean_operations,
    test_while_loop,
    test_complex as test_complex_interpreter,
    test_floating_point as test_floating_point_interpreter,
)
from test_semantic import test_correct_program, test_program_with_errors

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Тесты компилятора")
        self.root.geometry("1000x700")

        # Список тестов с их исходным кодом
        self.tests = {
            "AST Print - Простые выражения": (test_simple_expressions, """
    var x: int = 5;
    var y: float = 3.14;
    var z: string = "Hello";
    var b: bool = true;
    """),
            "AST Print - Арифметические операции": (test_arithmetic_operations, """
    var a: int = 10;
    var b: int = 5;
    var c: int = a + b * 2;
    """),
            "AST Print - Условные операторы": (test_conditional_statements, """
    var x: int = 10;
    if x > 5 {
        var y: int = 20;
    } else {
        var z: int = 30;
    }
    """),
            "AST Print - Функции": (test_functions, """
    func add(a: int, b: int): int {
        return a + b;
    }
    """),
            "AST Print - Комплексный тест": (test_complex, """
    func isPrime(n: int): bool {
        if (n <= 1) {
            return false;
        }
        var i: int = 2;
        while (i * i <= n) {
            if (n % i == 0) {
                return false;
            }
            i = i + 1;
        }
        return true;
    }
    func sumDigits(n: int): int {
        var sum: int = 0;
        var num: int = n;
        while (num > 0) {
            sum = sum + (num % 10);
            num = num / 10;
        }
        return sum;
    }
    func generateSequence(start: int, count: int): string {
        var result: string = "";
        var current: int = start;
        var i: int = 0;
        while (i < count) {
            if (isPrime(current)) {
                result = result + "Простое: " + current;
            } else {
                result = result + "Составное: " + current;
            }
            var sum: int = sumDigits(current);
            if (sum % 2 == 0) {
                result = result + " (четная сумма цифр)";
            } else {
                result = result + " (нечетная сумма цифр)";
            }
            result = result + "\\n";
            current = current + 1;
            i = i + 1;
        }
        return result;
    }
    var start: int = 10;
    var count: int = 5;
    print("Генерируем последовательность из " + count + " чисел, начиная с " + start);
    var sequence: string = generateSequence(start, count);
    print(sequence);
    var max: int = 3;
    var i: int = 1;
    while (i <= max) {
        print("Внешний цикл: " + i);
        var j: int = 1;
        while (j <= i) {
            var product: int = i * j;
            var message: string = "  " + i + " * " + j + " = " + product;
            if (isPrime(product)) {
                print(message + " - простое число");
            } else {
                print(message + " - составное число");
            }
            j = j + 1;
        }
        i = i + 1;
    }
    """),
            "AST Print - Числа с плавающей точкой": (test_floating_point, """
    var pi: float = 3.14159;
    var temp: float = -25.5;
    var result: float = pi * 2.0 + temp / 3.0;
    """),
            "AST Type - Простые выражения": (test_simple_expressions_type, """
    var x: int = 5;
    var y: float = 3.14;
    var z: string = "Hello";
    var b: bool = true;
    """),
            "AST Type - Арифметические операции": (test_arithmetic_operations_type, """
    var a: int = 10;
    var b: int = 5;
    var c: int = a + b * 2;
    """),
            "AST Type - Условные операторы": (test_conditional_statements_type, """
    var x: int = 10;
    if x > 5 {
        var y: int = 20;
    } else {
        var z: int = 30;
    }
    """),
            "AST Type - Функции": (test_functions_type, """
    func add(a: int, b: int): int {
        return a + b;
    }
    """),
            "AST Type - Комплексный тест": (test_complex_type, """
    func isPrime(n: int): bool {
        if (n <= 1) {
            return false;
        }
        var i: int = 2;
        while (i * i <= n) {
            if (n % i == 0) {
                return false;
            }
            i = i + 1;
        }
        return true;
    }
    func sumDigits(n: int): int {
        var sum: int = 0;
        var num: int = n;
        while (num > 0) {
            sum = sum + (num % 10);
            num = num / 10;
        }
        return sum;
    }
    func generateSequence(start: int, count: int): string {
        var result: string = "";
        var current: int = start;
        var i: int = 0;
        while (i < count) {
            if (isPrime(current)) {
                result = result + "Простое: " + current;
            } else {
                result = result + "Составное: " + current;
            }
            var sum: int = sumDigits(current);
            if (sum % 2 == 0) {
                result = result + " (четная сумма цифр)";
            } else {
                result = result + " (нечетная сумма цифр)";
            }
            result = result + "\\n";
            current = current + 1;
            i = i + 1;
        }
        return result;
    }
    var start: int = 10;
    var count: int = 5;
    print("Генерируем последовательность из " + count + " чисел, начиная с " + start);
    var sequence: string = generateSequence(start, count);
    print(sequence);
    var max: int = 3;
    var i: int = 1;
    while (i <= max) {
        print("Внешний цикл: " + i);
        var j: int = 1;
        while (j <= i) {
            var product: int = i * j;
            var message: string = "  " + i + " * " + j + " = " + product;
            if (isPrime(product)) {
                print(message + " - простое число");
            } else {
                print(message + " - составное число");
            }
            j = j + 1;
        }
        i = i + 1;
    }
    """),
            "AST Type - Числа с плавающей точкой": (test_floating_point_type, """
    var pi: float = 3.14159;
    var temp: float = -25.5;
    var result: float = pi * 2.0 + temp / 3.0;
    """),
            "Interpreter - Арифметические операции": (test_arithmetic_operations_interpreter, """
    var x: int = 10;
    var y: int = 5;
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
    """),
            "Interpreter - Условные операторы": (test_conditional_statements_interpreter, """
    var x: int = 10;
    if (x > 5) {
        print(x);
    } else {
        print(0);
    }
    """),
            "Interpreter - Цикл for": (test_for_loop, """
    var i: int = 0;
    for (i = 0; i < 5; i = i + 1) {
        print(i);
    }
    """),
            "Interpreter - Функции": (test_functions_interpreter, """
    func add(a: int, b: int): int {
        return a + b;
    }
    var result: int = add(5, 3);
    print(result);
    """),
            "Interpreter - Факториал": (test_factorial, """
    func factorial(n: int): int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    var result: int = factorial(5);
    print(result);
    """),
            "Interpreter - Строковые операции": (test_string_operations, """
    var name: string = "Иван";
    var age: int = 25;
    var greeting: string = "Привет, " + name + "!";
    print(greeting);
    print("Возраст: " + age);
    """),
            "Interpreter - Булевы операции": (test_boolean_operations, """
    var a: bool = true;
    var b: bool = false;
    print("a = " + a);
    print("b = " + b);
    print("a && b = " + (a && b));
    print("a || b = " + (a || b));
    print("!a = " + (!a));
    print("!b = " + (!b));
    print("Условие a && !b");
    if (a && !b) {
        print("Условие истинно");
    } else {
        print("Условие ложно");
    }
    print("Условие a || b");
    if (a || b) {
        print("Второе условие истинно");
    } else {
        print("Второе условие ложно");
    }
    """),
            "Interpreter - Цикл while": (test_while_loop, """
    var i: int = 0;
    while (i < 5) {
        print("i = " + i);
        i = i + 1;
    }
    var count: int = 10;
    while (count > 0) {
        print("Осталось: " + count);
        count = count - 2;
    }
    """),
            "Interpreter - Комплексный тест": (test_complex_interpreter, """
    func isPrime(n: int): bool {
        if (n <= 1) {
            return false;
        }
        var i: int = 2;
        while (i * i <= n) {
            if (n % i == 0) {
                return false;
            }
            i = i + 1;
        }
        return true;
    }
    func sumDigits(n: int): int {
        var sum: int = 0;
        var num: int = n;
        while (num > 0) {
            sum = sum + (num % 10);
            num = num / 10;
        }
        return sum;
    }
    func generateSequence(start: int, count: int): string {
        var result: string = "";
        var current: int = start;
        var i: int = 0;
        while (i < count) {
            if (isPrime(current)) {
                result = result + "Простое: " + current;
            } else {
                result = result + "Составное: " + current;
            }
            var sum: int = sumDigits(current);
            if (sum % 2 == 0) {
                result = result + " (четная сумма цифр)";
            } else {
                result = result + " (нечетная сумма цифр)";
            }
            if (i < count - 1) {
                result = result + "\\n";
            }
            current = current + 1;
            i = i + 1;
        }
        return result;
    }
    var start: int = 10;
    var count: int = 5;
    print("Генерируем последовательность из " + count + " чисел, начиная с " + start);
    var sequence: string = generateSequence(start, count);
    print(sequence);
    var max: int = 3;
    var i: int = 1;
    while (i <= max) {
        print("Внешний цикл: " + i);
        var j: int = 1;
        while (j <= i) {
            var product: int = i * j;
            var message: string = "  " + i + " * " + j + " = " + product;
            if (isPrime(product)) {
                print(message + " - простое число");
            } else {
                print(message + " - составное число");
            }
            j = j + 1;
        }
        i = i + 1;
    }
    """),
            "Interpreter - Операции с плавающей точкой": (test_floating_point_interpreter, """
    var pi: float = 3.14159;
    var radius: float = 5.5;
    var area: float = pi * radius * radius;
    print("Площадь круга: " + area);
    var temp1: float = 100.0;
    var temp2: float = 32.0;
    var fahrenheit: float = (temp1 * 9.0/5.0) + temp2;
    print("Температура по Фаренгейту: " + fahrenheit);
    var x: float = 10.5;
    var y: float = 3.2;
    print("x + y = " + (x + y));
    print("x - y = " + (x - y));
    print("x * y = " + (x * y));
    print("x / y = " + (x / y));
    var a: int = 5;
    var b: float = 2.5;
    print("a + b = " + (a + b));
    """),
            "Semantic - Корректная программа": (test_correct_program, """
    func factorial(n: int): int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    """),
            "Semantic - Программа с ошибками": (test_program_with_errors, """
    func foo(): int {
        var x: int = 10;
        var x: string = "error";  // Дублирование
        y = 5;  // Необъявленная переменная
        return "string";  // Несоответствие типа
    }
    func bar(a: int, b: float) {
        var res: bool = a + b;  // Несовместимость типов
        if (42) {  // Условие не boolean
            print("Hello");
        }
    }
    """),
        }

        # GUI элементы
        # Панель выбора теста
        self.label = ttk.Label(root, text="Выберите тест:")
        self.label.pack(pady=10)

        self.test_var = tk.StringVar()
        self.test_combobox = ttk.Combobox(root, textvariable=self.test_var, values=list(self.tests.keys()), state="readonly")
        self.test_combobox.pack(pady=5)
        self.test_combobox.bind("<<ComboboxSelected>>", self.load_test_code)

        # Контейнер для двух текстовых полей
        self.text_frame = ttk.Frame(root)
        self.text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Поле для редактирования кода
        self.code_label = ttk.Label(self.text_frame, text="Редактор кода:")
        self.code_label.pack(anchor="w")
        self.code_text = scrolledtext.ScrolledText(self.text_frame, height=15, width=50, wrap=tk.WORD)
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Поле для вывода результатов
        self.output_label = ttk.Label(self.text_frame, text="Результат выполнения:")
        self.output_label.pack(anchor="w")
        self.output_text = scrolledtext.ScrolledText(self.text_frame, height=15, width=50, wrap=tk.WORD)
        self.output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Кнопки
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=5)

        self.start_button = ttk.Button(self.button_frame, text="Старт", command=self.run_test)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Очистить поле", command=self.clear_output)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def load_test_code(self, event=None):
        """Загружает исходный код выбранного теста в редактор"""
        test_name = self.test_var.get()
        if test_name:
            test_func, code = self.tests[test_name]
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, code.strip())
            self.output_text.delete(1.0, tk.END)

    def run_test(self):
        """Запускает выбранный тест с кодом из редактора"""
        test_name = self.test_var.get()
        code = self.code_text.get(1.0, tk.END).strip()
        if not test_name:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Пожалуйста, выберите тест.\n")
            return
        if not code:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Пожалуйста, введите код в редакторе.\n")
            return

        # Перенаправляем stdout в строку
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Выполняем тест с кодом из редактора
            test_func, _ = self.tests[test_name]
            test_func(code)
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Ошибка при выполнении теста: {str(e)}\n"
        finally:
            sys.stdout = old_stdout

        # Выводим результат
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

    def clear_output(self):
        """Очищает поле вывода"""
        self.output_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()