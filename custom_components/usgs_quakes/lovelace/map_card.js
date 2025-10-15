// @ts-check

class UsgsQuakesMapCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  set hass(hass) {
    if (!this._config) return;
    this._render(hass);
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 4;
  }

  _render(hass) {
    const sensor = hass.states["sensor.usgs_quakes_latest"];
    if (!sensor) {
      this._renderError("Sensor not found: sensor.usgs_quakes_latest");
      return;
    }

    const events = sensor.attributes.events || [];
    const mapboxToken = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"; // fallback token
    const leafletLoaded = window.L;

    const mapId = "usgs_quakes_map";

    this.shadowRoot.innerHTML = `
      <ha-card header="USGS Quakes Map">
        <div id="${mapId}" style="height: 400px;"></div>
        <style>
          #${mapId} {
            border-radius: 8px;
          }
        </style>
      </ha-card>
    `;

    if (!leafletLoaded) {
      const leafletCss = document.createElement("link");
      leafletCss.rel = "stylesheet";
      leafletCss.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      this.shadowRoot.appendChild(leafletCss);

      const leafletScript = document.createElement("script");
      leafletScript.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
      leafletScript.onload = () => this._initMap(events, mapId);
      this.shadowRoot.appendChild(leafletScript);
    } else {
      this._initMap(events, mapId);
    }
  }

  _renderError(message) {
    this.shadowRoot.innerHTML = `
      <ha-card header="USGS Quakes Map">
        <div style="padding: 16px; color: red;">${message}</div>
      </ha-card>
    `;
  }

  _initMap(events, mapId) {
    const container = this.shadowRoot.getElementById(mapId);
    if (!container) return;

    // Clear previous map if exists
    if (this._map) {
      this._map.remove();
    }

    this._map = L.map(container).setView([0, 0], 2);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(this._map);

    const bounds = [];

    events.forEach((event) => {
      const coords = event.coordinates || [];
      const lat = coords[0];
      const lon = coords[1];
      if (lat == null || lon == null) return;

      const marker = L.marker([lat, lon]).addTo(this._map);
      const mag = event.magnitude || "?";
      const title = event.title || "Unknown";

      marker.bindPopup(`<strong>${title}</strong><br>Magnitude: ${mag}`);
      bounds.push([lat, lon]);
    });

    if (bounds.length) {
      this._map.fitBounds(bounds, { padding: [20, 20] });
    }
  }
}

customElements.define("usgs-quakes-map-card", UsgsQuakesMapCard);
