from go_lexer import lexer
from go_parser import build_tree
from go_interpreter import Interpreter


def test_arithmetic_operations():
    """Тест 1: Арифметические операции"""
    code = """
    var x: int = 10;
    var y: int = 5;
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
    """
    print("\n=== Тест 1: Арифметические операции ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_conditional_statements():
    """Тест 2: Условный оператор"""
    code = """
    var x: int = 10;
    if (x > 5) {
        print(x);
    } else {
        print(0);
    }
    """
    print("\n=== Тест 2: Условный оператор ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_for_loop():
    """Тест 3: Цикл for"""
    code = """
    var i: int = 0;
    for (i = 0; i < 5; i = i + 1) {
        print(i);
    }
    """
    print("\n=== Тест 3: Цикл for ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_functions():
    """Тест 4: Функции"""
    code = """
    func add(a: int, b: int): int {
        return a + b;
    }

    var result: int = add(5, 3);
    print(result);
    """
    print("\n=== Тест 4: Функции ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_factorial():
    """Тест 5: Работа программы из мейн"""
    code = """
    func factorial(n: int): int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    var result: int = factorial(5);
    print(result);
    """
    print("\n=== Тест 5: Работа программы из мейн ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_string_operations():
    """Тест 6: Работа со строками"""
    code = """
    var name: string = "Иван";
    var age: int = 25;
    var greeting: string = "Привет, " + name + "!";
    print(greeting);
    print("Возраст: " + age);
    """
    print("\n=== Тест 6: Работа со строками ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_boolean_operations():
    """Тест 7: Работа с булевыми значениями"""
    code = """
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
    """
    print("\n=== Тест 7: Работа с булевыми значениями ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_while_loop():
    """Тест 8: Цикл while"""
    code = """
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
    """
    print("\n=== Тест 8: Цикл while ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_complex():
    """Тест 9: Комплексный тест"""
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
    """
    print("\n=== Тест 9: Комплексный тест ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_floating_point():
    """Тест 10: Операции с плавающей точкой"""
    code = """
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
    """
    print("\n=== Тест 10: Операции с плавающей точкой ===")
    print("Исходный код:")
    print(code)
    print("Результат интерпретации:")
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)


def test_interpreter():
    """Основная функция для запуска всех тестов"""
    test_arithmetic_operations()
    test_conditional_statements()
    test_for_loop()
    test_functions()
    test_factorial()
    test_string_operations()
    test_boolean_operations()
    test_while_loop()
    test_complex()
    test_floating_point()


if __name__ == "__main__":
    test_interpreter()