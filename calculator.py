# Using class for inheritance purpose
class BigNumber:
    def __init__(self, value):
        if isinstance(value, str) and value.isdigit():
            self.digits = [int(d) for d in value][::-1]  # Store digits in reverse order
        elif isinstance(value, int) and value >= 0:
            self.digits = [int(d) for d in str(value)][::-1]
        else:
            raise ValueError("Only non-negative integers are supported.") # Handle negative number errors
    
    def __str__(self):
        return ''.join(map(str, self.digits[::-1]))

    def __add__(self, other):
        max_len = max(len(self.digits), len(other.digits))
        result = []
        carry = 0
        
        for i in range(max_len):
            digit1 = self.digits[i] if i < len(self.digits) else 0
            digit2 = other.digits[i] if i < len(other.digits) else 0
            total = digit1 + digit2 + carry
            carry, remainder = divmod(total, 10)
            result.append(remainder)
        
        if carry:
            result.append(carry)
        
        return BigNumber(''.join(map(str, result[::-1])))

    def __sub__(self, other):
        if self < other:
            raise ValueError("Negative results are not supported.")
        result = []
        borrow = 0

        for i in range(len(self.digits)):
            digit1 = self.digits[i]
            digit2 = other.digits[i] if i < len(other.digits) else 0
            diff = digit1 - digit2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.append(diff)
        
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        
        return BigNumber(''.join(map(str, result[::-1])))

    def __mul__(self, other):
        result = BigNumber(0)
        for i, digit1 in enumerate(self.digits):
            carry = 0
            partial_result = [0] * i  # Offset for the current place value
            for digit2 in other.digits:
                product = digit1 * digit2 + carry
                carry, remainder = divmod(product, 10)
                partial_result.append(remainder)
            if carry:
                partial_result.append(carry)
            result += BigNumber(''.join(map(str, partial_result[::-1])))
        
        return result

    def __lt__(self, other):
        if len(self.digits) != len(other.digits):
            return len(self.digits) < len(other.digits)
        return self.digits[::-1] < other.digits[::-1]

    def __eq__(self, other):
        return self.digits == other.digits

    def factorial(self):
        result = BigNumber(1)
        current = BigNumber(1)
        while current <= self:
            result *= current
            current += BigNumber(1)
        return result


def parse_input(expression):
    """Basic parser for a calculator expression."""
    tokens = expression.split()
    if len(tokens) == 3:
        num1, op, num2 = tokens
        num1 = BigNumber(num1)
        num2 = BigNumber(num2)
        return num1, op, num2
    elif len(tokens) == 2 and tokens[1] == "!":
        num = BigNumber(tokens[0])
        return num, "!"
    else:
        raise ValueError("Invalid input") # Error handling ->not supported inputs


def calculate(num1, op, num2=None):
    if op == "+":
        return num1+num2 # addition
    elif op == "-":
        return num1-num2 # sub
    elif op == "*":
        return num1*num2 # multi
    elif op == "!":
        return num1.factorial() # factorial
    else:
        raise ValueError(f"Unknown operator: {op}")


def repl():
    print("\nWelcome to the mySimple Calculator!")
    print("Supported operations like:\n\n3 + 3,\n3 - 3,\n3 * 3,\n4 ! factorial not working,\n ")
    print("Type 'exit' to quit.\n")
    while True:
        user_input = input(">")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        try:
            parsed = parse_input(user_input)
            if len(parsed) == 3:
                num1, op, num2 = parsed
                result = calculate(num1, op, num2)
            elif len(parsed) == 2:
                num1, op = parsed
                result = calculate(num1, op)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    repl()
