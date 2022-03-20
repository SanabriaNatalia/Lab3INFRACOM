#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Cliente uni-thread para la descarga de archivos
#
# @author: nataliasanabria
# (c) 2022. Universidad de los Andes
# Facultad de Ingeniería
# Infraestructura de comunicaciones
# -----------------------------------------------------

import os
import socket
import time
from hashlib import sha256

IP = socket.gethostbyname(socket.gethostname());
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
RECEIVED_DATA_PATH = "ArchivosRecibidos"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(ADDR)
    
    while True:
        data = server.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        
        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break
        
        # Received file details.
        file_path = server.recv(SIZE).decode(FORMAT)
        file_size = server.recv(SIZE).decode(FORMAT)
        file_hash = server.recv(SIZE).decode(FORMAT)
        data = server.recv(SIZE).decode(FORMAT)
        
        file_name = file_path.split("/")[-1]
        
        data = data.split("@")
        client_id = data[0]
        cons = data[-1]
        
        print(f"File name: {file_name} \n")
        print(f"File size: {file_size} \n")

        
        if not os.path.isdir("./ArchivosRecibidos"):
            os.mkdir("./ArchivosRecibidos")
        
        print("[RECEIVING] Receiving file")
        # Opening and reading file.
        with open("./ArchivosRecibidos/" + file_name, "wb") as file:
            c = 0
            # Starting the time capture.
            start_time = time.time()

            # Running the loop while file is recieved.
            while c <= int(file_size):
                data = server.recv(1024)
                if not (data):
                    break
                file.write(data)
                c += len(data)

            # Ending the time capture.
            end_time = time.time()

        print("File transfer Complete.Total time: ", end_time - start_time)
        
        file_path = "./" + RECEIVED_DATA_PATH + "/" + file_name
        new_path = "./" + RECEIVED_DATA_PATH + "/Cliente" + client_id+"-Prueba-"+cons+".txt"
        
        client_hash = getHash(file_path)
        match = client_hash == file_hash
        
        print(f"Received hash: {file_hash}")
        print(f"Calculated hash: {client_hash}")
        
        if match:
            print("Los hash de los archivos son consistentes")
        else :
            print("Error en la verificación de los hash")
        
        os.rename(file_path, new_path)
        
        """
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]
        
        if cmd == "LOGOUT":
            server.send(cmd.encode(FORMAT))
            break
        """
        break
    
    print("Disconnected from the server.")
    server.close()        
            
    
# -----------------------------------------------------
# Métodos auxiliares
# -----------------------------------------------------

def getHash(path):
    hash = sha256()
    with open(path, "rb") as f:
        while True:
            bloque = f.read(SIZE)
            if not bloque:
                break
            hash.update(bloque)
    f.close()
    return hash.hexdigest()

# Escribe el log del cliente
def writeLog(path, ip, port, fsize, tiempo):

    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
    

""" Main """
if __name__ == "__main__":
    main()
