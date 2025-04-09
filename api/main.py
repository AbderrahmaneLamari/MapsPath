from fastapi import FastAPI, Query
import osmnx as ox
import networkx as nx
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from astar import a_star
import math

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the road network of Algeria
G = ox.graph_from_place("Algiers", network_type="drive")

def h(u, v):
    return abs(u - v)

def haversine_heuristic(u, v):
    lat1, lon1 = u  # Coordinates of node u (latitude, longitude)
    lat2, lon2 = v  # Coordinates of node v (latitude, longitude)
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # Radius of the Earth in kilometers
    distance = R * c  # Distance in kilometers
    
    return distance

def euclidean_heuristic(u, v):
    x1, y1 = u  # Coordinates of node u
    x2, y2 = v  # Coordinates of node v
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

@app.get("/")
async def get_hello():
    return "Hello world"

@app.options("/route/")
async def get_options():
    return ["POST", "OPTIONS", "GET"]
    
@app.get("/route/")
async def get_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    orig_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    dest_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

    print(orig_node)
    print(dest_node)
    
    try:    

        # Compute shortest route
        # route = nx.shortest_path(G, orig_node, dest_node, weight="length")
        route = a_star(G, orig_node, dest_node, euclidean_heuristic)    

        # Extract route coordinates
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

        # Compute total distance
        _, edges_gdf = ox.graph_to_gdfs(G)  # Get route edges
        route_edges = edges_gdf.loc[route]
        route_length = route_edges["length"].sum()  # Sum edge lengths
    except e as Exception:
        print(e)
    finally:
        return {"route": route_coords, "distance_km": route_length / 1000}

uvicorn.run(app, port=8000, host="0.0.0.0")

