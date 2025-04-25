from go_parser import build_tree
from go_semantic import SemanticAnalyzer


def test_semantic_analysis(code: str, test_name: str):
    print(f"\n{'=' * 50}\nТест: {test_name}\n{'=' * 50}")
    print("Исходный код:")
    print(code.strip())

    print("\nРезультат парсинга:")
    ast = build_tree(code)
    print("\n".join(ast.tree))

    print("\nСемантический анализ:")
    analyzer = SemanticAnalyzer()
    if analyzer.analyze(ast):
        print("✅ Программа семантически корректна")
    else:
        print("❌ Обнаружены ошибки:")
        analyzer.diagnostics.print_errors()


def main():
    # Корректная программа
    correct_code = """
    func factorial(n: int): int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    """

    # Программа с ошибками
    error_code = """
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

    # Тестирование
    test_semantic_analysis(correct_code, "Корректная программа")
    test_semantic_analysis(error_code, "Программа с ошибками")


if __name__ == "__main__":
    main()