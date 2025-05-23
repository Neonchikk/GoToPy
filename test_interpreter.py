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

    print("\n=== Тест 5: Работа программы из мейн, тест рекурсии ===")
    correct_code = """
        func factorial(n: int): int {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        print(factorial(5));
        """

    ast = build_tree(correct_code)
    interpreter = Interpreter()
    interpreter.interpret(ast)

if __name__ == "__main__":
    test_interpreter() 