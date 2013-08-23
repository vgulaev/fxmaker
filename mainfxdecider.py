import json
#mydict = {"AccountBalance" : 2,
#          "Orders": [{"ticket" : 1}, {"ticket" : 2}]}

def profitEURUSD(sp, ep):
    return (ep - sp) * 100000
    
border_price = 1.25

handlefordel = open("C:/Program Files (x86)/MetaTrader 4/experts/files/delete.csv", "w")
handleforcreate = open("C:/Program Files (x86)/MetaTrader 4/experts/files/create.csv", "w")
handleprocess = open("C:/Program Files (x86)/MetaTrader 4/experts/files/proccess.csv", "w")

json_file = open("C:/Program Files (x86)/MetaTrader 4/experts/files/my_data.csv","r")
json_string = json_file.read()
json_file.close() 

mt4data = eval(json_string)

prices = [o["OrderOpenPrice"] for o in mt4data["Orders"] if (o["OrderType"] == 0)]

margin_for_currents_lots = [-o["OrderOpenPrice"] * o["OrderLots"] * 100000 / 500 + o["OrderLots"] * profitEURUSD(o["OrderOpenPrice"], border_price) for o in mt4data["Orders"] if (o["OrderType"] == 0)] 

#print(mt4data)

#k = sorted(mt4data["Orders"], key = lambda student: student["OrderOpenPrice"])

#tmpfile = open("my.json", "w")
#tmpfile.write(str(k))
#tmpfile.close()

print(mt4data["AccountBalance"])
mp = min(prices)

print(mp)

balance_for_grid_001 = ((mp - border_price) / 0.0001) * 0.01 * profitEURUSD((mp + border_price)/2, border_price) - (mp + border_price)/2 * ((mp - border_price) / 0.0001) * 0.01 * 100000 / 500
print(balance_for_grid_001)
print(sum(margin_for_currents_lots))

freemargin = mt4data["AccountBalance"] + balance_for_grid_001 + sum(margin_for_currents_lots)
print(freemargin)
#print(sum(margin) * 100000 / 500)

price = round(mt4data["Bid"], 4) - 0.0001
neworders = []
while (freemargin > 0):
    neworders.append({"Ticket": "new",
                      "OrderOpenPrice": price,
                      "OrderLots": 0.1})
    freemargin  = freemargin + 0.1 * profitEURUSD(price, border_price) - price * 100000 / 500 * 0.1 

print(len(neworders))

for order in mt4data["Orders"]:
    if (order["OrderType"] > 1):
        handlefordel.write(str(order["OrderTicket"]) + ";")

handlefordel.close()

price = mt4data["Ask"] - 0.01
for n in range(10):
    handleforcreate.write(str(price) + ";1;2;")
    price = price - 0.0001

handleprocess.write("end")
