import argparse
from xml.etree import ElementTree
from src.service import Service

class CliController:
    def __init__(self):
        self.__init_parser__()
        self.route()
    
    def __init_parser__(self):
        parser = argparse.ArgumentParser(description="Welcome to osmopolo cli! This app made for care broken osm files.")

        command_descriptions = {
            'clean': "Cleans IDs which have more than one in a single file.",
            'order': "Puts elements in correct order according to their id.",
            'sign': "Signs new elements with negative ids by giving them positive uniq ids"
        }

        commands_help = "\n".join([f"{cmd}: {desc}" for cmd, desc in command_descriptions.items()])
        parser.add_argument('--commands', nargs='+', choices=command_descriptions.keys(),
                            help=f"List of commands to execute in order. Available commands:\n\n{commands_help}")

        parser.add_argument('--input',"-i", type=str, help="Input files path")
        parser.add_argument('--output',"-o", type=str, help="Output files path")
        parser.add_argument('--add-args', action="store_true" , help="Append necessary arguments to elements")

        self.args = parser.parse_args()

        if not self.args.commands:
            print("err : You should give commands \n")
            exit(1)
        if not self.args.input:
            print("err : You should give input file \n")
            exit(1)
        if not self.args.output:
            print("err : You should output file \n")
            exit(1)

    
    
    def route(self):
        elementTree = ElementTree.parse(self.args.input)

        for command in self.args.commands:
            match command:
                case "clean":
                    elementTree = Service.clean(elementTree)
                    continue
                case "order":
                    elementTree = Service.order(elementTree)
                    continue
                case "sign":
                    elementTree = Service.sign(elementTree)
                    continue

        elementTree.write(self.args.output)
