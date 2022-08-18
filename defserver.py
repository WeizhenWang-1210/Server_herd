import asyncio
import re
import time
import AT
from collections import defaultdict
class Server:
    channels = {
        "Juzang":["Clark","Bernard","Campbell"],
        "Bernard":["Juzang","Jaquez","Campbell"],
        "Jaquez":["Clark","Bernard"],
        "Campbell":["Bernard","Juzang"],
        "Clark" : ["Jaquez", "Juzang"]
    }
    portmap = {
        "Juzang":10440,
        "Bernard": 10441,
        "Jaquez": 10442,
        "Campbell": 10443,
        "Clark":10444
    }
    def __init__(self, name, ip, port, message_max_length=1e6):
        self.name = name
        self.ip = ip
        self.port = port
        self.message_max_length = int(message_max_length)
        self.logname = self.name + ".csv"
        self.record = self.name + ".log"
        self.senders = {
            "Juzang":"",
            "Bernard": "",
            "Jaquez": "",
            "Campbell": "",
            "Clark":""
        }

    async def handle(self, reader, writer):
        f = open(self.logname, "a+")
        l = open(self.record, "a+")
        while True:
            data = await reader.read(self.message_max_length)  # Max number of bytes to read
            if not data:
                break
            message = data.decode("utf-8")
            tmp = message.rstrip()+";"+"\n"
            try:
                l.write(tmp)
            except ValueError:
                l = open(self.record, "a+")
                l.write(tmp)
            l.close()
            items = message.split()
            result = ""
            if(len(items)==4):
                if(items[0]=="IAMAT" and checkIAMAT(items)):
                    timestampdiff = time.time() - float(items[3])
                    strtd = ""
                    if(timestampdiff > 0):
                        strtd = "+"+str(timestampdiff)
                    else:
                        strtd = "-"+str(timestampdiff)
                    storemsg = " ".join(items[1:])
                    result = "AT " + self.name + " " + strtd + " " + storemsg + "\n"
                    coord = parseCoord(items[2])
                    log = items[1] + ";"+ coord[0] + ";" + coord[1] + ";" + result.replace(" ","_") + "\n"
                    try:
                        f.write(log)
                    except ValueError:
                        f = open(self.logname, "a+")
                        f.write(log)
                    f.close()
                    await self.propagate_message(log.rstrip())
                elif(items[0]=="WHATSAT" and checkWHATSAT(items)):
                    try:
                        f = open(self.logname,"r")
                    except:
                        print("problem reading")
                        exit(1)
                    lines = f.readlines()
                    lat = ""
                    long = ""
                    message = ""
                    find = False
                    for line in reversed(lines):
                        if(line.split(";")[0]==items[1]):
                            lat = line.split(";")[1]
                            long = line.split(";")[2]
                            message = line.split(";")[3].replace("_"," ")
                            find = True
                            #print("findit")
                            break
                    if(find):
                        rad = int(items[2])
                        bound = int(items[3])
                        result = message + await AT.find(lat,long,rad,bound)
                        result += "\n"
                    else:
                        result = "There is no coordinate associated witht this id"
                else:
                    result = "?" + " " + message
            elif (len(items)==2 and checkpropagate(items)):
                sender = items[0]
                msg = items[1]
                #print("received "+items[1]+ "from " + items[0])
                
                if(self.senders[sender] != msg):
                    self.senders[sender] = msg
                    try:
                        f.write(msg + "\n")
                    except:
                        f = open(self.logname, "a+")
                        f.write(msg + "\n")
                    f.close()
                    try:
                        l.write("Received from {} {}".format(sender, message)+";\n")
                    except:
                        l = open(self.record, "a+")
                        l.write("Received from {} {}".format(sender, message)+";\n")
                    l.close()
                    for neighbor in self.channels[self.name]:
                         if(neighbor!=sender):
                             #print(items[1])
                             await self.propagate_message(items[1])
                else:
                    try:
                        l.write("Received from {} {}".format(sender, message)+"Already seen, no propagation;\n")
                    except:
                        l = open(self.record, "a+")
                        l.write("Received from {} {}".format(sender, message)+"Already seen, no propagation;\n")
                    l.close()
                    #the sender already sent, no propagate 
                
            else:
                result = "?" + " " + message
            tmp = result.rstrip()+";"+"\n"
            try:
                l.write(tmp)
            except ValueError:
                l = open(self.record, "a+")
                l.write(tmp)
            l.close()  
            ret = result.encode("utf-8")
            writer.write(ret)
            await writer.drain()  # Flow control, see later
        writer.close()

    async def run_forever(self):
        server = await asyncio.start_server(self.handle, self.ip, self.port)

        # Serve requests until Ctrl+C is pressed
        print(f'serving on {server.sockets[0].getsockname()}')
        async with server:
            await server.serve_forever()
        # Close the server
        server.close()
        
    async def propagate_message(self, message):
        # send message to every server connected
        for neighbor in Server.channels[self.name]:
            msg = "{} {}".format(self.name,message)
            #print(msg)
            #print(str(len(msg.split(" "))))
            try:
                reader,writer = await asyncio.open_connection('127.0.0.1', Server.portmap[neighbor])
                f = open(self.record, "a+")
                f.write("{} send to {}: {}".format(self.name, neighbor, msg) + ";")
                f.close()
                writer.write(msg.encode())
                await writer.drain()
                f = open(self.record, "a+")
                f.write("Closing connection to {}".format(neighbor)+";"+"\n")
                f.close()
                writer.close()
                await writer.wait_closed()
            except:
                f = open(self.record, "a+")
                f.write("Error connecting to server {}".format(neighbor)+";"+"\n")
                f.close()
        



def checkIAMAT(items):
    pos = re.compile('[^\s]*')
    cord = re.compile('[+-]{1}(\d){1,}(\.)?(\d)*[+-]{1}(\d){1,}(\.)?(\d)*$')
    tstamp = re.compile("(\d)*(\.)?(\d)*$")
    result = (pos.match(items[1]) is not None) and (cord.match(items[2]) is not None) and (tstamp.match(items[3]) is not None)
    return result

def checkWHATSAT(items):
    pos = re.compile('[^\s]*')
    radius = re.compile('(\d)*')
    number = re.compile('(\d)*')
    result = (pos.match(items[1]) is not None) and (radius.match(items[2]) is not None) and (number.match(items[3]) is not None)
    return result

def parseCoord(cord):
    met = 0
    count = 0
    for i in cord:
        if(i!='+' and i!='-'):
            count += 1
        else:
            if(met == 1):
                break
            else:
                met +=1
    return [cord[0:count+1],cord[count+1:-1]]

def checkpropagate(items):
    isserver = items[0] in ["Clark", "Bernard", "Juzang", "Jaquez", "Campbell"]
    info  = items[1].split(";")
    coord = re.compile('[+-]{1}(\d){1,}(\.)?(\d)*')
    result = (isserver and (coord.match(info[1]) is not None) and (coord.match(info[2]) is not None))
    return result
    
    



    

