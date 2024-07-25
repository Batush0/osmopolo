import argparse
from parseElements import ParseElements 

class Osmopolo:
    def __init__(self):
        self.__init_parser__()
        self.__outputFile = open(self.args.output, 'w', encoding="utf-8")
        self.__run__()
    
    def __init_parser__(self):
        parser = argparse.ArgumentParser(description="Welcome to osmopolo cli! This app made for care broken osm files.")

        subParsers = parser.add_subparsers(dest='command')
        
        cleanParser = subParsers.add_parser('clean', help="Cleans id's which has more than one in single file")
        cleanParser.add_argument('--input',"-i", type=str, help="Input files path")
        cleanParser.add_argument('--output',"-o", type=str, help="Output files path")
        cleanParser.add_argument('--add-args', action="store_true" , help="Append necessary arguments to elements")

        orderParser = subParsers.add_parser('order', help="Orders elements in correct way")
        orderParser.add_argument('--input',"-i", type=str, help="Input files path")
        orderParser.add_argument('--output',"-o", type=str, help="Output files path")
        orderParser.add_argument('--add-args', action="store_true" , help="Append necessary arguments to elements")

        self.args = parser.parse_args()
    
    def clean(self):
        parser = ParseElements(self.args.input,self.args.add_args)
        elements = parser.parse()

        def clearElements(arr):
            seen_ids = set()
            unique_list = []
            
            for item in arr:
                if item['id'] not in seen_ids:
                    unique_list.append(item)
                    seen_ids.add(item['id'])
            
            return unique_list

        cleanNode = clearElements(elements["node"])
        print("node")
        print("- elements leng : ",len(elements["node"]))
        print("- cleaned elements leng : ",len(cleanNode))

        cleanWay = clearElements(elements["way"])
        print("way")
        print("- elements leng : ",len(elements["way"]))
        print("- cleaned elements leng : ",len(cleanWay))

        cleanRelation = clearElements(elements["relation"])
        print("relation")
        print("- elements leng : ",len(elements["relation"]))
        print("- cleaned elements leng : ",len(cleanRelation))

        print("write process started")

        self.__outputFile.write("<?xml version='1.0' encoding='UTF-8'?><osm version='0.6' generator='JOSM'>")
        self.__outputFile.write("".join([item["content"] for item in cleanNode]))
        self.__outputFile.write("".join([item["content"] for item in cleanWay]))
        self.__outputFile.write("".join([item["content"] for item in cleanRelation]))
        self.__outputFile.write("</osm>")

        print("all done!")

    def order(self):
        parser = ParseElements(self.args.input,self.args.add_args)
        elements = parser.parse()

        print("write process started")

        self.__outputFile.write("<?xml version='1.0' encoding='UTF-8'?><osm version='0.6' generator='JOSM'>")
        self.__outputFile.write("".join(element["content"] for element in sorted(elements["node"], key=lambda x: x["id"])))
        self.__outputFile.write("".join(element["content"] for element in sorted(elements["way"], key=lambda x: x["id"])))
        self.__outputFile.write("".join(element["content"] for element in sorted(elements["relation"], key=lambda x: x["id"])))
        self.__outputFile.write("</osm>")

        print("all done!")

    def __run__(self):
        if self.args.command == 'clean': self.clean()
        elif self.args.command == 'order': self.order()
        elif self.args.command == 'add-args': self.order()

Osmopolo()