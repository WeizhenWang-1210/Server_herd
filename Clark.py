import asyncio
import defserver

def main():
    server = defserver.Server(name="Clark",ip = '127.0.0.1', port = 10444)
    try:
        asyncio.run(server.run_forever())
    except KeyboardInterrupt:
        pass

def run():
    print("Clark")
    main()



'''
async def echo_server(reader, writer):
    f = open("clark.csv", "a+")
    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            break
        instruction = data.decode("utf-8")
        items = instruction.split()
        result = ""
        if(len(items)==4):
            pos = re.compile('[^\s]*')
            cord = re.compile('[+-]{1}(\d){1,}(\.)?(\d)*[+-]{1}(\d){1,}(\.)?(\d)*$')
            tstamp = re.compile("(\d)*(\.)?(\d)*$")
            if((items[0]=="IAMAT") and (pos.match(items[1]) is not None) and (cord.match(items[2]) is not None) and (tstamp.match(items[3]) is not None)):
                timestampdiff = time.time() - float(items[3])
                strtd = ""
                if(timestampdiff > 0):
                    strtd = "+"+str(timestampdiff)
                else:
                    strtd = "-"+str(timestampdiff)
                result = "AT CLARK " + strtd + " " + instruction
                log = items[1] + ";"+ items[2]+"\n"
                try:
                    f.write(log)
                except ValueError:
                    f = open("clark.csv", "a+")
                    f.write(log)
                f.close()
            else:
                result = "?" + " " + instruction
        else:
            result = "?" + " " + instruction      
        ret = result.encode("utf-8")
        writer.write(ret)
        await writer.drain()  # Flow control, see later
    writer.close()
async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()

def run():
    print("Clark")
    asyncio.run(main('127.0.0.1', 10447))
'''