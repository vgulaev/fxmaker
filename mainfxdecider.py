import json
#mydict = {"AccountBalance" : 2,
#          "Orders": [{"ticket" : 1}, {"ticket" : 2}]}
handlefordel = open("C:/Program Files (x86)/MetaTrader 4/experts/files/delete.csv", "w")
handleforcreate = open("C:/Program Files (x86)/MetaTrader 4/experts/files/create.csv", "w")
handleprocess = open("C:/Program Files (x86)/MetaTrader 4/experts/files/proccess.csv", "w")

json_file = open("C:/Program Files (x86)/MetaTrader 4/experts/files/my_data.csv","r")
json_string = json_file.read()
json_file.close() 

mt4data = eval(json_string)

#print(seo_tags)
print(mt4data["AccountBalance"] * 2)
#print(mt4data["Ask"])
print(len(mt4data["Orders"]))

for order in mt4data["Orders"]:
    if (order["OrderType"] > 1):
        handlefordel.write(str(order["OrderTicket"]) + ";")

handlefordel.close()

price = mt4data["Ask"] - 0.01
for n in range(10):
    handleforcreate.write(str(price) + ";1;2;")
    price = price - 0.0001
    print n

handleprocess.write("end")
