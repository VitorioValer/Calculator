def operation(n1, n2, op):
    """
    Takes two numbers and an operator, and performs the correct mathematical
    operation.

    :param n1: number on the left side of the operator.
    :param n2: number on the right side of the operator.
    :param op: operator

    :return: result of the operation.
    """

    n1 = float(n1)
    n2 = float(n2)

    if op == '*':
        return n1 * n2

    elif op == '/':
        return n1 / n2

    elif op == '+':
        return n1 + n2

    elif op == '-':
        return n1 - n2

    elif op == '^':
        return n1**n2

    else:
        raise ValueError


def factorial(num):
    """
    Calculates the factorial of a number.

    :param num: number to be calculated.
    :return: factorial of num.
    """
    if num == 1:
        return 1

    else:
        return num * factorial(num - 1)


class Equation:
    """
    Equation Object formats and solves an equation passed as a parameter.

    :param equation: string of an equation
    """

    def __init__(self, equation):
        self.equation = equation
        self.fixer()

        self.result = self.solver()

    def fixer(self):
        """
        Formats the main equation in the correct way for later calculations.

        :return: None
        """

        char_list = ('^', '*', '/', '+', '-')

        self.equation = ''.join(self.equation.split())

        if '**' in self.equation:
            self.equation = self.equation.replace('**', '^')

        for char in char_list:
            if char in self.equation:
                self.equation = self.equation.split(char)

                char = f' {char} ' if char != '^' else f'{char}'
                self.equation = char.join(self.equation)

        self.equation = self.equation.split()

        for pos, char in enumerate(self.equation):
            prev_char = self.equation[pos - 1][-1]

            if char == '-':
                if pos == 0 or ')' in prev_char or \
                                not prev_char.isnumeric():

                    neg_num = char + self.equation[pos + 1]

                    self.equation.pop(pos + 1)
                    self.equation.pop(pos)

                    if '(' in prev_char:
                        neg_num = f'{prev_char}{neg_num}'
                        self.equation.pop(pos - 1)

                        self.equation.insert(pos - 1, neg_num)

                    else:
                        self.equation.insert(pos, neg_num)

        self.equation = ' '.join(self.equation)

    def find_parenthesis(self):
        """
        Method which iterates through the main equation looking for
        parenthesis, if found, it separates its content in an inner equation,
        creating a new Equation object with it, and then replaces the inner
        equation and its parenthesis by its result in the main equation.

        :return: main equation with parenthesis and inner content replaced by
        it's solution.
        """

        eq = [char for char in self.equation]

        for pos, char in enumerate(eq):
            if '(' in char:
                inner_eq = ''
                inner_par = 0
                eq.pop(pos)

                for inner_char in eq[pos:]:

                    if '(' in inner_char:
                        inner_par += 1

                    if ')' in inner_char:
                        if inner_par == 0:
                            eq.pop(pos)
                            break

                        else:
                            inner_par -= 1

                    inner_eq += inner_char
                    eq.pop(pos)

                inner_eq = Equation(inner_eq)

                eq.insert(pos, inner_eq.result)

        return ''.join(eq)

    def solver(self):
        """
        Method responsible for solving the main equation.

        :return: Result for the informed equation.
        """

        result = self.find_parenthesis()
        result = result.split()

        while len(result) > 1 \
                or any(['!' in char for char in result]) \
                or any(['^' in char for char in result]):

            while any(['!' in char for char in result]):
                result = self.calculate('!', result)

            while any(['^' in char for char in result]):
                result = self.calculate('^', result)

            while '*' in result or '/' in result:
                result = self.calculate('*/', result)

            result = self.calculate('+-', result)

        return result[0]

    @staticmethod
    def calculate(operator, equation):
        """
        Method which takes an equation and loops through it in search of
        specific operators to perform the correct operation.

        :param operator: string containing all the operations characters,
        with no spaces, which the method should search for.
        :param equation: equation in which the operation is being performed.

        :return: the equation with the result of the operation in the correct
        place.
        """

        for pos, char in enumerate(equation):
            if char in operator or operator in char:
                if operator == '!':
                    char = int(char[:-1])
                    result = factorial(char)
                    equation.pop(pos)
                    equation.insert(pos, str(result))

                elif operator == '^':
                    char = char.split('^')
                    result = operation(
                        char[0],
                        char[1],
                        operator
                    )
                    equation.pop(pos)
                    equation.insert(pos, str(result))

                else:
                    result = operation(
                        equation[pos - 1],
                        equation[pos + 1],
                        char
                    )

                    equation.pop(pos + 1)
                    equation.pop(pos)
                    equation.pop(pos - 1)

                    equation.insert(pos - 1, str(result))

        return equation


if __name__ == '__main__':
    eq = Equation(input('Enter an equation -> '))

    print(f'{eq.equation} = {eq.result}')
