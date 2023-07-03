# -*- coding: utf-8 -*-

def getSoundPackets(vetorSom):
    lista = []
    lista.append(['\r', '\n', '\r', '\n', 0, 200])
    for i in range(0,int(len(vetorSom)/200)):
        lista.append([i+1].append(vetorSom[i*200:(i+1)*200]))
    if(len(vetorSom)/200 > 0):
        lista.append([int(len(vetorSom)/200)])
    return lista

if __name__ == '__main__':
    print(getSoundPackets([0x0F] * 8044) )