(() => {
  "use strict";

  const CARD_TYPE = "btc-address-card";
  const EDITOR_TYPE = `${CARD_TYPE}-editor`;
  const VERSION = "0.9.9.g";

  const isAddressEntity = (state) =>
    !!(
      state &&
      state.attributes &&
      Object.prototype.hasOwnProperty.call(
        state.attributes,
        "unconfirmed_count"
      )
    );

  const fmtBtc = (value) => {
    const n = Number(value);
    return Number.isFinite(n) ? n.toFixed(8) : "—";
  };

  const fmtSigned = (value) => {
    const n = Number(value);

    if (!Number.isFinite(n)) {
      return "—";
    }

    const s = n.toFixed(8);
    return n > 0 ? `+${s}` : s;
  };

  const shortAddr = (address) => {
    if (!address || address.length < 20) {
      return address || "";
    }

    return `${address.slice(0, 10)}…${address.slice(-8)}`;
  };

  const t = (hass, de, en) => {
    const language = (
      hass?.locale?.language ||
      hass?.language ||
      "en"
    ).toLowerCase();

    return language.startsWith("de") ? de : en;
  };

  class BtcAddressCard extends HTMLElement {
    static getConfigElement() {
      return document.createElement(EDITOR_TYPE);
    }

    static getStubConfig(hass) {
      const entity =
        Object.keys(hass?.states || {}).find(
          (entityId) =>
            isAddressEntity(
              hass.states[entityId]
            )
        ) || "";

      return {
        entity,
        font_size: 100,
      };
    }

    setConfig(config) {
      if (!config?.entity) {
        throw new Error("You need to define an entity");
      }

      this._config = {
        font_size: 100,
        ...config,
      };

      this._render();
    }

    set hass(hass) {
      this._hass = hass;
      this._render();
    }

    getCardSize() {
      return 3;
    }

    getGridOptions() {
      return {
        rows: 4,
        columns: 12,
        min_rows: 4,
        min_columns: 6,
        max_columns: 24,
      };
    }

    _render() {
      if (!this._config) {
        return;
      }

      if (!this._root) {
        this._root = this.attachShadow({
          mode: "open",
        });
      }

      const hass = this._hass;
      const entity = this._config.entity;
      const state = hass?.states?.[entity];
      const attrs = state?.attributes || {};

      let name =
        this._config.name ||
        attrs.friendly_name ||
        entity ||
        t(hass, "BTC-Adresse", "BTC address");

      if (
        hass?.formatEntityName &&
        state &&
        this._config.name
      ) {
        try {
          name = hass.formatEntityName(
            state,
            this._config.name
          );
        } catch {
          name =
            attrs.friendly_name ||
            entity;
        }
      }

      const confirmed = state?.state ?? null;
      const pendingIn = attrs.pending_incoming;
      const pendingOut = attrs.pending_outgoing;
      const pendingChange = attrs.pending_change;
      const unconfirmed = attrs.unconfirmed_count;
      const address = attrs.address || "";

      const changeNum = Number(pendingChange);

      const changeClass =
        changeNum > 0
          ? "pos"
          : changeNum < 0
            ? "neg"
            : "";

      const unavailable =
        !state ||
        confirmed === "unavailable" ||
        confirmed === "unknown";

      const configuredFontSize =
        Number(this._config.font_size);

      const fontSize =
        Number.isFinite(configuredFontSize)
          ? Math.min(
              150,
              Math.max(70, configuredFontSize)
            )
          : 100;

      const fontScale = fontSize / 100;

      this._root.innerHTML = `
        <style>
          :host {
            display: block;
            width: 100%;
            height: 100%;
            min-width: 0;
            min-height: 0;
            box-sizing: border-box;
            font-size: calc(1rem * ${fontScale});
          }

          ha-card {
            display: flex;
            flex-direction: column;
            width: 100%;
            height: 100%;
            min-width: 0;
            min-height: 0;
            box-sizing: border-box;
            overflow: hidden;
            cursor: pointer;
          }

          .wrap {
            display: flex;
            flex-direction: column;
            flex: 1 1 auto;
            width: 100%;
            min-width: 0;
            min-height: 0;
            box-sizing: border-box;
            padding: 16px;
          }

          .head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            min-width: 0;
          }

          .head > div:first-child {
            min-width: 0;
          }

          .title {
            font-weight: 500;
            font-size: 1.05em;
            line-height: 1.3;
            color: var(--primary-text-color);
          }

          .addr {
            margin-top: 2px;
            font-family:
              var(--code-font-family, monospace);
            font-size: 0.75em;
            color: var(--secondary-text-color);
            word-break: break-all;
          }

          .badge {
            flex-shrink: 0;
            font-size: 0.75em;
            padding: 2px 8px;
            border-radius: 999px;
            background: var(--secondary-background-color);
            color: var(--secondary-text-color);
          }

          .badge.hot {
            background:
              color-mix(
                in srgb,
                var(--warning-color) 22%,
                transparent
              );
            color: var(--warning-color);
          }

          .balance {
            margin: 14px 0 4px;
            font-size: 1.7em;
            font-weight: 650;
            letter-spacing: -0.02em;
            font-variant-numeric: tabular-nums;
            color: var(--primary-text-color);
          }

          .unit {
            font-size: 0.85em;
            font-weight: 500;
            margin-left: 4px;
            color: var(--secondary-text-color);
          }

          .warn {
            color: var(--secondary-text-color);
            padding: 16px;
          }

          .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px 12px;
            margin-top: auto;
            padding-top: 12px;
            border-top: 1px solid var(--divider-color);
          }

          .item {
            min-width: 0;
          }

          .item .lbl {
            font-size: 0.72em;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--secondary-text-color);
          }

          .item .val {
            margin-top: 2px;
            font-variant-numeric: tabular-nums;
            font-size: 0.95em;
            font-weight: 500;
            color: var(--primary-text-color);
          }

          .pos {
            color: var(--success-color, #4caf50);
          }

          .neg {
            color: var(--error-color, #f44336);
          }
        </style>

        <ha-card>
          ${
            unavailable
              ? `
                <div class="warn">
                  ${t(
                    hass,
                    "Entity nicht verfügbar:",
                    "Entity unavailable:"
                  )}
                  ${this._esc(entity)}
                </div>
              `
              : `
                <div class="wrap">

                  <div class="head">

                    <div>

                      <div class="title">
                        ${this._esc(name)}
                      </div>

                      <div
                        class="addr"
                        title="${this._esc(address)}"
                      >
                        ${this._esc(
                          shortAddr(address)
                        )}
                      </div>

                    </div>

                    <div
                      class="badge ${
                        Number(unconfirmed) > 0
                          ? "hot"
                          : ""
                      }"
                    >
                      ${Number(unconfirmed) || 0} TX
                    </div>

                  </div>

                  <div class="balance">
                    ${fmtBtc(confirmed)}
                    <span class="unit">BTC</span>
                  </div>

                  <div class="grid">

                    <div class="item">
                      <div class="lbl">
                        ${t(
                          hass,
                          "Eingang unbestätigt",
                          "Pending in"
                        )}
                      </div>

                      <div
                        class="val ${
                          Number(pendingIn) > 0
                            ? "pos"
                            : ""
                        }"
                      >
                        ${fmtBtc(pendingIn)}
                      </div>
                    </div>

                    <div class="item">
                      <div class="lbl">
                        ${t(
                          hass,
                          "Ausgang unbestätigt",
                          "Pending out"
                        )}
                      </div>

                      <div
                        class="val ${
                          Number(pendingOut) > 0
                            ? "neg"
                            : ""
                        }"
                      >
                        ${fmtBtc(pendingOut)}
                      </div>
                    </div>

                    <div class="item">
                      <div class="lbl">
                        ${t(
                          hass,
                          "Netto pending",
                          "Net pending"
                        )}
                      </div>

                      <div class="val ${changeClass}">
                        ${fmtSigned(pendingChange)}
                      </div>
                    </div>

                    <div class="item">
                      <div class="lbl">
                        ${t(
                          hass,
                          "Bestätigt",
                          "Confirmed"
                        )}
                      </div>

                      <div class="val">
                        ${fmtBtc(
                          attrs.confirmed_balance ??
                          confirmed
                        )}
                      </div>
                    </div>

                  </div>

                </div>
              `
          }
        </ha-card>
      `;

      const card =
        this._root.querySelector("ha-card");

      if (card) {
        card.onclick = () => {
          this.dispatchEvent(
            new CustomEvent("hass-more-info", {
              bubbles: true,
              composed: true,
              detail: {
                entityId: entity,
              },
            })
          );
        };
      }
    }

    _esc(value) {
      return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }
  }

  class BtcAddressCardEditor extends HTMLElement {
    constructor() {
      super();

      this._config = {};
      this._hass = null;
      this._container = null;
      this._picker = null;
      this._name = null;
      this._theme = null;
      this._font = null;
    }

    setConfig(config) {
      this._config = {
        font_size: 100,
        ...config,
      };

      this._render();
    }

    set hass(hass) {
      this._hass = hass;
      this._render();
    }

    _render() {
      if (!this._hass) {
        return;
      }

      if (!this._container) {
        this.innerHTML = "";

        this._container =
          document.createElement("div");

        this._container.style.display = "grid";
        this._container.style.gap = "16px";

        /*
         * BTC ENTITY PICKER
         *
         * HA-Komponente.
         * Nur Sensoren mit unconfirmed_count.
         */

        this._picker =
          document.createElement(
            "ha-entity-picker"
          );

        this._picker.hass = this._hass;
        this._picker.allowCustomEntity = false;
        this._picker.includeDomains = ["sensor"];

        this._picker.entityFilter = (state) =>
          isAddressEntity(state);

        this._picker.addEventListener(
          "value-changed",
          (event) => {
            event.stopPropagation();

            this._update({
              entity:
                event.detail?.value || "",
            });
          }
        );

        /*
         * NAME
         */

        this._name =
          document.createElement(
            "ha-selector"
          );

        this._name.selector = {
          entity_name: {},
        };

        this._name.addEventListener(
          "value-changed",
          (event) => {
            event.stopPropagation();

            this._update({
              name:
                event.detail?.value ||
                undefined,
            });
          }
        );

        /*
         * DESIGN / THEME
         */

        this._theme =
          document.createElement(
            "ha-selector"
          );

        this._theme.selector = {
          theme: {},
        };

        this._theme.addEventListener(
          "value-changed",
          (event) => {
            event.stopPropagation();

            this._update({
              theme:
                event.detail?.value ||
                undefined,
            });
          }
        );

        /*
         * SCHRIFTGRÖSSE
         */

        this._font =
          document.createElement(
            "ha-selector"
          );

        this._font.selector = {
          number: {
            min: 70,
            max: 150,
            step: 5,
            mode: "slider",
            unit_of_measurement: "%",
          },
        };

        this._font.addEventListener(
          "value-changed",
          (event) => {
            event.stopPropagation();

            const value =
              Number(
                event.detail?.value
              );

            if (!Number.isFinite(value)) {
              return;
            }

            this._update({
              font_size: Math.min(
                150,
                Math.max(70, value)
              ),
            });
          }
        );

        this._container.append(
          this._picker,
          this._name,
          this._theme,
          this._font
        );

        this.appendChild(
          this._container
        );
      }

      this._picker.hass =
        this._hass;

      this._picker.value =
        this._config.entity || "";

      this._picker.label =
        t(
          this._hass,
          "BTC-Adresse",
          "BTC address"
        );

      this._name.hass =
        this._hass;

      this._name.value =
        this._config.name || "";

      this._name.label =
        t(
          this._hass,
          "Name",
          "Name"
        );

      this._theme.hass =
        this._hass;

      this._theme.value =
        this._config.theme || "";

      this._theme.label =
        t(
          this._hass,
          "Design",
          "Theme"
        );

      this._font.hass =
        this._hass;

      this._font.value =
        Number.isFinite(
          Number(this._config.font_size)
        )
          ? Math.min(
              150,
              Math.max(
                70,
                Number(this._config.font_size)
              )
            )
          : 100;

      this._font.label =
        t(
          this._hass,
          "Schriftgröße",
          "Font size"
        );
    }

    _update(changes) {
      this._config = {
        ...this._config,
        ...changes,
      };

      if (!this._config.name) {
        delete this._config.name;
      }

      if (!this._config.theme) {
        delete this._config.theme;
      }

      this.dispatchEvent(
        new CustomEvent(
          "config-changed",
          {
            bubbles: true,
            composed: true,
            detail: {
              config: this._config,
            },
          }
        )
      );
    }
  }

  if (!customElements.get(CARD_TYPE)) {
    customElements.define(
      CARD_TYPE,
      BtcAddressCard
    );
  }

  if (!customElements.get(EDITOR_TYPE)) {
    customElements.define(
      EDITOR_TYPE,
      BtcAddressCardEditor
    );
  }

  window.customCards =
    window.customCards || [];

  window.customCards.push({
    type: CARD_TYPE,
    name: "BTC Address Card",
    preview: true,
    description:
      "Bestätigter Saldo und unbestätigte Ein-/Ausgänge (Mempool Watch)",
    documentationURL:
      "https://github.com/jinx-22/btc-address-card",
  });

  console.info(
    `%c BTC Address Card %c v${VERSION} `,
    "color:white;background:#f7931a;font-weight:bold;",
    "color:#f7931a;background:white;font-weight:bold;"
  );
})();