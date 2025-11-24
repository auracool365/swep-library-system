import cmath

def quadratic_formula(a, b, c):
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in a quadratic equation.")
    
    # Calculate the discriminant
    discriminant = b**2 - 4*a*c
    
    # Calculate the two solutions using the quadratic formula
    sqrt_discriminant = cmath.sqrt(discriminant)
    
    # Calculate the two solutions using the quadratic formula
    x1 = (-b + sqrt_discriminant) / (2 * a)
    x2 = (-b - sqrt_discriminant) / (2 * a)

    return (x1, x2)


a = 1
b = -3
c = 2
solutions = quadratic_formula(a, b, c)
print(f"The solutions to the equation {a}x^2 + {b}x + {c} = 0 are: {solutions[0]} and {solutions[1]}")