"""
This project is licensed under the GNU General Public License v3.0.
See the LICENSE file for details.
"""

import argparse
import json
import textwrap
import sys
import sympy as sp

##################################################

class IterationBiseccion:
    def __init__(self, **kwargs):
        self.iter = kwargs.get('iter', 0)
        self.xl = kwargs.get('xl', 0.0)
        self.f_xl = kwargs.get('f_xl', 0.0)
        self.xr = kwargs.get('xr', 0.0)
        self.f_xr = kwargs.get('f_xr', 0.0)
        self.xi = kwargs.get('xi', 0.0)
        self.f_xi = kwargs.get('f_xi', 0.0)
        self.e = kwargs.get('e', 0.0)


class IterationPuntoSimple:
    def __init__(self, **kwargs):
        self.iter = kwargs.get('iter', 0)
        self.xi = kwargs.get('xi', 0.0)
        self.g_x = kwargs.get('g_x', 0.0)
        self.e = kwargs.get('e', 0.0)

class IterationNewtonRaphson:
    def __init__(self, **kwargs):
        self.iter = kwargs.get('iter', 0)
        self.xi = kwargs.get('xi', 0.0)
        self.f_x = kwargs.get('f_x', 0.0)
        self.fp_x = kwargs.get('fp_x', 0.0)
        self.e = kwargs.get('e', 0.0)


##################################################

def load_cmd_strings(filename='cmd_strings.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def initialize_arguments(cmd_strings):

    # Load cmd strings and parse arguments

    cmd_strings = load_cmd_strings()

    parser = argparse.ArgumentParser(
        description=cmd_strings['message_version']
    )
    
    # Define Arguments

    # Function (-v, --version)
    parser.add_argument(
        cmd_strings['args_option_version_short'],
        cmd_strings['args_option_version_long'],
        action='store_true',
        help=cmd_strings['args_option_version_info']
    )

    # Method (-m, --method)
    parser.add_argument(
        cmd_strings['args_option_method_short'],
        cmd_strings['args_option_method_long'],
        choices=['biseccion', 'pfalsa', 'psimple', 'newton'],
        help=textwrap.dedent(cmd_strings['args_option_method_info'])
    )

        # Function (-f, --function)
    parser.add_argument(
        cmd_strings['args_option_function_short'],
        cmd_strings['args_option_function_long'],
        help=cmd_strings['args_option_function_info']
    )

        # Xl (-xl, --xl)
    parser.add_argument(
        cmd_strings['args_option_xl_short'],
        cmd_strings['args_option_xl_long'],
        help=cmd_strings['args_option_xl_info']
    )

        # Xr (-xr, --xr)
    parser.add_argument(
        cmd_strings['args_option_xr_short'],
        cmd_strings['args_option_xr_long'],
        help=cmd_strings['args_option_xr_info']
    )

        # Xi (-xi, --xi)
    parser.add_argument(
        cmd_strings['args_option_xi_short'],
        cmd_strings['args_option_xi_long'],
        help=cmd_strings['args_option_xi_info']
    )

        # E (-e, --error)
    parser.add_argument(
        cmd_strings['args_option_e_short'],
        cmd_strings['args_option_e_long'],
        help=cmd_strings['args_option_e_info']
    )

    return parser.parse_args()

#########################

def from_args_get_method(args):
    if args.metodo:
        return args.metodo

def from_args_get_function(args):
    if args.funcion:
        return args.funcion

def from_args_get_xl(args):
    if args.xl:
        return args.xl

def from_args_get_xr(args):
    if args.xr:
        return args.xr

def from_args_get_xi(args):
    if args.xi:
        return args.xi

def from_args_get_e(args):
    if args.e:
        return args.e

#########################

def print_table_biseccion_and_pfalsa(iterations, significant_figures):
    from tabulate import tabulate
    
    data = [[
        it.iter,
        it.xl,
        it.f_xl,
        it.xr,
        it.f_xr,
        it.xi,
        it.f_xi,
        it.e
    ] for it in iterations]
    
    headers = ['Iter', 'xl', 'f(xl)', 'xr', 'f(xr)', 'xi', 'f(xi)', 'e']
    
    # Different table styles: 'grid', 'fancy_grid', 'pipe', 'orgtbl', 'github', 'pretty'
    print(tabulate(data, headers=headers, tablefmt='pipe', floatfmt='{}.{}f'.format('', significant_figures)))

def print_table_psimple(iterations, significant_figures):
    from tabulate import tabulate
    
    data = [[
        it.iter,
        it.xi,
        it.g_x,
        it.e
    ] for it in iterations]
    
    headers = ['Iter', 'xi', 'g(x)', 'e']
    
    print(tabulate(data, headers=headers, tablefmt='pipe', floatfmt='{}.{}f'.format('', significant_figures)))

def print_table_newton_raphson(iterations, significant_figures):
    from tabulate import tabulate
    
    data = [[
        it.iter,
        it.xi,
        it.f_x,
        it.fp_x,
        it.e
    ] for it in iterations]
    
    headers = ['Iter', 'xi', 'f(x)', 'f\'(x)', 'e']
    
    print(tabulate(data, headers=headers, tablefmt='pipe', floatfmt='{}.{}f'.format('', significant_figures)))


''' @Deprecated
def print_ascii_iteration(iterations_list, iter):
    print("\n")
    print("Iteration: ", iterations_list[iter].iter)
    print("Xl: ", iterations_list[iter].xl)
    print("f(Xl): ", iterations_list[iter].f_xl)
    print("Xr: ", iterations_list[iter].xr)
    print("f(Xr): ", iterations_list[iter].f_xr)
    print("Xi: ", iterations_list[iter].xi)
    print("f(Xi): ", iterations_list[iter].f_xi)
    print("E: ", iterations_list[iter].e, "%")
'''

''' @Deprecated
def print_ascii_all_iterations(iterations_list):
    for iteration in range(0, len(iterations_list)):
        print_ascii_iteration(iterations_list, iteration)
'''

##################################################

def run_method_biseccion_and_pfalsa(args, cmd_strings, method):

    function = ""
    target_e = 0.0
    xl = 0.0
    xr = 0.0
    xi = 0.0
    f_xl = 0.0
    f_xr = 0.0
    f_xi = 0.0

    # Get data from arguments
    
    function = str(from_args_get_function(args))
    target_e = float(from_args_get_e(args))
    xl = float(from_args_get_xl(args))
    xr = float(from_args_get_xr(args))

    #########################

    # Sympy initialization
    x = sp.symbols('x') # Create x symbol
    expr = sp.sympify(function) # Parse the equation

    #########################

    current_iteration = 0
    iterations_list = [] # To store the 'IterationBiseccion' objects
    significant_figures = int(cmd_strings['significant_figures'])
    e = 0.0
    old_xi = 0.0
    f_xl_f_xi = 0.0
    method_name_string = ""

    while True:

        f_xl = expr.subs(x, xl) # Calculate f(Xl)
        f_xr = expr.subs(x, xr) # Calculate f(Xr)

        # Calculate Xi

        xi = (xl + xr) / 2.0

        #'''
        # Calculate Xi
        if method == "biseccion":
            xi = (xl + xr) / 2.0
            method_name_string = str(cmd_strings['method_name_biseccion'])
        elif method == "pfalsa":
            xi = ((xl)*(f_xr)-(xr)*(f_xl)) / ((f_xr)-(f_xl))
            method_name_string = str(cmd_strings['method_name_pfalsa'])
        #'''
        
        f_xi = expr.subs(x, xi) # Calculate f(Xi)

        # Calculate E
        if current_iteration > 0:
            e = abs( (xi - old_xi)*(100)/xi )
            '''
            print("Old Xi: ", old_xi)
            print("Xi: ", xi)
            print("Error Calc: ", e,"%")
            print("-----")
            #'''

        # Append current iteration to list
        iterations_list.append(
            IterationBiseccion(
                iter=current_iteration,
                xl=round(xl, significant_figures),
                xr=round(xr, significant_figures),
                xi=round(xi, significant_figures),
                f_xl=round(f_xl, significant_figures),
                f_xr=round(f_xr, significant_figures),
                f_xi=round(f_xi, significant_figures),
                e=round(e, significant_figures)
            )
        )

        if current_iteration > 0:
            if e <= target_e:
                break

        # Evaluaciones Paso 3

        f_xl_f_xi = f_xl * f_xi

        if f_xl_f_xi < 0:
            xr = xi
        elif f_xl_f_xi > 0:
            xl = xi
        elif f_xl_f_xi == 0:
            print("Raiz: ", xi)

        old_xi = xi
        current_iteration += 1

    print()
    print_table_biseccion_and_pfalsa(iterations_list, significant_figures)
    print()
    print("Method: " + method_name_string)
    print("Function: x = " + function)
    print("Iterations: " + str(current_iteration))
    print("Xi = " + str(round(xi, 8)))

    return 1

def run_method_simple_punto_fijo(args, cmd_strings):

    #print("Debug: run_method_simple_punto_fijo")

    function = ""
    target_e = 0.0
    xi = 0.0
    g_x = 0.0
    method_name_string = str(cmd_strings['method_name_psimple'])

    # Get data from arguments
    
    function = str(from_args_get_function(args))
    target_e = float(from_args_get_e(args))
    xi = float(from_args_get_xi(args))

    function = function + " + x" # Add x to the function

    #########################

    # Sympy initialization
    x = sp.symbols('x') # Create x symbol
    expr = sp.sympify(function) # Parse the equation

    #########################

    current_iteration = 0
    iterations_list = [] # To store the 'IterationBiseccion' objects
    significant_figures = int(cmd_strings['significant_figures'])

    # Iteration 0
    g_x = expr.subs(x, xi) # Calculate g(X)
    e = 0.0
    old_xi = xi

    # Append iteration 0 to list
    iterations_list.append(
        IterationPuntoSimple(
            iter=current_iteration,
            xi=round(xi, significant_figures),
            g_x=round(g_x, significant_figures),
            e=round(e, significant_figures)
        )
    )

    current_iteration += 1

    # Iterations >= 1

    while True:

        xi = g_x # Pass old g(X) to new Xi

        g_x = expr.subs(x, xi) # Calculate g(X)
        
        f_xi = expr.subs(x, xi) # Calculate f(Xi)

        # Calculate E
        if current_iteration > 0:
            e = abs( (xi - old_xi)*(100)/xi )

        # Append current iteration to list
        iterations_list.append(
            IterationPuntoSimple(
                iter=current_iteration,
                xi=round(xi, significant_figures),
                g_x=round(g_x, significant_figures),
                e=round(e, significant_figures)
            )
        )

        if current_iteration > 0:
            if e <= target_e:
                break

        old_xi = xi
        current_iteration += 1

    print()
    print_table_psimple(iterations_list, significant_figures)
    print()
    print("Method: " + method_name_string)
    print("Function: x = " + function)
    print("Iterations: " + str(current_iteration))
    print("Xi = " + str(round(xi, 8)))

def run_method_newton_raphson(args, cmd_strings):

    #print("Debug: run_method_newton_raphson")

    function = ""
    function_derivated = ""
    target_e = 0.0
    xi = 0.0
    f_x = 0.0
    fp_x = 0.0
    method_name_string = str(cmd_strings['method_name_newton'])
    #method_name_string = "Newton-Raphson"

    # Get data from arguments
    function = str(from_args_get_function(args))
    target_e = float(from_args_get_e(args))
    xi = float(from_args_get_xi(args))

    #########################

    # Sympy initialization

    x = sp.symbols('x') # Create x symbol

    # f(x)
    f_x_expr = sp.sympify(function) # Parse the equation

    # f'(x)
    function_derivated = sp.diff(function, x) # Derivate function and create string
    fp_x_expr = sp.sympify(function_derivated) # Parse the equation

    #print("Debug: " + "Function: "+ str(function))
    #print("Debug: " + "Function Derivated: "+ str(function_derivated))

    #########################

    current_iteration = 0
    iterations_list = [] # To store the 'IterationBiseccion' objects
    significant_figures = int(cmd_strings['significant_figures'])

    # Iteration 0

    f_x = f_x_expr.subs(x, xi) # Calculate f(X)
    fp_x = fp_x_expr.subs(x, xi) # Calculate f'(X)
    e = 0.0
    old_xi = xi

    #print("Debug: " + str(f_x))
    #print("Debug: " + str(fp_x))

    # Append iteration 0 to list
    iterations_list.append(
        IterationNewtonRaphson(
            iter=current_iteration,
            xi=round(xi, significant_figures),
            f_x=round(f_x, significant_figures),
            fp_x=round(fp_x, significant_figures),
            e=round(e, significant_figures)
        )
    )

    '''
    for i in iterations_list:
        print(i.iter)
        print(i.xi)
        print(i.f_x)
        print(i.fp_x)
        print(i.e)
    #'''

    current_iteration += 1

    # Iterations >= 1

    while True:

        # Calculate new Xi
        xi = old_xi - f_x/fp_x

        f_x = f_x_expr.subs(x, xi) # Calculate f(Xi)
        
        fp_x = fp_x_expr.subs(x, xi) # Calculate f'(Xi)

        # Calculate E
        if current_iteration > 0:
            e = abs( (xi - old_xi)*(100)/xi )

        # Append current iteration to list
        iterations_list.append(
            IterationNewtonRaphson(
                iter=current_iteration,
                xi=round(xi, significant_figures),
                f_x=round(f_x, significant_figures),
                fp_x=round(fp_x, significant_figures),
                e=round(e, significant_figures)
            )
        )

        if current_iteration > 0:
            if e <= target_e:
                break

        old_xi = xi
        current_iteration += 1

    print()
    print_table_newton_raphson(iterations_list, significant_figures)
    print()
    print("Method: " + method_name_string)
    print("Function: x = " + function)
    print("Derivated Function: x = " + str(function_derivated))
    print("Iterations: " + str(current_iteration))
    print("Xi = " + str(round(xi, 8)))

##################################################


def main():

    # Load strings from JSON file

    cmd_strings = load_cmd_strings()
    args = initialize_arguments(cmd_strings)

    #########################

    # Print version if called or if there are no arguments and exit

    if args.version:
        print(cmd_strings['message_version'])
        sys.exit(1)

    #########################

    # Pick method

    method = str(from_args_get_method(args))

    if method == "biseccion":
        run_method_biseccion_and_pfalsa(args, cmd_strings, method)
    elif method == "pfalsa":
        run_method_biseccion_and_pfalsa(args, cmd_strings, method)
    elif method == "psimple":
        run_method_simple_punto_fijo(args, cmd_strings)
    elif method == "newton":
        run_method_newton_raphson(args, cmd_strings)


if __name__ == "__main__":
    main()
