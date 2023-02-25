import heapq
import random
import time 

inicio = time.time()
def knapsack(obto, cap):
    def heuristic(node):
        peso, valor, tomado = node
        restantes_cap = cap - peso
        restantes_obto = obto[len(tomado):]
        restantes_obto.sort(key=lambda item: item[1]/item[0], reverse=True)
        heuristic_valor = valor
        for item in restantes_obto:
            if item[0] <= restantes_cap:
                heuristic_valor += item[1]
                restantes_cap -= item[0]
            else:
                heuristic_valor += restantes_cap * item[1] / item[0]
                break
        return -heuristic_valor

    heap = [(0, (0, 0, []))]
    mejor_val = 0
    mejor_tomado = []
    while heap:
        _, node = heapq.heappop(heap)
        peso, valor, tomado = node
        if peso > cap:
            continue
        if not tomado:
            restantes_obto = obto
        else:
            restantes_obto = obto[len(tomado):]
        for i, item in enumerate(restantes_obto):
            nue_peso = peso + item[0]
            nue_valor = valor + item[1]
            nue_tomado = tomado + [i]
            nue_node = (nue_peso, nue_valor, nue_tomado)
            if nue_peso <= cap and nue_valor > mejor_val:
                mejor_val = nue_valor
                mejor_tomado = nue_tomado
            heapq.heappush(heap, (heuristic(nue_node), nue_node))
    return (mejor_val, [obto[i] for i in mejor_tomado])

obto = [(random.randint(1, 50), random.randint(1, 50)) for i in range(50)]
cap = random.randint(10, 20)
print(f"Objetos: {obto}")
mejor_val, mejor_obj = knapsack(obto, cap)
print(f"Mejor valor: {mejor_val}")
print(f"Mejor objeto: {mejor_obj}")

fin = time.time()

print('Tiempo de ejecucion: ', fin-inicio)