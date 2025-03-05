import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, Polyline } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "./App.css";

function App() {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [route, setRoute] = useState([]);
  const [distance, setDistance] = useState(null);

  // Capture user clicks to set start and end points
  function MapClickHandler() {
    useMapEvents({
      click(e) {
        if (!start) setStart(e.latlng);
        else setEnd(e.latlng);
      },
    });
    return null;
  }

  // Fetch route from FastAPI backend
  async function fetchRoute() {
    if (!start || !end) return;

    const res = await axios.get("http://localhost:8000/route/", {
      params: {
        start_lat: start.lat,
        start_lon: start.lng,
        end_lat: end.lat,
        end_lon: end.lng,
      },
      headers:{
        "Access-Control-Allow-Origin": "http://localhost:5173",
      }
    });

    setRoute(res.data.route);
    setDistance(res.data.distance_km);
  }
  const reset =  async () =>{
    setStart(null);
    setEnd(null);
  };
  return (
    <div id="mapcon">
      <MapContainer center={[36.75, 3.04]} zoom={6} style={{ height: "500px", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <MapClickHandler />
        {start && <Marker position={start} />}
        {end && <Marker position={end} />}
        {route.length > 0 && <Polyline positions={route} color="blue" />}
      </MapContainer>
      <button onClick={fetchRoute} disabled={!start || !end} style={{ marginTop: "10px" }}>
        Get Route
      </button>
      <button onClick={reset}>
        Reset
      </button>
      {distance && <p>Distance: {distance} km</p>}
    </div>
  );
}

export default App;
