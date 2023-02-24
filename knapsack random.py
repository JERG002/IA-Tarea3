import heapq
import random

def knapsack(items, capacity):
    def heuristic(node):
        weight, value, taken = node
        remaining_capacity = capacity - weight
        remaining_items = items[len(taken):]
        remaining_items.sort(key=lambda item: item[1]/item[0], reverse=True)
        heuristic_value = value
        for item in remaining_items:
            if item[0] <= remaining_capacity:
                heuristic_value += item[1]
                remaining_capacity -= item[0]
            else:
                heuristic_value += remaining_capacity * item[1] / item[0]
                break
        return -heuristic_value

    heap = [(0, (0, 0, []))]
    best_value = 0
    best_taken = []
    while heap:
        _, node = heapq.heappop(heap)
        weight, value, taken = node
        if weight > capacity:
            continue
        if not taken:
            remaining_items = items
        else:
            remaining_items = items[len(taken):]
        for i, item in enumerate(remaining_items):
            new_weight = weight + item[0]
            new_value = value + item[1]
            new_taken = taken + [i]
            new_node = (new_weight, new_value, new_taken)
            if new_weight <= capacity and new_value > best_value:
                best_value = new_value
                best_taken = new_taken
            heapq.heappush(heap, (heuristic(new_node), new_node))
    return (best_value, [items[i] for i in best_taken])

items = [(random.randint(1, 10), random.randint(1, 10)) for i in range(10)]
capacity = random.randint(10, 20)
print(f"Objetos: {items}")
best_value, best_items = knapsack(items, capacity)
print(f"Best value: {best_value}")
print(f"Best items: {best_items}")
