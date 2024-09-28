import argparse
from src.parseElements import ParseElements 

class CliController:
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

    
    def clearElements(self,arr):
        seen_ids = set()
        unique_list = []
        
        for item in arr:
            if item['id'] not in seen_ids:
                unique_list.append(item)
                seen_ids.add(item['id'])
            
        return unique_list

    def handleCleanSectionProcess(self,key,elements):
        
        cleanElements = self.clearElements(elements)
        length = len(cleanElements)
        
        print(f"writing {key} data , just {len(elements) - length} rows of duplicated elements deleted!")
        
        mid_index = length // 2
        part1 = cleanElements[0:mid_index] if length % 2 == 0 else cleanElements[0:(mid_index + 1)]
        part2 = cleanElements[mid_index:] if length % 2 == 0 else cleanElements[mid_index+1:]
        del cleanElements
        
        self.__outputFile.write("".join([item["content"] for item in part1]))
        del part1

        print(f"writing {key} process in 1/2")
        
        self.__outputFile.write("".join([item["content"] for item in part2]))
        del part2
        

        
    
    def clean(self):
        parser = ParseElements(self.args.input,self.args.add_args)
        
        self.__outputFile.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' generator='JOSM'>\n")
        
        parser.parse(self.handleCleanSectionProcess)

        self.__outputFile.write("</osm>")

        print("all done!")

    def handleOrderSectionProcess(self,key,elements):
        print(f"ordering {key}")

        sortedElements = sorted(elements, key=lambda x: x["id"])
        length = len(sortedElements)
        mid_index = length // 2
        part1 = sortedElements[0:mid_index] if length % 2 == 0 else sortedElements[0:(mid_index + 1)]
        part2 = sortedElements[mid_index:] if length % 2 == 0 else sortedElements[mid_index+1:]
        del sortedElements
        
        self.__outputFile.write("".join([item["content"] for item in part1]))
        del part1

        self.__outputFile.write("".join([item["content"] for item in part2]))
        del part2


    def order(self):
        parser = ParseElements(self.args.input,self.args.add_args)

        self.__outputFile.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' generator='JOSM'>\n")

        parser.parse(self.handleOrderSectionProcess)

        self.__outputFile.write("</osm>")

        print("all done!")

    def __run__(self):
        if self.args.command == 'clean': self.clean()
        elif self.args.command == 'order': self.order()
        elif self.args.command == 'add-args': self.order()
