import sys
from scapy.all import *
from time import *
import statistics

# pip install modified-thompson-tau-test
from Modified_Thompson_Tau_Test.modified_thompson_tau_test import run_modified_thompson_tau_test


# Parámetros ajustables
maxTTL = 30
destino = "acpe.edu.au"
cantidadDeMediciones = 30

def traceroute(url):
    print(f'\nTracerouting a {destino}')
    responses = {}
    for i in range(cantidadDeMediciones):
        print()
        for ttl in range(1,maxTTL):
            probe = IP(dst=url, ttl=ttl) / ICMP()
            t_i = time()
            ans = sr1(probe, verbose=False, timeout=0.8)
            t_f = time()
            rtt = (t_f - t_i)*1000 #Parece ser que así queda en milisegundos
            if ans is not None:
                if ttl not in responses: 
                    responses[ttl] = []
                responses[ttl].append((ans.src, round(rtt, 2)))

                if ttl in responses:
                    print(ttl, responses[ttl])


    #Para cada rtt me quedo con el router con más apariciones y promediamos sus resultados
    print(f'\n Resultados promediados:\n')
    averagedResponses = {}
    for ttl in range(1, maxTTL):
        if ttl not in responses:
            continue
        ipDictionary = {}
        for result in responses[ttl]:
            resultIP = result[0]
            ipDictionary[resultIP] = ipDictionary[resultIP] + 1 if resultIP in ipDictionary.keys() else 0
        mostFrequentIP = max(ipDictionary)
        RTTsOfMostFrequentIP = []
        for result in responses[ttl]:
            resultIP = result[0]
            if resultIP == mostFrequentIP:
                RTTsOfMostFrequentIP.append(result[1])
        averagedRTT = statistics.mean(RTTsOfMostFrequentIP)
        averagedResponses[ttl] = (mostFrequentIP, round(averagedRTT, 2))
        print(ttl, averagedResponses[ttl])


    #Elimino routers repetidos:
    print(f'\n Eliminando routers repetidos:\n')
    routers = {}
    for ttl in averagedResponses.keys():
        responseIP = averagedResponses[ttl][0]
        responseRTT = averagedResponses[ttl][1]
        if responseIP not in routers.keys():
            routers[responseIP] =  [responseRTT]        
        else:
            routers[responseIP].append(responseRTT)
    for routerIP in routers.keys():
        routers[routerIP] = statistics.mean(routers[routerIP])
        print(f'Router: {routerIP} , RTT a CABA: {round(routers[routerIP], 2)}')


    #Calculo el RTT entre los routers
    print(f'\n RTT entre los routers:\n')
    IPs = list(routers.keys())
    RTTentreRouters = []
    for routerIP in IPs[:-1]:
        siguienteRouterIP = IPs[IPs.index(routerIP) + 1]
        RTTentreEllos = round(routers[siguienteRouterIP]-routers[routerIP], 4)
        if(RTTentreEllos < 0): continue
        RTTentreRouters.append(RTTentreEllos)
        print(f'RTT entre {routerIP} y {siguienteRouterIP}: {RTTentreEllos}')


    #Printeamos sólo las IPs para poder copypastearlas fácilmente en ipinfo.io o similares:
    print(f'\n Sólo las IPs de los routers:')
    for routerIP in list(routers.keys()): print(routerIP)


    #Calculamos los outliers
    print()
    print(run_modified_thompson_tau_test(RTTentreRouters))
    

traceroute(destino)