"""
This project is licensed under the GNU General Public License v3.0.
See the LICENSE file for details.
"""

import argparse
import json
import textwrap


def load_cmd_strings(filename='cmd_strings.json'):
    with open(filename, 'r') as f:
        return json.load(f)


def main():

    # Load cmd strings and parse arguments

    cmd_strings = load_cmd_strings()

    #print(cmd_strings['message_version'])

    parser = argparse.ArgumentParser(
        description=cmd_strings['message_version']
        )
    
    # Define Arguments

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

            # Function (-v, --version)
    parser.add_argument(
        cmd_strings['args_option_version_short'],
        cmd_strings['args_option_version_long'],
        action='store_true',
        help=cmd_strings['args_option_version_info']
        )
    
    # Process Arguments

    args = parser.parse_args()

    if args.version:
        print(cmd_strings['message_version'])








if __name__ == "__main__":
    main()