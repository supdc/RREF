import random

def row_echelon_form(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    for i in range(min(rows, cols)):  # Ensure we don't go out of bounds
        # Find the pivot
        if matrix[i][i] == 0:
            for j in range(i+1, rows):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]  # Swap rows
                    break
        
        # Normalize pivot row
        pivot = matrix[i][i]
        if pivot != 0:
            matrix[i] = [x / pivot for x in matrix[i]]
        
        # Eliminate rows below
        for j in range(i+1, rows):
            factor = matrix[j][i]
            matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(cols)]
    
    return matrix

def reduced_row_echelon_form(matrix):
    # First convert to row echelon form
    matrix = row_echelon_form(matrix)
    lenrow = len(matrix)
    lencol = len(matrix[0])
    row = 0
    col = 0
    while row < lenrow and col < lencol:
        # หา pivot row
        j = row
        while j < lenrow and matrix[j][col] == 0:
            j += 1
        # ถ้าหาไม่เจอแถวที่ไม่เป็น 0 เลื่อนไป column ถัดไป
        if j == lenrow:
            col += 1
            continue
        
        # ถ้าเจอแถวที่ไม่เป็น 0 ให้สลับแถว
        if j != row:
            matrix[row], matrix[j] = matrix[j], matrix[row]
        
        # ปรับ pivot row ให้ pivot เป็น 1
        leader = matrix[row][col]
        matrix[row] = [inrow / leader for inrow in matrix[row]]
        
        # กำจัดค่าอื่นๆ ใน column เดียวกัน
        for i in range(lenrow):
            if i != row:
                multiplier = matrix[i][col]
                matrix[i] = [inrow - multiplier * inlead for inrow, inlead in zip(matrix[i], matrix[row])]
        
        # ไปที่ row และ col ถัดไป
        row += 1
        col += 1


    for i in range(lenrow):
        for j in range(lencol):
            if matrix[i][j] < 0.0001 and matrix[i][j] > -0.0001:
                matrix[i][j] = 0.0
            else:
                matrix[i][j] = round(matrix[i][j], 4)

    return matrix

def is_consistent(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Check for inconsistency
    for i in range(rows):
        # If a row has all 0s in the coefficient part but the constant part is non-zero
        if all(matrix[i][j] == 0 for j in range(cols-1)) and matrix[i][-1] != 0:
            return False  # Inconsistent
    return True  # Consistent

def identify_variables(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    lead_vars = []
    free_vars = list(range(1, cols))  # Start with all variables as free variables (excluding the constant column)
    
    for i in range(rows):
        for j in range(cols-1):
            if matrix[i][j] != 0:
                lead_vars.append(j + 1)  # Adjust lead variable to start from 1
                if j + 1 in free_vars:
                    free_vars.remove(j + 1)  # Remove from free variables list
                break
    
    # Add remaining free variables (if any) that are not in lead_vars
    for col in range(1, cols):
        if col not in lead_vars and col not in free_vars:
            free_vars.append(col)

    return lead_vars, free_vars

def extract_linear_equations(matrix, lead_vars, free_vars):
    rows = len(matrix)
    cols = len(matrix[0])
    equations = []
    
    for i in range(rows):
        equation = []
        constant = matrix[i][-1]  # Constant term (the right-hand side of the equation)
        
        # Create the equation in terms of the lead variables
        for j in range(cols - 1):
            if matrix[i][j] != 0:
                equation.append(f"{matrix[i][j]:.2f}*x{j+1}")
        
        # If there are any terms in the equation, format it as a string
        if equation:
            equation_str = " + ".join(equation) + f" = {constant:.2f}"
            equations.append(equation_str)
    
    return equations

def solve_system(matrix, lead_vars, free_vars):
    rows = len(matrix)
    cols = len(matrix[0])
    solutions = {}
    
    # Initialize free variables as parameters (e.g., t1, t2, t3, ...)
    for i, free_var in enumerate(free_vars):
        solutions[f"x{free_var}"] = f"t{i+1}"  # Assign free variables as t1, t2, t3, ...

    # Solve for lead variables in terms of free variables
    for i in range(len(lead_vars)):
        equation = matrix[i][:-1]  # Coefficients of the variables
        constant = matrix[i][-1]   # Constant term (right-hand side)
        lead_var = lead_vars[i]    # The lead variable for this row
        
        # Solve for the lead variable
        solution = constant
        for j in range(cols - 1):
            if j + 1 != lead_var and matrix[i][j] != 0:
                # Check if it's a free variable (parameter) and use it without conversion to float
                term = solutions.get(f"x{j+1}", None)
                if term and "t" in term:
                    solution -= matrix[i][j] * 1  # Keep it symbolic (e.g., t1)
                else:
                    solution -= matrix[i][j] * float(term if term is not None else 0)
        
        solutions[f"x{lead_var}"] = round(solution, 2)  # Round the solution to 2 decimal places
    
    return solutions


# Take matrix input from user
n = int(input("Enter the number of rows (n): "))
m = int(input("Enter the number of columns (m): "))
matrix = []

print("Enter the elements of the matrix row by row:")
for i in range(n):
    row = list(map(float, input(f"Row {i+1}: ").split()))
    matrix.append(row)

# matrix = [[0 for x in range(m)] for y in range(n)] 
# for i in range(n):
#     j = 0
#     for j in range(m):
#         matrix[i][j] = random.randrange(0,10)

print("\nMatrix Before Converting:")
for row in matrix:
    print(row)

# Convert to reduced row echelon form
result = reduced_row_echelon_form(matrix)

print("\nAfter Converting to Reduced Row Echelon Form:")
for row in result:
    print(row)

# Check consistency
if is_consistent(result):
    print("\nThe system is Consistent.")
else:
    print("\nThe system is Inconsistent.")

if is_consistent(result):
    # Identify lead and free variables
    lead_vars, free_vars = identify_variables(result)

    print(f"\nLead Variables (Pivot Columns): {lead_vars}")
    print(f"Free Variables: {free_vars}")

    # Extract and display linear equations
    equations = extract_linear_equations(result, lead_vars, free_vars)

    print("\nThe Linear Equations are:")
    for eq in equations:
        print(eq)

    # Solve the system for each variable
    solutions = solve_system(result, lead_vars, free_vars)

    print("\nThe Solutions are:")
    for var, value in solutions.items():
        print(f"{var} = {'1' if isinstance(value, str) else f'{value:.2f}'}")


else:
    print("\nCannot Solve.")
