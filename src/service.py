import time
from xml.etree import ElementTree

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
                        
                root.append(item)
            
        return ElementTree.ElementTree(root)