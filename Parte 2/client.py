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
import os
import threading
from datetime import datetime
import time
from hashlib import sha256


IP = "localhost"
PORT = 4466
SIZE = 1024
FORMAT = "utf-8"
RECEIVED_DATA_PATH = "Recibidos"

clients = int(input('how many clients? '))
while (clients <= 0 and clients>25 ):
    clients = int(input('Invalid number '))

class Main:
    def __init__(self):
        self.lock = threading.Lock()
    def funct(self, name):
        self.lock.acquire()
        log = open("./logs/"+name+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
        self.lock.release()
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ADDR = ('localhost', 4466)
        print('connecting to %s port %s' % ADDR)
        server.connect(ADDR)
        file = open("./Recibidos/" + name + "-prueba-" + str(clients) + ".txt", "w")

        try:
            self.lock.acquire()
            mensaje = b'Iniciar conexion...'
            print('enviando "%s"' % mensaje)
            server.sendto(mensaje,ADDR)

            check, ADDR = server.recvfrom(32)
            if (check.decode('utf-8') == "ok"):
                print('servidor mando ok')
                server.sendto(b'Cual es el nombre del archivo?', ADDR)
                N, server_addr = server.recvfrom(32)
                file_name = N.decode('utf-8')
                log.write('El nombre es: ' + file_name + '\n')
                server.sendto(b'listo', ADDR)

                num_paq = 0
                start_time = time.time()
                err = False
                while (True):
                    data, server_addr = server.recvfrom(1024)

                    if data:
                        try:
                            file.write(data.decode('utf-8') + os.linesep)
                            # md5.update(data)
                            num_paq += 1

                        except:
                            err = True
                            print('Ocurrio un error')
                            server.sendto(b'Hubo un error al recibir el archivo', server_addr)
                            break

                    else:
                        print('Final de lectura del archivo')
                        server.sendto(b'Archivo recibido', server_addr)
                        break
                end_time = time.time()
                file_size = os.path.getsize("./Recibidos/" + name + "-prueba-" + str(clients) + ".txt")

                file.close()
                log.write('El nombre del cliente es: ' + name + '\n')
                log.write('El tamaño del archivo es: ' + str(file_size / 1000000) + ' MB' + '\n')
                if err == False:
                    print("Archivo leido")
                    log.write('Entrega del archivo' + '\n')
                else:
                    log.write('Error entrega archivo' + '\n')

                log.write('Tiempo de transferencia: ' + str(end_time - start_time) + ' segs' + '\n')
                log.write('Valor total en bytes recibidos: ' + str(file_size) + '\n')
                log.write('Cantidad de paquetes recibidos: ' + str(num_paq) + '\n')

        finally:

            print('Cerrar socket')

            self.lock.release()
            print('Fin del programa')
            log.close()
        server.close()

def t(c, nombre):
    c.funct(nombre)


hilo = Main()
for clients in range(clients):
    client = threading.Thread(name="Cliente%s" % (clients + 1),
                               target=t,
                               args=(hilo, "Cliente%s" % (clients + 1))
                               )
    client.start()
