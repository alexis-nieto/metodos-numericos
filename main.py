import argparse
import json


def load_cmd_strings(filename='cmd_strings.json'):
    with open(filename, 'r') as f:
        return json.load(f)



def main():

    # Load cmd strings and parse arguments

    cmd_strings = load_strings()
    parser = argparse.ArgumentParser(description=cmd_strings['help_description'])
    parser.parse_args()

    




if __name__ == "__main__":
    main()

