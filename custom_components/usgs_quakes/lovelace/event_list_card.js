class UsgsEventsListCard extends HTMLElement {
  setConfig(config) {
    this._config = config;
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  render() {
    if (!this._hass || !this._config?.entity) return;

    const events = this._hass.states[this._config.entity]?.attributes?.events || [];

    this.innerHTML = `
      <ha-card header="USGS Earthquake Events">
        <div class="card-content">
          ${events.length === 0
            ? "<p>No recent events.</p>"
            : events.map(event => `
                <div style="margin-bottom: 1em">
                  <strong>${event.title}</strong><br />
                  Place: ${event.place}<br />
                  Magnitude: ${event.magnitude} Mw<br />
                  Date/Time: ${new Date(event.time).toLocaleString()}<br />
                  Location: <a href="https://www.google.com/maps?q=${event.coordinates[0]},${event.coordinates[1]}" target="_blank">Map</a>
                </div>
              `).join('')}
        </div>
      </ha-card>
    `;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('usgs-events-list-card', UsgsEventsListCard);
