"""
This project is licensed under the GNU General Public License v3.0.
See the LICENSE file for details.
"""

import argparse
import json
import textwrap

##################################################

class Iteration:
  def __init__(self, iteration=0, xl=0.0, f_xl=0.0, xr=0.0, f_xr=0.0, xi=0.0, f_xi=0.0, e=0.0):
    self.iteration = iteration
    self.xl = xl
    self.xr = xr
    self.xi = xi
    self.f_xl = f_xl
    self.f_xr = f_xr
    self.f_xi = f_xi
    self.e = e

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

    return parser.parse_args()

##################################################

def main():

    # Load strings from JSON file
    cmd_strings = load_cmd_strings()

    args = initialize_arguments(cmd_strings)

    if args.version:
        print(cmd_strings['message_version'])
    elif args.metodo:
        print("debug", args.metodo)
    elif args.funcion:
        print("debug", args.funcion)

    iteration1 = Iteration(7, 0.1, 1338, 0.2, 67890, 0.125, 0.0007, 0.20)
    print(iteration1.iteration)
    print(iteration1.f_xl)
    print(iteration1.f_xr)
    print(iteration1.f_xi)
    print(iteration1.xl)
    print(iteration1.xr)
    print(iteration1.xi)
    print(iteration1.e)

    iteration2 = Iteration()
    print(iteration2.iteration)
    print(iteration2.f_xl)
    print(iteration2.f_xr)
    print(iteration2.f_xi)
    print(iteration2.xl)
    print(iteration2.xr)
    print(iteration2.xi)
    print(iteration2.e)
    


if __name__ == "__main__":
    main()