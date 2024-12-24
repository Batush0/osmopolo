import time
from xml.etree import ElementTree
from datetime import datetime,timezone

class Service:
    @staticmethod
    def createRoot():
        return ElementTree.Element("osm",version="0.6",generator="maxi-labs")

    @staticmethod
    def order(xmlTree: ElementTree.ElementTree):
        root = Service.createRoot()
       
        for key in ["node","way","relation"]:
            for st in sorted(xmlTree.findall(key), key=lambda x: int(x.get("id"))):
                root.append(st)

        return ElementTree.ElementTree(root)
    
    @staticmethod
    def clean(xmlTree: ElementTree.ElementTree):
        root = Service.createRoot()
        if xmlTree.find("bounds") != None:root.append(xmlTree.find("bounds"))

        for key in ["node","way","relation"]:
            seen_ids = set()
            
            for item in xmlTree.findall(key):
                if item.get("id") not in seen_ids:
                    root.append(item)
                    seen_ids.add(item.get("id"))

        return ElementTree.ElementTree(root)            
    
    @staticmethod
    def sign(xmlTree: ElementTree.ElementTree):
        root = Service.createRoot()
        if xmlTree.find("bounds") != None:root.append(xmlTree.find("bounds"))
        changeset = {
            "node":[],
            "way":[],
            "relation":[],
        }

        for key in ["node","way","relation"]:
            for item in xmlTree.findall(key):
                if int(item.get("id")) < 0:
                    newId = str(time.time())[2:14].replace(".","")
                    changeset[key].append({"negative":int(item.get("id")),"new":newId})
                    item.set("id",newId)
                    item.set("version","1")
                    time.sleep(0.1)
                    
                if key == "way":
                    for nd in item.findall("nd"):
                        for chs in changeset["node"]:
                            if chs["negative"] == int(nd.get("ref")):
                                nd.set("ref",chs["new"])
                elif key == "relation":
                    for member in item.findall("member"):
                        for chs in changeset["node"]:
                            if chs["negative"] == int(member.get("ref")):
                                member.set("ref",chs["new"])
                        
                root.append(item)
            
        return ElementTree.ElementTree(root)
    
    @staticmethod
    def makeLatestAllElements(xmlTree:ElementTree.ElementTree):
        root = Service.createRoot()
        if xmlTree.find("bounds") != None:root.append(xmlTree.find("bounds"))
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
       
        for key in ["node","way","relation"]:
            for item in xmlTree.findall(key):
                item.set("timestamp",timestamp)            
                root.append(item)

        return ElementTree.ElementTree(root)
    
    @staticmethod
    def setHeaders(xmlTree:ElementTree.ElementTree):
        root = Service.createRoot()
        root.append(ElementTree.Element("bounds"))

        for key in ["node","way","relation"]:
            for item in xmlTree.findall(key):
                root.append(item)
        
        bbox = Service.findBbox(root.findall("node"))
        print(bbox)
        if(bbox != None):
            bounds = root.find("bounds")
            bounds.set("minlon",str(bbox.get("minlon")))
            bounds.set("minlat",str(bbox.get("minlat")))
            bounds.set("maxlon",str(bbox.get("maxlon")))
            bounds.set("maxlat",str(bbox.get("maxlat")))
        else:
            root.remove("bounds")
        return ElementTree.ElementTree(root)
    
    @staticmethod
    def findBbox(nodes: list[ElementTree.Element]):
        min_lat = float(9999)
        min_lon = float(9999)
        max_lat = float(-9999)
        max_lon = float(-9999)
        
        for node in nodes:
            try:
                min_lat = min(min_lat, float(node.get("lat")))
                min_lon = min(min_lon, float(node.get("lon")))
                max_lat = max(max_lat, float(node.get("lat")))
                max_lon = max(max_lon, float(node.get("lon")))
            except:
                continue;
        
        if(min_lat == float(9999)): return None;
        return {
            "minlon":min_lon,
            "minlat":min_lat,
            "maxlon":max_lon,
            "maxlat":max_lat
        }
    
    @staticmethod
    def readBbox(xmlTree:ElementTree.ElementTree):
        try:
            bounds = xmlTree.find("bounds")
            return f"{float(bounds.get("minlon"))},{float(bounds.get("minlat"))},{float(bounds.get("maxlon"))},{float(bounds.get("maxlat"))}"
        except:
            return "cannot find bbox"
        
    @staticmethod
    def splitWays(xmlTree:ElementTree.ElementTree):
        root = Service.createRoot()
        root.extend(xmlTree.findall("node"));


        for way in xmlTree.findall("way"):
            wayNodes = way.findall("nd") 
            splitNodes = []

            #find nodes that used more than one way
            for nd in wayNodes:
                for compareWay in xmlTree.findall("way"):
                    if(compareWay.get("id") == way.get("id")):continue

                    if any(n.get("ref") == nd.get("ref") for n in compareWay.findall("nd")):
                        splitNodes.append(nd)
                        break
            
            if len(splitNodes) == 0:
                continue

            #order splitables
            orderedSplitNodes = []
            for i in range(len(wayNodes)):
                wayNode = wayNodes[i]
                for splitNode in splitNodes:
                    if(wayNode.get("ref") == splitNode.get("ref")):
                        orderedSplitNodes.append(splitNode)                    

            other_elements = [elem for elem in way if elem.tag != "nd"]
            

            splitedWayNodes = [[]]

            #split way
            for wayNode in wayNodes:
                splitedWayNodes[-1].append(wayNode)
                if any(orderedNode.get("ref") == wayNode.get("ref") for orderedNode in orderedSplitNodes):
                    splitedWayNodes.append([wayNode])
            
            for index,splitedWayElements in enumerate(splitedWayNodes):
                newElement = ElementTree.Element("way")
                newElement.set("id",str(time.time())[2:14].replace(".",""))
                time.sleep(0.1)
                newElement.set("version",str(1))
                newElement.set("timestamp",datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
                if(index == 0):
                    newElement.set("id",str(way.get("id")))
                    newElement.set("version",str(int(way.get("version"))+1))
                newElement.extend(splitedWayElements)
                newElement.extend(other_elements)
                root.append(newElement)

        return ElementTree.ElementTree(root)