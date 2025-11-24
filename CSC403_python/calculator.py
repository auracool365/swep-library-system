def calculator():
    print("Calculator Implementation")
    print("Available operations:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    while True:
        choice = input("Enter operation (using the number): 1( + ), 2( - ), 3( * ), 4( / ): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            match choice:
                case '1':
                    result = num1 + num2
                    operation = '+'
                case '2':
                    result = num1 - num2
                    operation = '-'
                case '3':
                    result = num1 * num2
                    operation = 'x'
                case '4':
                    if num2 != 0:
                        result = num1 / num2
                        operation = '/'
                    else:
                        print("Error: Division by zero is not allowed.")
                        continue

            print(f"{num1} {operation} {num2} = {result}")


            next_calculation = input("Do you want to perform another calculation? (yes/no): ")
            if next_calculation.lower() != 'yes':
                break
        else:
            print("Invalid Input")

calculator()