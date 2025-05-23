from go_parser import build_tree
from go_semantic import SemanticAnalyzer

def test_semantic_analysis(code: str, test_name: str):
    """Общая функция для выполнения семантического анализа теста"""
    print(f"\n{'=' * 50}\nТест: {test_name}\n{'=' * 50}")
    print("Исходный код:")
    print(code.strip())

    print("\nСемантический анализ:")
    ast = build_tree(code)
    analyzer = SemanticAnalyzer()
    if analyzer.analyze(ast):
        print("✅ Программа семантически корректна")
    else:
        print("❌ Обнаружены ошибки:")
        analyzer.diagnostics.print_errors()


def test_correct_program():
    """Тест 1: Корректная программа"""
    code = """
    func factorial(n: int): int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    """
    test_semantic_analysis(code, "Корректная программа")


def test_program_with_errors():
    """Тест 2: Программа с ошибками"""
    code = """
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
    """
    test_semantic_analysis(code, "Программа с ошибками")


def main():
    """Основная функция для запуска всех тестов"""
    test_correct_program()
    test_program_with_errors()


if __name__ == "__main__":
    main()