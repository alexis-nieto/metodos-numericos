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


class Iteration:
    def __init__(self, **kwargs):
        self.iter = kwargs.get('iter', 0)
        self.xl = kwargs.get('xl', 0.0)
        self.f_xl = kwargs.get('f_xl', 0.0)
        self.xr = kwargs.get('xr', 0.0)
        self.f_xr = kwargs.get('f_xr', 0.0)
        self.xi = kwargs.get('xi', 0.0)
        self.f_xi = kwargs.get('f_xi', 0.0)
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
        choices=['biseccion', 'pfalsa'],
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

        # E (-e, --error)
    parser.add_argument(
        cmd_strings['args_option_e_short'],
        cmd_strings['args_option_e_long'],
        help=cmd_strings['args_option_e_info']
    )

    return parser.parse_args()

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

def from_args_get_e(args):
    if args.e:
        return args.e

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

def print_ascii_all_iterations(iterations_list):
    for iteration in range(0, len(iterations_list)):
        print_ascii_iteration(iterations_list, iteration)

'''
@Deprecated
def print_table(iterations):
    # Print header
    header = f"{'Iter':<6} {'xl':<12} {'f(xl)':<12} {'xr':<12} {'f(xr)':<12} {'xi':<12} {'f(xi)':<12} {'e':<12}"
    print(header)
    print("-" * len(header))
    
    # Print each iteration
    for iteration in iterations:
        row = f"{iteration.iter:<6} {iteration.xl:<12.6f} {iteration.f_xl:<12.6f} {iteration.xr:<12.6f} {iteration.f_xr:<12.6f} {iteration.xi:<12.6f} {iteration.f_xi:<12.6f} {iteration.e:<12.6f}"
        print(row)
#'''

def print_table(iterations, significant_figures):
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

##################################################


def main():

    # Load strings from JSON file
    cmd_strings = load_cmd_strings()
    args = initialize_arguments(cmd_strings)

    #########################

    # Print version if called and exit
    if args.version:
        print(cmd_strings['message_version'])
        sys.exit(7)

    #########################

    method = ""
    function = ""
    target_e = 0.0
    xl = 0.0
    xr = 0.0
    xi = 0.0
    f_xl = 0.0
    f_xr = 0.0
    f_xi = 0.0

    # Get data from arguments
    method = str(from_args_get_method(args))
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
    iterations_list = [] # To store the 'Iteration' objects
    significant_figures = int(cmd_strings['significant_figures'])
    e = 0.0
    old_xi = 0.0
    f_xl_f_xi = 0.0

    while True:

        f_xl = expr.subs(x, xl) # Calculate f(Xl)
        f_xr = expr.subs(x, xr) # Calculate f(Xr)

        # Calculate Xi
        if method == "biseccion":
            xi = (xl + xr) / 2.0
        elif method == "pfalsa":
            xi = ((xl)*(f_xr)-(xr)*(f_xl)) / ((f_xr)-(f_xl))

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
            Iteration(
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
    
    #print_ascii_all_iterations(iterations_list)

    print_table(iterations_list, significant_figures)

if __name__ == "__main__":
    main()
