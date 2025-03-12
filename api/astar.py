import networkx as nx
import heapq

def a_star(graph, start, goal, heuristic):
    
    open_list = []
    
    g_values = {start: 0}
    
    came_from = {}

    node_1 = (graph.nodes[start]['x'], graph.nodes[start]['y'])
    node_2 = (graph.nodes[goal]['x'], graph.nodes[goal]['y'])

    
    heapq.heappush(open_list, (heuristic(node_1, node_2), start))

    while open_list:
        
        current_f, current_node = heapq.heappop(open_list)

        
        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path

        
        for neighbor in graph.neighbors(current_node):
            
            n1 = (graph.nodes[neighbor]['x'], graph.nodes[neighbor]['y'])
            n2 = (graph.nodes[goal]['x'], graph.nodes[goal]['y'])

            tentative_g = g_values[current_node] + graph[current_node][neighbor].get('weight', 1)  # default weight 1 if not set
            
           
            if neighbor not in g_values or tentative_g < g_values[neighbor]:
                g_values[neighbor] = tentative_g
                f_value = tentative_g + heuristic(n1, n2)
                heapq.heappush(open_list, (f_value, neighbor))
                came_from[neighbor] = current_node

    return None  

