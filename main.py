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
        self.root.geometry("800x600")

        # Список тестов
        self.tests = {
            "AST Print - Простые выражения": test_simple_expressions,
            "AST Print - Арифметические операции": test_arithmetic_operations,
            "AST Print - Условные операторы": test_conditional_statements,
            "AST Print - Функции": test_functions,
            "AST Print - Комплексный тест": test_complex,
            "AST Print - Числа с плавающей точкой": test_floating_point,
            "AST Type - Простые выражения": test_simple_expressions_type,
            "AST Type - Арифметические операции": test_arithmetic_operations_type,
            "AST Type - Условные операторы": test_conditional_statements_type,
            "AST Type - Функции": test_functions_type,
            "AST Type - Комплексный тест": test_complex_type,
            "AST Type - Числа с плавающей точкой": test_floating_point_type,
            "Interpreter - Арифметические операции": test_arithmetic_operations_interpreter,
            "Interpreter - Условные операторы": test_conditional_statements_interpreter,
            "Interpreter - Цикл for": test_for_loop,
            "Interpreter - Функции": test_functions_interpreter,
            "Interpreter - Факториал": test_factorial,
            "Interpreter - Строковые операции": test_string_operations,
            "Interpreter - Булевы операции": test_boolean_operations,
            "Interpreter - Цикл while": test_while_loop,
            "Interpreter - Комплексный тест": test_complex_interpreter,
            "Interpreter - Операции с плавающей точкой": test_floating_point_interpreter,
            "Semantic - Корректная программа": test_correct_program,
            "Semantic - Программа с ошибками": test_program_with_errors,
        }

        # GUI элементы
        self.label = ttk.Label(root, text="Выберите тест:")
        self.label.pack(pady=10)

        self.test_var = tk.StringVar()
        self.test_combobox = ttk.Combobox(root, textvariable=self.test_var, values=list(self.tests.keys()), state="readonly")
        self.test_combobox.pack(pady=5)
        self.test_combobox.bind("<<ComboboxSelected>>", self.run_test)

        self.output_text = scrolledtext.ScrolledText(root, height=30, width=80, wrap=tk.WORD)
        self.output_text.pack(pady=10)

        self.clear_button = ttk.Button(root, text="Очистить поле", command=self.clear_output)
        self.clear_button.pack(pady=5)

    def run_test(self, event=None):
        """Запускает выбранный тест и выводит результат в текстовое поле"""
        test_name = self.test_var.get()
        if not test_name:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Пожалуйста, выберите тест.\n")
            return

        # Перенаправляем stdout в строку
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Выполняем тест
            test_func = self.tests[test_name]
            test_func()
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Ошибка при выполнении теста: {str(e)}\n"
        finally:
            sys.stdout = old_stdout

        # Очищаем поле и выводим результат
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

    def clear_output(self):
        """Очищает текстовое поле"""
        self.output_text.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()