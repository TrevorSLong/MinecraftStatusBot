from mcstatus import MinecraftServer

server = MinecraftServer.lookup("mc.hypixel.net")
status = server.status()
print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

latency = server.ping()
print("The server replied in {0} ms".format(latency))