import json
mydict = {"AccountBalance" : 2,
          "Orders": [{"ticket" : 1}, {"ticket" : 2}]}
handle = open("my.json", "w")
handle.write(str(mydict))
handle.close()

#json_file = open("my.json","r")
#json_string = json_file.read()
#json_file.close() 

#seo_tags = eval(json_string)

#print(seo_tags)
#print(seo_tags["abc"])