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

def test_ast_print():
    # Тест 1: Простые выражения
    code1 = """
    var x: int = 5;
    var y: float = 3.14;
    var z: string = "Hello";
    var b: bool = true;
    """
    
    print("\n=== Тест 1: Простые выражения ===")
    ast1 = build_tree(code1)
    print_ast_with_types(ast1)
    
    # Тест 2: Арифметические операции
    code2 = """
    var a: int = 10;
    var b: int = 5;
    var c: int = a + b * 2;
    """
    
    print("\n=== Тест 2: Арифметические операции ===")
    ast2 = build_tree(code2)
    print_ast_with_types(ast2)
    
    # Тест 3: Условные операторы
    code3 = """
    var x: int = 10;
    if x > 5 {
        var y: int = 20;
    } else {
        var z: int = 30;
    }
    """
    
    print("\n=== Тест 3: Условные операторы ===")
    ast3 = build_tree(code3)
    print_ast_with_types(ast3)
    
    # Тест 4: Функции
    code4 = """
    func add(a: int, b: int): int {
        return a + b;
    }
    """
    
    print("\n=== Тест 4: Функции ===")
    ast4 = build_tree(code4)
    print_ast_with_types(ast4)
    
    # Тест 9: Комплексный тест
    code9 = """
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
    
    print("\n=== Тест 9: Комплексный тест ===")
    print("Исходный код:")
    print(code9)
    print("\nAST с типами:")
    try:
        ast9 = build_tree(code9)
        if ast9:
            print_ast_with_types(ast9)
        else:
            print("Ошибка: AST не был построен")
    except Exception as e:
        print(f"Ошибка при построении AST: {str(e)}")

if __name__ == "__main__":
    test_ast_print() 