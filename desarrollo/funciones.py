import requests
import pandas as pd
import plotly.graph_objects as go

def fetch_query_aux(base_url="https://spmflotacionprod.azurewebsites.net/visualization/query-aux",
                    params=None,
                    timeout=10):
    """
    Consulta el endpoint 'query-aux' y devuelve los datos en formato JSON.

    Parámetros:
        base_url (str): URL del endpoint.
        params (dict): Parámetros de consulta GET (opcional).
        timeout (float|tuple): Segundos antes de timeout (pasar tuple para connect/read timeouts).

    Retorna:
        dict|list: Objeto JSON obtenido de la respuesta.

    Lanza:
        requests.exceptions.HTTPError: si la respuesta HTTP no es 2xx.
        requests.exceptions.RequestException: otros errores de conexión.
    """
    # Cabeceras habituales para recibir JSON
    headers = {
        "Accept": "application/json",
    }

    # Realiza la petición GET
    response = requests.get(base_url, headers=headers, params=params, timeout=timeout)
    # Lanza excepción si el código de estado es >=400
    response.raise_for_status()  # Para asegurar que errores HTTP no pasen inadvertidos :contentReference[oaicite:2]{index=2}

    # Decodifica y retorna el JSON
    return response.json()


def plot_dual_axis(  df: pd.DataFrame,   x_col: str,   y1_col: str,   y2_col: str = None, start_time: pd.Timestamp = None, end_time: pd.Timestamp = None
) -> go.Figure:
    """
    Grafica una serie temporal con dos ejes Y en Plotly.

    Parámetros:
        df (pd.DataFrame): DataFrame que contiene los datos.
        x_col (str): Nombre de la columna de fecha/hora para el eje X.
        y1_col (str): Nombre de la columna para el eje Y primario.
        y2_col (str, opcional): Nombre de la columna para el eje Y secundario. Si es None, solo un eje Y.
        start_time (pd.Timestamp o str, opcional): Fecha/hora de inicio para filtrar los datos.
        end_time (pd.Timestamp o str, opcional): Fecha/hora de fin para filtrar los datos.

    Retorna:
        go.Figure: Figura interactiva de Plotly.
    """
    try:
            # Copia para evitar SettingWithCopyWarning
            dfc = df.copy()
    
            # Conversión a datetime y filtrado
            dfc[x_col] = pd.to_datetime(dfc[x_col])
            if start_time is not None:
                dfc = dfc[dfc[x_col] >= pd.to_datetime(start_time)]
            if end_time is not None:
                dfc = dfc[dfc[x_col] <= pd.to_datetime(end_time)]
    
            # Construcción de la figura
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dfc[x_col],
                y=dfc[y1_col],
                name=y1_col,
                yaxis='y1',
                line=dict(width=2)
            ))
            if y2_col:
                fig.add_trace(go.Scatter(
                    x=dfc[x_col],
                    y=dfc[y2_col],
                    name=y2_col,
                    yaxis='y2',
                    line=dict(width=2 )# , dash='dash')
                ))
    
            # Layout de presentación con especificación correcta de fuentes de título
            layout = dict(
                template="plotly_white",
                width=1100, height=600,
                title=dict(
                    text=f"{y1_col}" + (f" vs {y2_col}" if y2_col else "") + f" sobre {x_col}",
                    x=0.5, font=dict(size=20)
                ),
                xaxis=dict(
                    title=dict(text=x_col, font=dict(size=16)),
                    tickformat="%b %Y",
                    tickfont=dict(size=12)
                ),
                yaxis=dict(
                    title=dict(text=y1_col, font=dict(size=16)),
                    tickfont=dict(size=12)
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom", y=1.02,
                    xanchor="center", x=0.5,
                    font=dict(size=12)
                ),
                margin=dict(l=80, r=80, t=100, b=80),
                hovermode="x unified"
            )
            if y2_col:
                layout['yaxis2'] = dict(
                    title=dict(text=y2_col, font=dict(size=16)),
                    overlaying='y',
                    side='right',
                    tickfont=dict(size=12),
                    showgrid=False
                )
    
            fig.update_layout(**layout)
    
            fig.show()
            #return fig
    
    except Exception as e:
        print(f"Error al generar la gráfica: {e}")
        return None