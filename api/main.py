from fastapi import FastAPI, Query
import osmnx as ox
import networkx as nx
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the road network of Algeria
G = ox.graph_from_place("Moscow", network_type="drive")

def h(u, v):
    return abs(u - v)

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
    
    # Compute shortest route
    # route = nx.shortest_path(G, orig_node, dest_node, weight="length")
    route = nx.astar_path(G, orig_node, dest_node, heuristic=h, weight="length")

    # Extract route coordinates
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    
    # Compute total distance
    _, edges_gdf = ox.graph_to_gdfs(G)  # Get route edges
    route_edges = edges_gdf.loc[route]
    route_length = route_edges["length"].sum()  # Sum edge lengths
    
    return {"route": route_coords, "distance_km": route_length / 1000}

uvicorn.run(app, port=8000, host="0.0.0.0")
