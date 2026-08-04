def updatefileProperties (filePath,key,value):
    with open(filePath,"r") as serverConf:
        lines = serverConf.readlines();

    with open(filePath,"w") as serverConf:
        for line in lines:
            if key in line:
                serverConf.write(key+"="+value+"\n")
            else:
                 serverConf.write(line)


updatefileProperties("server.conf","MAX_CONNECTIONS","200")