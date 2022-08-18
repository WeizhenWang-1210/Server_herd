import asyncio
import defserver

def main():
    server = defserver.Server(name="Campbell",ip = '127.0.0.1', port = 10443)
    try:
        asyncio.run(server.run_forever())
    except KeyboardInterrupt:
        pass

def run():
    print("Campbell")
    main()