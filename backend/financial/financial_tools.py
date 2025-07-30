import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from langchain_community.tools.polygon import PolygonAggregates
from langchain_community.utilities.polygon import PolygonAPIWrapper

# Cargar configuración
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')
polygon_wrapper = PolygonAPIWrapper(polygon_api_key=os.getenv("POLYGON_API_KEY"))
polygon_tool = PolygonAggregates(api_wrapper=polygon_wrapper)

def get_best_symbol(company_name: str) -> str:
    """
    Busca el mejor símbolo usando Twelve Data
    Prioriza: NYSE/NASDAQ > otros mercados > símbolos cortos y limpios
    """
    try:
        response = requests.get(
            "https://api.twelvedata.com/symbol_search",
            params={'symbol': company_name, 'apikey': os.getenv("TWELVE_DATA_API_KEY")},
            timeout=8
        )
        
        results = response.json().get('data', [])
        if not results:
            print(f"❌ No se encontraron símbolos para '{company_name}'")
            return None
            
        # Elegir el mejor símbolo priorizando mercados con cobertura de Polygon
        best = max(results, key=lambda x: (
            x.get('exchange') in ['NYSE', 'NASDAQ'],  # Máxima prioridad: mercados US principales
            x.get('exchange') in ['AMEX', 'OTC'],     # Alta prioridad: otros mercados US
            len(x.get('symbol', '')) <= 5,           # Bonus: símbolos cortos (más confiables)
            x.get('symbol', '').isalpha()            # Bonus: solo letras (evita derivados)
        ))
        
        symbol = best.get('symbol')
        exchange = best.get('exchange')
        print(f"✅ {company_name} → {symbol} ({exchange})")
        return symbol
        
    except Exception as e:
        print(f"❌ Error buscando símbolos para '{company_name}': {e}")
        return None

def get_polygon_data(symbol: str) -> dict:
    """
    Obtiene datos de Polygon (única fuente de datos de precios)
    """
    try:
        # Configurar rango de fechas (últimos 5 días)
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        result = polygon_tool.run({
            "ticker": symbol,
            "timespan": "day", 
            "timespan_multiplier": 1,
            "from_date": start_date,
            "to_date": end_date
        })
        
        # Verificar si tenemos datos válidos
        if isinstance(result, dict) and result.get("results"):
            print(f"✅ Polygon exitoso: {symbol}")
            return {"data": result, "success": True}
            
    except Exception as e:
        # Manejar el caso especial donde Polygon devuelve datos en el mensaje de error
        if "API Error:" in str(e) and "{" in str(e):
            try:
                import ast
                dict_str = str(e)[str(e).find("{"):]
                result = ast.literal_eval(dict_str)
                if result.get("results"):
                    print(f"✅ Polygon datos extraídos: {symbol}")
                    return {"data": result, "success": True}
            except:
                pass
    
    print(f"❌ Polygon sin datos para {symbol}")
    return {"success": False}

def get_stock_data(company_name: str) -> dict:
    """
    Función principal: Obtiene datos financieros para una empresa
    
    Proceso:
    1. Buscar símbolo con Twelve Data (solo búsqueda, plan gratuito)
    2. Obtener datos con Polygon (única fuente de precios)
    3. Si no hay datos, respuesta elegante para análisis general
    """
    
    # 1. Buscar símbolo
    symbol = get_best_symbol(company_name)
    if not symbol:
        return {
            "symbol": "UNKNOWN",
            "company_name": company_name,
            "success": False,
            "error": "Company symbol not found",
            "timestamp": datetime.now().isoformat(),
            "source": "none"
        }
    
    print(f"📊 Obteniendo datos financieros para: {symbol}")

    # 2. Obtener datos de Polygon
    polygon_result = get_polygon_data(symbol)
    if polygon_result.get("success"):
        return {
            "symbol": symbol,
            "company_name": company_name,
            "raw_data": polygon_result["data"],
            "success": True,
            "source": "polygon",
            "timestamp": datetime.now().isoformat()
        }
    
    # 3. Sin datos de Polygon (mercados no cubiertos)
    return {
        "symbol": symbol,
        "company_name": company_name,
        "success": False,
        "error": "Market data not available - Polygon covers primarily US markets",
        "source": "none",
        "timestamp": datetime.now().isoformat()
    }

def format_market_data_for_llm(stock_data: dict) -> str:
    """
    Formatea los datos del mercado para que sean comprensibles por el LLM
    """
    symbol = stock_data.get('symbol', 'UNKNOWN')
    company_name = stock_data.get('company_name', 'empresa')

    # Caso 1: Sin datos disponibles
    if not stock_data.get("success", False):
        if symbol == "UNKNOWN":
            # No mencionar símbolo si no se encontró
            return f"""
DATOS FINANCIEROS DE {company_name.upper()}:

Estado: Datos de precios no disponibles
Empresa: {company_name}
Símbolo: No encontrado en bases de datos financieras

Nota: Genera análisis general sobre {company_name} sin mencionar símbolos específicos ni precios.
Enfócate en información corporativa, sector, tendencias del mercado y contexto general de la empresa.

Motivo: {stock_data.get('error', 'Datos no disponibles')}
            """.strip()
        else:
            # Símbolo encontrado pero sin datos de mercado
            return f"""
DATOS FINANCIEROS DE {symbol}:

Estado: Datos de precios no disponibles
Empresa: {company_name}
Símbolo encontrado: {symbol}

Nota: Genera análisis general sobre {company_name} ({symbol}) sin mencionar precios específicos.
Enfócate en información corporativa, sector, tendencias del mercado y contexto general de la empresa.

Motivo: {stock_data.get('error', 'Datos no disponibles')}
            """.strip()

    # Caso 2: Datos de Polygon disponibles
    raw_data = stock_data.get("raw_data", {})
    results = raw_data.get("results", [])
    
    if not results:
        return f"DATOS FINANCIEROS DE {symbol}: Datos de Polygon incompletos"
        
    latest = results[-1]
    o = latest.get("o")  # open
    c = latest.get("c")  # close
    h = latest.get("h")  # high
    l = latest.get("l")  # low
    v = latest.get("v")  # volume

    # Calcular métricas
    pct_change = f"{((c - o) / o * 100):.2f}%" if o and c else "N/A"
    volume_formatted = f"{int(v):,}" if v else "N/A"
    
    return f"""
DATOS FINANCIEROS DE {symbol} (Polygon):

Empresa: {company_name}
Símbolo: {symbol}

Precio de apertura: ${o}
Precio de cierre: ${c}
Rango del día: ${l} - ${h}
Cambio porcentual: {pct_change}
Volumen: {volume_formatted}

INSTRUCCIONES PARA EL ANÁLISIS:
- Usa estos datos reales y actualizados para crear análisis específico
- Menciona los precios, cambios porcentuales y volumen en tu análisis
- Proporciona contexto sobre el rendimiento de la acción
- Relaciona los datos con tendencias del mercado cuando sea relevante
    """.strip()