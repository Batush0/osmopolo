from datetime import datetime

class ParseElements:
    def __init__(self,filePath,setAttribute):
        self.__filePath = filePath
        self.__elementData = ""
        self.__elementDataCollected = True
        self.__elementKind = ""
        self.__file = open(self.__filePath,"r+",encoding='utf-8')
        self.__quotesType = ""
        self.__timestamp = ""
        self.__setAttribute = setAttribute
       
    def setAttribute(self):
        editedElement = self.__elementData[0:len(self.__elementKind)+1]
        if " version" not in self.__elementData:editedElement+= f" verison={self.__quotesType}6{self.__quotesType} "
        if " timestamp" not in self.__elementData:editedElement+= self.__timestamp
        return editedElement + self.__elementData[len(self.__elementKind):-1]+">"


    def parse(self):
        self.__file.readline()
        quoteLine = self.__file.readline()
        quoteKeyword = "<osm version="
        self.__quotesType = quoteLine[(quoteLine.find(quoteKeyword) + len(quoteKeyword))]
        self.__timestamp = f" timestamp={self.__quotesType}{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}{self.__quotesType} "

        elements = {
            "node":[],
            "way":[],
            "relation":[]
        }

        idKeyword = f" id={self.__quotesType}"

        while True:
            line = self.__file.readline().strip()

            #collect element data
            if self.__elementDataCollected == True : 
                self.__elementData = line
                self.__elementDataCollected = False

                if "<node " in line:self.__elementKind = "node"
                elif "<way" in line:self.__elementKind = "way"
                elif "<relation" in line:self.__elementKind = "relation"
                elif "</osm>" in line:break
                else:
                    self.__elementData = ""
                    self.__elementDataCollected = True
                    continue

            else : self.__elementData += line

            if self.__getElementCount() == 1 and "/>" in self.__elementData: self.__elementDataCollected = True
            if self.__elementDataCollected == False:
                if "</" + self.__elementKind in self.__elementData:self.__elementDataCollected = True
                else: continue
            
            #progress element
            start = self.__elementData.find(idKeyword) + len(idKeyword)
            end = self.__elementData.find(self.__quotesType, start)
            id = int(self.__elementData[start:end])

            if self.__setAttribute: self.__elementData = self.setAttribute()

            elements[self.__elementKind].append({"id":id,"content":self.__elementData})

        self.__file.close()
        return elements
    
    def __getElementCount(self):
        return self.__elementData.count(">")
    