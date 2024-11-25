#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/rpgtoolbox/charhandler.py
\package rpgtoolbox.charhandler
\brief Character Handler für internal data exchange and communitcation

This is a very basic

lorem ipsum

\date (c) 2023
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "22.12.2023"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__license__ = "GNU V3"
__copyright__ = "2022 - 2023"

import json
import socket

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *
from rpgtoolbox.globaltools import *

mycnf = chkCfg()
logger = log.createLogger('global', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"] , 'charhandler.log')



class Server:
    """!This class raises a central server for managing character data during
        play and saving current statusses of them when playing session is finished
    """


    def __init__(self, host = "127.0.0.1", port = 9999, groupfile = "", npcfile = ""):
        """!Constructor of Server object

            @param host address to bind the server (default:127.0.0.1)
            @param port port number to bind the server (defaalt: 9999)
            @param groupfile path and name of a JSON file to load initially a group
                             of player characters from
            @param npcfile path and name of a CSV (campaign) file to load intially
                           npcs from
        """

        if groupfile:
            logger.debug(f"read {groupfile}")

            with open(groupfile) as fp:
                self.chargrp = json.load(fp)
            logger.info(f"{groupfile} successfully read")

        else:
            self.chargrp = []

        if npcfile:
            logger.debug(f"read {npcfile}")
            self.npcgrp = readCSV(npcfile)
            logger.info(f"{npcfile} successfully read")

        else:
            self.npcgrp = []

        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)


    def start(self):
        """! method to start the sever . client communication

        -----
        @todo the following has to be implemented:
        - variable transfer sizes in chunks (1024)
        - action commands definition: add/remove (n)pc, inventory commands, save commands
        """
        logger.info(f"Server listen to {self.host}:{self.port}...")
        client_socket, client_address = self.server_socket.accept()
        logger.info(f"connection from {client_address} established.")

        request = client_socket.recv(1024).decode('utf-8')
        logger.debug(f"incomming request: {request}")

        if request == "Daten anfordern":
            response = "Hier sind die Daten vom Server."
            client_socket.sendall(response.encode('utf-8'))

        else:
            response = "Ungültige Anfrage."
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()


    def stop(self):
        self.server_socket.close()



class Client:


    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))


    def send_request(self, request):
        self.client_socket.sendall(request.encode('utf-8'))
        data = self.client_socket.recv(1024)
        print(f"Empfangene Daten: {data.decode('utf-8')}")


    def close(self):
        self.client_socket.close()



if __name__ == "__main__":
    # Beispiel der Verwendung der Klassen
    HOST = '127.0.0.1'
    PORT = 9999

    server = Server(HOST, PORT)
    client = Client(HOST, PORT)

    try:
        server.start()
        client.send_request('Daten anfordern')
    finally:
        server.stop()
        client.close()
