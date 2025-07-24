import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from langchain_community.tools.polygon import PolygonAggregates
from langchain_community.utilities.polygon import PolygonAPIWrapper

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

# Configurar la conexión con Polygon.io usando LangChain
polygon_wrapper = PolygonAPIWrapper(polygon_api_key=os.getenv("POLYGON_API_KEY"))
polygon_tool = PolygonAggregates(api_wrapper=polygon_wrapper)

def search_symbol_with_twelve_data(company_name: str) -> str:
    """
    Busca el símbolo de stock usando Twelve Data API (gratuito, sin API key)
    """
    try:
        url = f"https://api.twelvedata.com/symbol_search?symbol={company_name}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, timeout=8, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', [])
            
            if results:
                # Priorizar NYSE/NASDAQ para Polygon, pero aceptar otros para backup
                preferred_exchanges = ['NYSE', 'NASDAQ', 'AMEX']
                secondary_exchanges = ['MCE', 'BME', 'MTA', 'LSE', 'FRA']  # Europeas para Twelve Data
                
                polygon_compatible = []
                twelve_data_compatible = []
                
                for result in results:
                    exchange = result.get('exchange', '')
                    symbol = result.get('symbol', '')
                    instrument_name = result.get('instrument_name', '')
                    
                    if exchange in preferred_exchanges:
                        polygon_compatible.append({
                            'symbol': symbol,
                            'name': instrument_name,
                            'exchange': exchange,
                            'api_preference': 'polygon'
                        })
                    elif exchange in secondary_exchanges:
                        twelve_data_compatible.append({
                            'symbol': symbol,
                            'name': instrument_name,
                            'exchange': exchange,
                            'api_preference': 'twelve_data'
                        })
                
                # Preferir símbolos compatibles con Polygon
                if polygon_compatible:
                    best_match = polygon_compatible[0]
                else:
                    best_match = twelve_data_compatible[0] if twelve_data_compatible else results[0]
                    best_match['api_preference'] = 'twelve_data'
                
                symbol = best_match['symbol']
                name = best_match.get('name', best_match.get('instrument_name', company_name))
                exchange = best_match.get('exchange', 'Unknown')
                
                print(f"✅ Encontrado: {name} -> {symbol} ({exchange})")
                return symbol
        
        return None
        
    except Exception as e:
        print(f"❌ Error con Twelve Data: {e}")
        return None

def get_twelve_data_prices(symbol: str) -> dict:
    """
    Obtiene datos de precios usando Twelve Data API como backup de Polygon
    """
    try:
        # Usar time_series endpoint para datos históricos
        url = f"https://api.twelvedata.com/time_series"
        params = {
            'symbol': symbol,
            'interval': '1day',
            'outputsize': '10',  # Últimos 10 días
            'format': 'json',
            'apikey': os.getenv("TWELVE_DATA_API_KEY", "8fa2d731f03b4fe190ffd12334a59632")
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, timeout=10, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar si hay error en la respuesta
            if 'code' in data and data['code'] != 200:
                print(f"   ❌ Error en Twelve Data: {data.get('message', 'Unknown error')}")
                return None
            
            values = data.get('values', [])
            meta = data.get('meta', {})
            
            if values:
                # Convertir formato de Twelve Data a formato similar a Polygon
                results = []
                for item in values:
                    try:
                        result_item = {
                            'o': float(item.get('open', 0)),
                            'c': float(item.get('close', 0)),
                            'h': float(item.get('high', 0)),
                            'l': float(item.get('low', 0)),
                            'v': float(item.get('volume', 0)),
                            't': item.get('datetime', ''),  # Twelve Data usa datetime string
                        }
                        results.append(result_item)
                    except (ValueError, TypeError):
                        continue
                
                if results:
                    # Formato compatible con el resto del sistema
                    twelve_data_response = {
                        'ticker': symbol,
                        'queryCount': len(results),
                        'resultsCount': len(results),
                        'adjusted': True,
                        'results': results,
                        'status': 'OK',
                        'source': 'twelve_data',
                        'count': len(results)
                    }
                    
                    print(f"   ✅ Twelve Data: {len(results)} registros obtenidos")
                    return twelve_data_response
            
            print(f"   ❌ Twelve Data: Sin datos para {symbol}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error en Twelve Data para {symbol}: {e}")
        return None

def get_symbol_for_company(company_name: str) -> str:
    """
    Búsqueda directa de símbolo para una empresa específica.
    
    Args:
        company_name: Nombre de la empresa (ej: "Amazon", "Tesla")
        
    Returns:
        str: Símbolo encontrado o None
    """
    company_clean = company_name.strip()
    print(f"Búsqueda para empresa: '{company_clean}'")

    # Búsqueda directa con Twelve Data API
    print(f"Buscando con Twelve Data...")
    symbol = search_symbol_with_twelve_data(company_clean)
    
    if symbol:
        return symbol
    
    print(f"❌ No se encontró símbolo para empresa '{company_clean}'")
    return None

def get_stock_data(company_name: str) -> dict:
    """
    Obtiene datos financieros para una empresa específica.
    
    Args:
        company_name: Nombre de la empresa (ej: "Amazon")
        
    Returns:
        dict: Datos financieros con símbolo, datos del mercado, etc.
    """
    symbol = get_symbol_for_company(company_name)
    
    if not symbol:
        print(f"❌ No se pudo determinar símbolo para empresa: '{company_name}'")
        return {
            "symbol": "UNKNOWN",
            "raw_data": f"No se pudo determinar el símbolo bursátil para '{company_name}'",
            "success": False,
            "error": "Company symbol not found",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"Obteniendo datos financieros para: {symbol}")

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    query = {
        "ticker": symbol,
        "timespan": "day",
        "timespan_multiplier": 1,
        "from_date": start_date,
        "to_date": end_date
    }
    
    # 1. Intentar con Polygon primero
    print(f"📊 Intentando Polygon...")
    try:
        result = polygon_tool.run(query)
        
        has_data = (isinstance(result, dict) and 
                   "results" in result and 
                   len(result["results"]) > 0)

        if has_data:
            status = result.get("status", "OK")
            print(f"✅ Polygon exitoso: Status {status}")
            
            return {
                "symbol": symbol,
                "company_name": company_name,
                "raw_data": result,
                "query_used": query,
                "success": True,
                "status": status,
                "source": "polygon",
                "timestamp": datetime.now().isoformat()
            }

    except Exception as e:
        error_message = str(e)
        print(f"⚠️ Polygon excepción: {error_message}")
        
        # Intentar extraer datos de la excepción (como antes)
        if "API Error:" in error_message:
            try:
                import ast
                start_idx = error_message.find("{")
                if start_idx != -1:
                    dict_str = error_message[start_idx:]
                    result = ast.literal_eval(dict_str)
                    
                    has_data = (isinstance(result, dict) and 
                               "results" in result and 
                               len(result["results"]) > 0)
                    
                    if has_data:
                        status = result.get("status", "DELAYED")
                        print(f"✅ Polygon datos extraídos: Status {status}")
                        
                        return {
                            "symbol": symbol,
                            "company_name": company_name,
                            "raw_data": result,
                            "query_used": query,
                            "success": True,
                            "status": status,
                            "source": "polygon",
                            "timestamp": datetime.now().isoformat()
                        }
            except:
                pass
    
    # 2. Backup con Twelve Data
    print(f"🔄 Polygon falló, intentando Twelve Data backup...")
    twelve_data_result = get_twelve_data_prices(symbol)
    
    if twelve_data_result:
        print(f"✅ Twelve Data backup exitoso")
        return {
            "symbol": symbol,
            "company_name": company_name,
            "raw_data": twelve_data_result,
            "query_used": {"source": "twelve_data", "symbol": symbol},
            "success": True,
            "status": "OK",
            "source": "twelve_data",
            "timestamp": datetime.now().isoformat()
        }
    
    # 3. Ambos fallaron
    print(f"❌ Ambas APIs fallaron para {symbol}")
    return {
        "symbol": symbol,
        "company_name": company_name,
        "raw_data": f"No se pudieron obtener datos para {symbol}",
        "success": False,
        "error": "Both APIs failed",
        "source": "none",
        "timestamp": datetime.now().isoformat()
    }

def format_market_data_for_llm(stock_data: dict) -> str:
    symbol = stock_data.get('symbol', 'UNKNOWN')
    timestamp = stock_data.get("timestamp", "")
    status = stock_data.get("status", "UNKNOWN")
    source = stock_data.get("source", "unknown")

    if not stock_data.get("success", False):
        return f"""
DATOS FINANCIEROS DE {symbol}:

❌ Estado: Datos no disponibles en tiempo real
⚠️ Nota para el contenido: Genera análisis general sobre {symbol} sin mencionar precios específicos.

Sugerencias para el contenido:
- Habla sobre la empresa en general
- Menciona que es una acción del mercado
- Evita datos específicos de precio
- Enfócate en el análisis cualitativo
        """.strip()

    raw_data = stock_data.get("raw_data", {})
    results = raw_data.get("results", [])
    info = ""

    if results:
        latest = results[-1]
        o = latest.get("o")
        c = latest.get("c")
        h = latest.get("h")
        l = latest.get("l")
        v = latest.get("v")

        pct_change = f"{((c - o) / o * 100):.2f}%" if o and c else "N/A"
        volume_formatted = f"{int(v):,}" if v else "N/A"
        
        info = f"""
📈 Precio de apertura: ${o}
📉 Precio de cierre: ${c}
📊 Máximo: ${h} / Mínimo: ${l}
🔁 Cambio porcentual: {pct_change}
📦 Volumen negociado: {volume_formatted}
        """.strip()

    status_emoji = "✅" if status in ["OK", "DELAYED"] else "❌"
    status_text = "Datos obtenidos exitosamente" if status in ["OK", "DELAYED"] else "Datos no disponibles"
    
    # Fuente de datos
    source_text = {
        "polygon": "Polygon.io via LangChain",
        "twelve_data": "Twelve Data API", 
        "unknown": "Fuente desconocida"
    }.get(source, "Fuente desconocida")
    
    status_note = ""
    if status == "DELAYED":
        status_note = "\n⏰ Nota: Los datos pueden tener un retraso de 15-20 minutos"
    elif source == "twelve_data":
        status_note = "\n🌍 Nota: Datos obtenidos de fuente alternativa para cobertura global"

    formatted_text = f"""
DATOS FINANCIEROS DE {symbol}:

{status_emoji} Estado: {status_text}
🕐 Timestamp: {timestamp}
📊 Fuente: {source_text}{status_note}

INFORMACIÓN DEL MERCADO:
{info}

INSTRUCCIONES PARA EL CONTENIDO:
- Usa estos datos para crear contenido financiero relevante y actualizado
- Si hay precios, menciona cambios porcentuales específicos
- Si hay volumen, comenta sobre la actividad del mercado
- Mantén un tono profesional pero accesible
- Adapta el contenido al idioma solicitado
    """.strip()

    return formatted_text