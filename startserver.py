# ['Juzang', 'Bernard', 'Jaquez', 'Campbell', 'Clark']
def startserver(server):
    if(server == 'Juzang'):
        try:
            import Juzang
            Juzang.run()
        except:
            print("Problem Starting Juzang")
            exit()
    elif(server == 'Bernard'):
        try:
            import Bernard
            Bernard.run()
        except:
            print("Problem Starting Bernard")
            exit()
    elif(server == 'Jaquez'):
        try:
            import Jaquez
            Jaquez.run()
        except:
            print("Problem Starting Jaquez")
            exit()
    elif(server == 'Campbell'):
        try:
            import Campbell
            Campbell.run()
        except:
            print("Problem Starting Campbell")
            exit()
    elif(server == 'Clark'):
        try:
            import Clark
            Clark.run()
        except:
            print("Exit Clark")
            exit()
    else:
        print("Not a valid server, not STARTING!")
        exit()

