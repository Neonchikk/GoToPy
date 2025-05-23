from go_parser import build_tree
from go_ast import AstNode


def print_ast_with_types(node: AstNode, indent=0):
    """Рекурсивно выводит дерево AST с типами."""
    if node is None:
        print("  " * indent + "None")
        return
    print("  " * indent + f"{str(node)} (type: {getattr(node, 'node_type', 'unknown')})")
    for child in node.childs:
        print_ast_with_types(child, indent + 1)


def test_simple_expressions():
    """Тест 1: Простые выражения"""
    code = """
    var x: int = 5;
    var y: float = 3.14;
    var z: string = "Hello";
    var b: bool = true;
    """
    print("\n=== Тест 1: Простые выражения ===")
    print("Исходный код:")
    print(code)
    print("AST с типами:")
    ast = build_tree(code)
    print_ast_with_types(ast)


def test_arithmetic_operations():
    """Тест 2: Арифметические операции"""
    code = """
    var a: int = 10;
    var b: int = 5;
    var c: int = a + b * 2;
    """
    print("\n=== Тест 2: Арифметические операции ===")
    print("Исходный код:")
    print(code)
    print("AST с типами:")
    ast = build_tree(code)
    print_ast_with_types(ast)


def test_conditional_statements():
    """Тест 3: Условные операторы"""
    code = """
    var x: int = 10;
    if x > 5 {
        var y: int = 20;
    } else {
        var z: int = 30;
    }
    """
    print("\n=== Тест 3: Условные операторы ===")
    print("Исходный код:")
    print(code)
    print("AST с типами:")
    ast = build_tree(code)
    print_ast_with_types(ast)


def test_functions():
    """Тест 4: Функции"""
    code = """
    func add(a: int, b: int): int {
        return a + b;
    }
    """
    print("\n=== Тест 4: Функции ===")
    print("Исходный код:")
    print(code)
    print("AST с типами:")
    ast = build_tree(code)
    print_ast_with_types(ast)


def test_complex():
    """Тест 5: Комплексный тест"""
    code = """
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
    """
    print("\n=== Тест 5: Комплексный тест ===")
    print("Исходный код:")
    print(code)
    print("AST с типами:")
    try:
        ast = build_tree(code)
        if ast:
            print_ast_with_types(ast)
        else:
            print("Ошибка: AST не был построен")
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")


def test_floating_point():
    """Тест 6: Числа с плавающей точкой"""
    code = """
    var pi: float = 3.14159;
    var temp: float = -25.5;
    var result: float = pi * 2.0 + temp / 3.0;
    """
    print("\n=== Тест 6: Числа с плавающей точкой ===")
    print("Исходный код:")
    print(code)
    print("AST с типами:")
    ast = build_tree(code)
    print_ast_with_types(ast)


def test_ast_print():
    """Основная функция для запуска всех тестов"""
    test_simple_expressions()
    test_arithmetic_operations()
    test_conditional_statements()
    test_functions()
    test_complex()
    test_floating_point()


if __name__ == "__main__":
    test_ast_print()