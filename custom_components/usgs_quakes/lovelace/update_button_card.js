// @ts-check

class UsgsQuakesUpdateButtonCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  set hass(hass) {
    if (!this._config) return;
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 1;
  }

  _render() {
    this.shadowRoot.innerHTML = `
      <ha-card>
        <div class="card-content">
          <mwc-button raised id="update-btn">Update Earthquake Feed</mwc-button>
        </div>
        <style>
          ha-card {
            padding: 16px;
            text-align: center;
          }
          mwc-button {
            --mdc-theme-primary: #2196f3;
          }
        </style>
      </ha-card>
    `;

    this.shadowRoot.querySelector("#update-btn").addEventListener("click", () => {
      this._hass.callService("usgs_quakes", "force_feed_update");
    });
  }
}

customElements.define("usgs-quakes-update-button-card", UsgsQuakesUpdateButtonCard);
