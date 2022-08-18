import asyncio
import defserver

def main():
    server = defserver.Server(name="Juzang",ip = '127.0.0.1', port = 10440)
    try:
        asyncio.run(server.run_forever())
    except KeyboardInterrupt:
        pass

def run():
    print("Juzang")
    main()