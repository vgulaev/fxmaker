import json
#mydict = {"AccountBalance" : 2,
#          "Orders": [{"ticket" : 1}, {"ticket" : 2}]}

def profitEURUSD(sp, ep):
    return (ep - sp) * 100000
    
#this is minimal price whitch use in calculation 
border_price = 1.25
#this the aim of edge volume, every order must have
#this volume
volume_edge = 0.1

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
no_max = price 
neworders = []
while (freemargin > 0):
    no_min = price
    neworders.append({"Ticket": "new",
                      "OrderOpenPrice": price,
                      "OrderLots": 0.1})
    freemargin  = freemargin + 0.1 * profitEURUSD(price, border_price) - price * 100000 / 500 * 0.1
    price = round(price - 0.0001, 4) 

current_orders = sorted([o for o in mt4data["Orders"] if ((o["OrderOpenPrice"] >= no_min)and(o["OrderOpenPrice"] <= no_max))], key = lambda o: o["OrderOpenPrice"], reverse=True)

#print(neworders[0])
#print(current_orders[0])

i1 = 0
i2 = 0
breakthisloop = False
while (breakthisloop == False):
    #if prices equal then check type order and volume
    #if incorect volume then we need new order
    if (neworders[i1]["OrderOpenPrice"] == current_orders[i2]["OrderOpenPrice"]):
        if (current_orders[i2]["OrderLots"] == neworders[i1]["OrderLots"]):
            neworders[i1]["Ticket"] = "remove"
        i1 = i1 + 1
        i2 = i2 + 1
    elif (neworders[i1]["OrderOpenPrice"] < current_orders[i2]["OrderOpenPrice"]):
        i2 = i2 + 1
    elif (neworders[i1]["OrderOpenPrice"] > current_orders[i2]["OrderOpenPrice"]):
        i1 = i1 + 1
    if (i1 == len(neworders))or(i2 == len(current_orders)):
        break
        
#print(neworders)
#print(len(current_orders))

for order in current_orders:
    if ((order["OrderLots"] == 0.01)and(order["OrderType"] == 2)):
        handlefordel.write(str(order["OrderTicket"]) + ";")

handlefordel.close()

#price = mt4data["Ask"] - 0.01
for n in neworders:
    if (n["Ticket"] == "new"):
        handleforcreate.write(str(n["OrderOpenPrice"]) + ";" + str(n["OrderLots"]) + ";2;")
    #price = price - 0.0001

handleprocess.write("end")
