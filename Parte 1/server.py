#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Servidor multithread para la descarga de archivos
#
# @author: nataliasanabria
# (c) 2022. Universidad de los Andes
# Facultad de Ingeniería
# Infraestructura de comunicaciones
# -----------------------------------------------------

import os
import socket
import threading
from hashlib import sha256
import time 
from datetime import datetime

IP = socket.gethostbyname(socket.gethostname());
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr, path,client_id, cons):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server.".encode(FORMAT))

    while True:
        
        # Getting file details.
        file_size = os.path.getsize(path)

        # Sending file_name and detail.
        conn.send(path.encode(FORMAT))
        conn.send(str(file_size).encode(FORMAT))
        file_hash = getHash(path)
        print(f"server hash: {file_hash}")
        conn.send(file_hash.encode(FORMAT))
        data = str(client_id)+"@"+str(cons)
        conn.send(data.encode(FORMAT))

        print("[SENDING] Sending file")
        # Opening file and sending data.
        with open(path, "rb") as file:
            c = 0
            # Starting the time capture.
            start_time = time.time()

            # Running loop while c != file_size.
            while c <= file_size:
                data = file.read(SIZE)
                if not (data):
                    break
                conn.sendall(data)
                c += len(data)

            # Ending the time capture.
            end_time = time.time()
            total_time = end_time - start_time
            print("File Transfer Complete.Total time: ", total_time)
        
        """
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        
        if cmd == "LOGOUT":
            break
        """
    print(f"[DISCONNECTED] {addr} disconnected")


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening")
    
    print("Inserte el número de conexiones que recibirá el servidor")
    cons = input("> ")
    
    print("Archivo tipo 1: 100 MB")
    print("Archivo tipo 2: 250 MB")
    arch = input("[/] Seleccione el tipo de archivo a enviar: (1 o 2)\n")
    
    # Filepath
    path = SERVER_DATA_PATH
    
    if(arch == "1"):
        path += "/dummy100.txt"
    elif arch == "2":
        path += "/dummy250.txt"
        
    client_id = 0
    
    while True:
        conn, addr = server.accept()
        client_id+=1
        thread = threading.Thread(target=handle_client, args=(conn, addr, path, client_id, cons))
        thread.start()
    conn.close()

# -----------------------------------------------------
# Métodos auxiliares
# -----------------------------------------------------

# Entrega el valor de hash
def getHash(path):
    hash = sha256()
    with open(path, "rb") as f:
        while True:
            bloque = f.read(4096)
            if not bloque:
                break
            hash.update(bloque)
    f.close()
    return hash.hexdigest()

# Escribe el log del servidor
def writeLog(path, ip, port, fsize, tiempo):

    if not os.path.isdir("./logs"):
        os.mkdir("./logs")

    fActual = datetime.now()
    log = f"{fActual.year}-{fActual.month}-{fActual.day}-{fActual.hour}-{fActual.minute}-{fActual.second}-log.txt"
    
    fileLog = open(f"logs/{log}", "x")

    fileLog.write("Log {}\n".format(fActual))
    fileLog.write("Nombre del archivo: {}\n".format(path.split("/")[-1]))
    fileLog.write("Tamaño del archivo: {}".format(fsize))
    fileLog.write("\n")
    fileLog.write("####################################################\n")
    fileLog.write("* ip: {add}\n* port: {p}\n* time: {t}\n".format(add=ip, p=port, t = tiempo*1000))
    fileLog.write("\n")

    fileLog.close()

""" Main """
if __name__ == "__main__":
    main()

