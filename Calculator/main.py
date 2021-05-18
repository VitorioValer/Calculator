from utilities import Equation

while True:
    eq = Equation(input('Inform an equation -> '))

    print(f'{eq.equation} = {eq.result}')

    user = input('\nWish to calculate another equation?[y/n] ')

    if user in 'Nn':
        break
