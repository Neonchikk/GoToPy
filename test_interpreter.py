from go_lexer import lexer
from go_parser import build_tree
from go_interpreter import Interpreter

def test_interpreter():
    print("\n=== Тест 1: Арифметические операции ===")
    # Простой тест с арифметическими операциями
    code = """
    var x: int = 10;
    var y: int = 5;
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
    """
    
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 2: Условный оператор ===")
    # Тест с условиями
    code = """
    var x: int = 10;
    if (x > 5) {
        print(x);
    } else {
        print(0);
    }
    """
    
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 3: Цикл for ===")
    # Тест с циклом
    code = """
    var i: int = 0;
    for (i = 0; i < 5; i = i + 1) {
        print(i);
    }
    """
    
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 4: Функции ===")
    # Тест с функцией
    code = """
    func add(a: int, b: int): int {
        return a + b;
    }
    
    var result: int = add(5, 3);
    print(result);
    """
    
    ast = build_tree(code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 5: Работа программы из мейн ===")
    correct_code = """
        func factorial(n: int): int {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        var result: int = factorial(5);
        print(result);
        """

    ast = build_tree(correct_code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 6: Работа со строками ===")
    string_code = """
    var name: string = "Иван";
    var age: int = 25;
    var greeting: string = "Привет, " + name + "!";
    print(greeting);
    print("Возраст: " + age);
    """

    ast = build_tree(string_code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 7: Работа с булевыми значениями ===")
    bool_code = """
    var a: bool = true;
    var b: bool = false;
    
    print("a = " + a);  // должно вывести true
    print("b = " + b);  // должно вывести false
    
    print("a && b = " + (a && b));  // должно вывести false
    print("a || b = " + (a || b));  // должно вывести true
    print("!a = " + (!a));      // должно вывести false
    print("!b = " + (!b));      // должно вывести true
    
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

    ast = build_tree(bool_code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 8: Цикл while ===")
    while_code = """
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

    ast = build_tree(while_code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\n=== Тест 9: Комплексный тест ===")
    complex_code = """
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

    ast = build_tree(complex_code)

    interpreter = Interpreter()
    interpreter.interpret(ast)

if __name__ == "__main__":
    test_interpreter() 