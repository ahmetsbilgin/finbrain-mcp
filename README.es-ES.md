

# FinBrain MCP&nbsp;<!-- omit in toc -->

[![PyPI version](https://img.shields.io/pypi/v/finbrain-mcp.svg)](https://pypi.org/project/finbrain-mcp/)
[![CI](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

> **Requiere Python 3.10+**

Un servidor de **Model Context Protocol (MCP)** que expone los conjuntos de datos de FinBrain a clientes de IA (Claude Desktop, extensiones MCP de VS Code, etc.) mediante herramientas simples.
Respaldado por el SDK oficial de **`finbrain-python`** (API v2).

- Nombre del paquete: **`finbrain-mcp`**

- Punto de entrada de CLI: **`finbrain-mcp`**

- Documentación: **[finbrain.tech/integrations/mcp](https://finbrain.tech/integrations/mcp/)**

----------

## Características

### Predicciones de precios impulsadas por IA

Acceda a los pronósticos de precios de aprendizaje automático de FinBrain con horizontes diarios (10 días) y mensuales (12 meses). Incluye predicciones medias con intervalos de confianza del 95%.

### Análisis de noticias y sentimiento

Navegue por artículos de noticias recientes para cualquier valor, o siga las puntuaciones de sentimiento diario agregadas a lo largo del tiempo. Filtre noticias en todas las acciones supervisadas.

### Datos alternativos

- **Métricas de LinkedIn** — Número de empleados y tendencias de seguidores como indicadores de salud empresarial
- **Calificaciones de App Store** — Datos de rendimiento de aplicaciones móviles para empresas orientadas al consumidor
- **Flujo de opciones** — Relación put/call y volumen para medir la posición en el mercado
- **Menciones en Reddit** — Recuento de menciones de valores en subreddits, recopiladas cada 4 horas
- **Contratos gubernamentales** — Adjudicaciones de contratos del gobierno de EE. UU. desde USAspending.gov
- **Solicitudes de patentes** — Patentes concedidas por la USPTO mapeadas a valores por cesionario corporativo, con clasificación CPC

### Actividad institucional y de insiders

- **Operaciones del Congreso de EE. UU.** — Transacciones de valores reveladas por representantes de la Cámara y senadores, con la fecha de la transacción y la fecha de divulgación pública (para que pueda medir el retraso en el reporte), el titular beneficiario de la cuenta operada (miembro, cónyuge, hijo dependiente, conjunta o un código de cuenta) y los montos declarados normalizados según las bandas de la Ley STOCK, manteniendo la declaración original
- **Lobby corporativo** — Declaraciones de lobby con registrante, ingresos, gastos y códigos de tema
- **Transacciones de insiders** — Formularios SEC Form 4 que muestran compras y ventas de ejecutivos
- **Calificaciones de analistas** — Cobertura de Wall Street y cambios en los objetivos de precio

----------

## Qué obtienes

- ⚡️ Servidor MCP **local** (sin proxy) que utiliza **tu propia clave API de FinBrain**

- 🧰 Herramientas (JSON por defecto, CSV opcional) con paginación

  - `health`

  - `available_markets`, `available_tickers`, `available_regions`

  - `predictions_by_market`, `predictions_by_ticker`

  - `news_by_ticker`, `news_sentiment_by_ticker`

  - `app_ratings_by_ticker`

  - `analyst_ratings_by_ticker`

  - `house_trades_by_ticker`, `senate_trades_by_ticker`

  - `corporate_lobbying_by_ticker`

  - `insider_transactions_by_ticker`

  - `linkedin_metrics_by_ticker`

  - `options_put_call`

  - `reddit_mentions_by_ticker`

  - `government_contracts_by_ticker`

  - `patent_filings_by_ticker`

  - `recent_news`, `recent_analyst_ratings`

  - `screener_sentiment`, `screener_analyst_ratings`, `screener_news`

  - `screener_insider_trading`, `screener_house_trades`, `screener_senate_trades`

  - `screener_put_call_ratio`, `screener_linkedin`, `screener_app_ratings`, `screener_reddit_mentions`, `screener_government_contracts`, `screener_patent_filings`

- 🧹 Formatos coherentes y amigables para modelos (normalizamos las respuestas crudas de la API)

- 🔑 Proporcione su clave API mediante la variable de entorno `FINBRAIN_API_KEY` (una variable de entorno de shell o el bloque `env` de su cliente MCP)

----------

## Instalación

### Opción A — Instalación estándar (pip)

```bash
# macOS / Linux / Windows
pip install --upgrade finbrain-mcp
```

### Opción B — Instalación para desarrollo (editable)

```bash
# desde la raíz del repositorio
python -m venv .venv
source .venv/bin/activate # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"
```

> Mantenga **pip** (producción) y su **venv** (desarrollo) separados para evitar confusiones en las rutas.

### Opción C — Docker

```bash
# Construir la imagen
docker build -t finbrain-mcp:latest .

# Ejecutar con su clave API
docker run --rm -e FINBRAIN_API_KEY="YOUR_KEY" finbrain-mcp:latest
```

> Consulte [DOCKER.md](DOCKER.md) para obtener instrucciones detalladas de uso de Docker.

----------

## Configure su clave API de FinBrain

### A) En la configuración de su cliente MCP (recomendado / más confiable)

Coloque la clave directamente en la entrada del servidor MCP que utiliza su cliente (Claude Desktop o una extensión MCP de VS Code). Esto garantiza que el servidor iniciado la vea, incluso si las variables de entorno del sistema no se capturan.

#### Claude Desktop (instalación con pip)

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

### B) Variable de entorno

Esto también funciona, pero tenga en cuenta que debe reiniciar el cliente después de configurarla para que se herede el nuevo valor.

```bash
# macOS/Linux
export FINBRAIN_API_KEY="YOUR_KEY"

# Windows (PowerShell, sesión actual)
$env:FINBRAIN_API_KEY="YOUR_KEY"

# Windows (persistente para nuevos procesos)
setx FINBRAIN_API_KEY "YOUR_KEY"
# luego salga completamente y vuelva a abrir su cliente MCP (por ejemplo, Claude Desktop)
```

>**Consejo:** Si la ruta de la variable de entorno no parece funcionar (común en Windows si el cliente ya estaba en ejecución), use el método **`env` del JSON de configuración** anterior; es más determinista.
----------

## Ejecutar el servidor

> **Nota:** Por lo general, no necesita ejecutar el servidor manualmente; su cliente MCP (Claude/VS Code) lo inicia automáticamente. Use los comandos a continuación solo para verificaciones manuales o depuración.

- Si está instalado (pip):

    `finbrain-mcp`

- Desde un venv de desarrollo:

    `python -m finbrain_mcp.server`

Verificación rápida de estado sin un cliente MCP:

```python
python - <<'PY'
import json
from finbrain_mcp.tools.health import health
print(json.dumps(health(), indent=2))
PY
```

----------

## Conectar un cliente de IA

> **No se requiere inicio manual:** Claude Desktop y VS Code **iniciarán el servidor MCP por usted** según su configuración. Solo necesita ejecutar `finbrain-mcp` usted mismo para verificaciones rápidas o depuración.

### Claude Desktop

Edite su configuración:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

- Linux: `~/.config/Claude/claude_desktop_config.json`

**Instalación con pip (paquete publicado):**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}

```

**Consejo para macOS (ruta completa):**

Si `"command": "finbrain-mcp"` no funciona, busque la ruta absoluta y úsela en su lugar.

```bash
which finbrain-mcp    # macOS/Linux
# (Windows: where finbrain-mcp)
```

**Configuración de Claude con ruta completa (ejemplo para macOS):**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "/full/path/to/finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

**Venv de desarrollo (ejecutar el módulo explícitamente):**

```json
{
  "mcpServers": {
    "finbrain-dev": {
      "command": "C:\\Users\\you\\path\\to\\repo\\.venv\\Scripts\\python.exe",
      "args": ["-m", "finbrain_mcp.server"],
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

**Docker:**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "finbrain-mcp:latest"],
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

> Después de editar, **salga y vuelva a abrir Claude**.

### VS Code (MCP)

1. Abra la Paleta de Comandos → **“MCP: Open User Configuration”**.  
   Esto abre su `mcp.json` (perfil de usuario).
2. Agregue el servidor bajo la clave **`servers`**:

    ```json
    {
      "servers": {
        "finbrain": {
          "command": "finbrain-mcp",
          "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
        }
      }
    }
    ```

3. En Copilot Chat, habilite el modo Agente para usar las herramientas MCP.

----------

## ¿Qué puede preguntarle al agente?

No necesita conocer los nombres de las herramientas, simplemente pregunte en lenguaje natural. Ejemplos:

- **Predicciones**
  - “Obtén las **predicciones diarias** de FinBrain para **AMZN**.”
  - “Muestra las **predicciones mensuales** (horizonte de 12 meses) para **AMZN**.”
  - “Obtén **predicciones diarias a nivel de mercado** para los valores del **S&P 500**.”

- **Noticias**
  - “Obtén **artículos de noticias recientes** para **AMZN**.”
  - “¿Cuál es el **sentimiento de noticias** para **AMZN** **desde el 2025-01-01 hasta el 2025-03-31** (límite 50)?”
  - “Muéstrame las **últimas noticias** en todas las acciones del **S&P 500**.”

- **Calificaciones de aplicaciones**
  - “Obtén las **calificaciones de la tienda de aplicaciones** para **AMZN** entre el **2025-01-01** y el **2025-06-30**.”

- **Calificaciones de analistas**
  - “Lista las **calificaciones de analistas** para **AMZN** en el **Q1 2025**.”

- **Operaciones del Congreso**
  - “Muestra **operaciones recientes de la Cámara** que involucren a **AMZN**.”
  - “Muestra **operaciones recientes del Senado** que involucren a **META**.”
  - “Para las operaciones de la Cámara de **NVDA**, ¿cuánto tiempo tardó cada miembro en **divulgar** la operación?”
  - “¿Cuáles de las **operaciones recientes del Senado** se realizaron a través de una cuenta de **cónyuge o conjunta**?”

- **Lobby corporativo**
  - “Muestra las **declaraciones de lobby corporativo** para **AAPL**.”
  - “¿Qué **firmas de lobby** ha utilizado **MSFT** en **2024** (desde el 2024-01-01 hasta el 2024-12-31)?”

- **Transacciones de insiders**
  - “¿Transacciones recientes de **insiders** para **AMZN**?”

- **Métricas de LinkedIn**
  - “Obtén el **recuento de empleados y seguidores de LinkedIn** para **AMZN** (últimos 12 meses).”

- **Opciones (put/call)**
  - “¿Cuál es la **relación put/call** para **AMZN** durante los **últimos 60 días**?”

- **Menciones en Reddit**
  - “Muestra **menciones en Reddit** para **TSLA** durante la **última semana**.”
  - “¿Qué **subreddits** están hablando más sobre **AAPL**?”

- **Contratos gubernamentales**
  - “Muestra **contratos gubernamentales** adjudicados a **LMT** en **2025**.”
  - “¿Qué empresas tienen las **mayores adjudicaciones de contratos gubernamentales**?”

- **Solicitudes de patentes**
  - “Muestra **solicitudes de patentes recientes** para **AAPL**.”
  - “¿Qué empresas han obtenido **más patentes concedidas** recientemente?”

- **Filtros (multivalor)**
  - “Filtra el **sentimiento** en las acciones del **S&P 500**.”
  - “Muestra las **últimas calificaciones de analistas** en todas las acciones.”
  - “Filtra **operaciones de insiders** en todos los valores (límite 50).”
  - “Filtra **datos de LinkedIn** para acciones de la región **EE. UU.**.”
  - “¿Cuáles son los **valores más mencionados** en **Reddit** en este momento?”
  - “¿Qué empresas están presentando **más patentes** en este momento?”

- **Disponibilidad**
  - “¿Qué **mercados** están disponibles?”
  - “Lista los **valores** en el universo de predicciones **diarias**.”
  - “Muestra las **regiones** disponibles y sus mercados.”

> **Notas**
>
> - Formato de fecha: `YYYY-MM-DD`.
> - Los endpoints de series temporales devuelven por defecto los **últimos N** puntos; diga “limit 200” para obtener más.
> - Horizonte de predicciones: **diario** (10 días) o **mensual** (12 meses).
> - Diga “**as CSV**” para recibir CSV en lugar de JSON.
> - No es necesario especificar un mercado, simplemente use el símbolo del valor directamente.

----------

## Desarrollo

```bash
# configuración
python -m venv .venv
source .venv/bin/activate # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"  # ejecutar pruebas pytest -q
```

### Estructura del proyecto (alto nivel)

```text
finbrain-mcp
├─ README.md
├─ pyproject.toml
├─ LICENSE
├─ .github/
├─ examples/
├─ src/
│  └─ finbrain_mcp/
│     ├─ __init__.py
│     ├─ server.py                # Punto de entrada del servidor MCP
│     ├─ registry.py              # Instancia FastMCP
│     ├─ client_adapter.py        # envuelve finbrain-python; almacena en caché el cliente SDK; llama a normalizadores
│     ├─ auth.py                  # resuelve la clave API (variable de entorno)
│     ├─ utils.py                 # helpers (latest_slice, CSV, DF->records)
│     ├─ normalizers/             # formateadores específicos de endpoint
│     └─ tools/                   # funciones de herramientas MCP (registradas y probables)
└─ tests/                         # suite pytest con un SDK ficticio
```

----------

## Solución de problemas

- **`ENOENT`** (no se puede iniciar el servidor)

  - Ruta incorrecta en la configuración del cliente. Use la ruta **exacta** del venv:

    - `…\.venv\Scripts\python.exe` + `[“-m”,”finbrain_mcp.server”]`, o

    - `…\.venv\Scripts\finbrain-mcp.exe`

- **`FinBrain API key not configured`**

  - Coloque `FINBRAIN_API_KEY` en el bloque `env` del cliente **o**

  - `setx FINBRAIN_API_KEY "YOUR_KEY"` y reinicie completamente el cliente.

- **Mezclar instalaciones de dev y prod**

  - Mantenga **pip** (producción) y **venv** (desarrollo) separados.

  - En las configuraciones, apunte a una u otra, no a ambas.

----------

## Licencia

MIT (ver `LICENSE`).

----------

## Agradecimientos

- Construido sobre Model Context Protocol y **FastMCP**.

- Utiliza el SDK oficial de **`finbrain-python`**.

----------

© 2026 FinBrain Technologies — Construido con ❤️ para la comunidad de cuantitativos.
