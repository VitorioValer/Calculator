#!/usr/bin/env python

from utilities import Equation


def main():
    while True:
        eq = Equation(input('Inform an equation -> '))

        print(f'{eq.equation} = {eq.result}')

        user = input('\nWish to calculate another equation?[y/n] ')

        if user in 'Nn':
            break


if __name__ == '__main__':
    main()
