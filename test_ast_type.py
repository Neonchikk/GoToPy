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

def test_simple_expressions(code):
    """Тест 1: Простые выражения"""
    print("\n=== Тест 1: Простые выражения ===")
    print("AST с типами:")
    try:
        ast = build_tree(code)
        print_ast_with_types(ast)
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

def test_arithmetic_operations(code):
    """Тест 2: Арифметические операции"""
    print("\n=== Тест 2: Арифметические операции ===")
    print("AST с типами:")
    try:
        ast = build_tree(code)
        print_ast_with_types(ast)
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

def test_conditional_statements(code):
    """Тест 3: Условные операторы"""
    print("\n=== Тест 3: Условные операторы ===")
    print("AST с типами:")
    try:
        ast = build_tree(code)
        print_ast_with_types(ast)
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

def test_functions(code):
    """Тест 4: Функции"""
    print("\n=== Тест 4: Функции ===")
    print("AST с типами:")
    try:
        ast = build_tree(code)
        print_ast_with_types(ast)
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

def test_complex(code):
    """Тест 5: Комплексный тест"""
    print("\n=== Тест 5: Комплексный тест ===")
    print("AST с типами:")
    try:
        ast = build_tree(code)
        if ast:
            print_ast_with_types(ast)
        else:
            print("Ошибка: AST не был построен")
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

def test_floating_point(code):
    """Тест 6: Числа с плавающей точкой"""
    print("\n=== Тест 6: Числа с плавающей точкой ===")
    print("AST с типами:")
    try:
        ast = build_tree(code)
        print_ast_with_types(ast)
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

def test_ast_print(code=None):
    """Основная функция для запуска всех тестов"""
    if code:
        print("Запуск теста с пользовательским кодом")
        test_simple_expressions(code)  # Пример: запуск только одного теста
    else:
        test_simple_expressions("""
    var x: int = 5;
    var y: float = 3.14;
    var z: string = "Hello";
    var b: bool = true;
    """)
        test_arithmetic_operations("""
    var a: int = 10;
    var b: int = 5;
    var c: int = a + b * 2;
    """)
        test_conditional_statements("""
    var x: int = 10;
    if x > 5 {
        var y: int = 20;
    } else {
        var z: int = 30;
    }
    """)
        test_functions("""
    func add(a: int, b: int): int {
        return a + b;
    }
    """)
        test_complex("""
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
    """)
        test_floating_point("""
    var pi: float = 3.14159;
    var temp: float = -25.5;
    var result: float = pi * 2.0 + temp / 3.0;
    """)

if __name__ == "__main__":
    test_ast_print()