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

prices = [o["OrderOpenPrice"] for o in mt4data["Orders"] if (o["OrderType"] == 0)]

margin = [o["OrderOpenPrice"] * o["OrderLots"] for o in mt4data["Orders"] if (o["OrderType"] == 0)] 

#print(seo_tags)
print(mt4data["AccountBalance"])
#print(mt4data["Ask"])
print(len(mt4data["Orders"]))
print(min(prices))
print(sum(margin) * 100000 / 500)



for order in mt4data["Orders"]:
    if (order["OrderType"] > 1):
        handlefordel.write(str(order["OrderTicket"]) + ";")

handlefordel.close()

price = mt4data["Ask"] - 0.01
for n in range(10):
    handleforcreate.write(str(price) + ";1;2;")
    price = price - 0.0001

handleprocess.write("end")
