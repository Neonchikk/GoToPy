from go_parser import build_tree

sample_code = """
func factorial(n: int): int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

func main(): int {
    var result: int = factorial(5);
    print("Factorial of 5 is", result);
    return 0;
}
"""

if __name__ == "__main__":
    ast = build_tree(sample_code)
    print("\n".join(ast.tree))