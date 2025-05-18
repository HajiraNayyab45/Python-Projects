
def fibonacci_generator(n):
    """
    Generate a Fibonacci sequence of n numbers.

    :param n: Number of terms in the Fibonacci sequence
    :return: A generator yielding Fibonacci numbers

    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Example usage
if __name__ == "__main__":
    terms = int(input("Enter the number of terms for the Fibonacci sequence: "))
    print("Fibonacci sequence:")
    for num in fibonacci_generator(terms):
        print(num, end=" ")