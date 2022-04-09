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
import time
from threading import Thread
from hashlib import sha256
from datetime import datetime

threads = []

IP = "localhost"
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr, path,client_id, cons):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.sendto(f"Welcome, {addr[1]}!".encode("utf-8"), addr)  # 1
    conn.sendto(f"{client_id}".encode("utf-8"), addr)  # 2
    conn.sendto(f"{cons}".encode("utf-8"), addr)  # 3
    fsize = os.path.getsize(path)
    conn.sendto(f"{fsize}".encode("utf-8"), addr)  # 4

    buffer_size = 64000;

    start = time.time()
    file = open(path, "rb")
    data = file.read(buffer_size)

    x = 0
    while True:

        while (data):
            if (conn.sendto(data, addr)):
                x += 0.0625
                print(f"Sending to client {client_id} ... " + str(round(x, 3)) + " MB")
                data = file.read(buffer_size)
        file.close()

        end = time.time()

        tiempo = end - start

        fname = f"Cliente{client_id}-Prueba-{cons}"

        writeLog(addr, fsize, tiempo, fname, client_id)

    print(f"[DISCONNECTED] {addr} disconnected")


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print("[LISTENING] Server is listening")
    
    print("Inserte el número de conexiones del servidor")
    cons = input("> ")
    
    print("Archivo tipo 1: 100 MB")
    print("Archivo tipo 2: 250 MB")
    arch = input("[/] Seleccione el tipo de archivo: (1 o 2)\n")
    
    # Filepath
    path = SERVER_DATA_PATH
    if(arch == "1"):
        path += "/100.txt"
    elif arch == "2":
        path += "/250.txt"
        
    client_id = 0
    
    while True:
        id_client = 1
        while True:
            data, addr = server.recvfrom(4096)
            print(f"Cliente numero: {id_client} {data.decode()}")
            thread = Thread(target=handle_client, args=(server, addr, path, cons, id_client))

            threads.append(thread)

            if (id_client == cons):
                for thr in threads:
                    thr.start()
                break

            id_client += 1

# -----------------------------------------------------
# Métodos auxiliares
# -----------------------------------------------------

# Creacio archivo
def crearArchivo(path, tam):
    with open(path, "wb") as f:
        f.seek(tam * 1024 ** 2)
        f.write("Infracom".encode())

# Escribe el log del servidor
def writeLog(addr, fsize, time, fname, client_id):
    if not os.path.isdir("./logs"):
        os.mkdir("./logs")

    archivo = datetime.now()
    log = f"{archivo.year}-{archivo.month}-{archivo.day}-{archivo.hour}-{archivo.minute}-{archivo.second}-Cliente{client_id}-log.txt"
    fp = os.path.join('.', 'logs', 'servidor')
    if not os.path.exists(fp):
        os.mkdir(fp)
    fileLog = open(f"logs/servidor/{log}", "x")

    fileLog.write("Log {}\n".format(archivo))
    fileLog.write("File name {}\n".format(fname + ".txt"))
    fileLog.write("File size: {}".format(fsize))
    fileLog.write("\n")
    fileLog.write(" ***************** Client info ******************** \n")
    fileLog.write(f"* {addr} \n* Time to send: {round(time, 4)} secs")

    fileLog.close()

""" Main """
if __name__ == "__main__":
    main()

