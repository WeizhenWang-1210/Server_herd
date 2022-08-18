import asyncio
import defserver

def main():
    server = defserver.Server(name="Bernard",ip = '127.0.0.1', port = 10441)
    try:
        asyncio.run(server.run_forever())
    except KeyboardInterrupt:
        pass

def run():
    print("Bernard")
    main()