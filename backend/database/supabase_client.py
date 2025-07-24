import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

class SupabaseClient:
    """
    Cliente singleton para Supabase.
    Maneja la conexión y configuración de la base de datos.
    """
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._initialize_client()
    
    def _initialize_client(self):
        """
        Inicializa el cliente de Supabase con las credenciales del .env
        """
        try:
            # Obtener credenciales del .env
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar definidas en el archivo .env")
            
            # Crear cliente
            self._client = create_client(supabase_url, supabase_key)
            
            print("✅ Cliente Supabase inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando cliente Supabase: {e}")
            self._client = None
    
    @property
    def client(self) -> Client:
        """
        Devuelve el cliente de Supabase.
        
        Returns:
            Client: Cliente de Supabase o None si no se pudo inicializar
        """
        if self._client is None:
            print("⚠️ Cliente Supabase no disponible")
        return self._client
    
    def is_connected(self) -> bool:
        """
        Verifica si el cliente está conectado y funcionando.
        
        Returns:
            bool: True si está conectado, False si no
        """
        if self._client is None:
            return False
        
        try:
            # Test básico de conexión
            result = self._client.table('financial_news').select("id").limit(1).execute()
            return True
        except Exception as e:
            print(f"⚠️ Error de conexión Supabase: {e}")
            return False
    
    def test_connection(self):
        """
        Prueba la conexión a Supabase y muestra información de diagnóstico.
        """
        print("🔍 Probando conexión a Supabase...")
        
        if self._client is None:
            print("❌ Cliente no inicializado")
            return False
        
        try:
            # Intentar consulta simple
            result = self._client.table('financial_news').select("count").execute()
            print("✅ Conexión exitosa a Supabase")
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("💡 Verifica que:")
            print("   - SUPABASE_URL esté correcta en .env")
            print("   - SUPABASE_KEY esté correcta en .env")
            print("   - La tabla 'financial_news' exista en Supabase")
            return False

# Instancia global del cliente
supabase_client = SupabaseClient()

def get_supabase_client() -> Client:
    """
    Función helper para obtener el cliente de Supabase.
    
    Returns:
        Client: Cliente de Supabase
    """
    return supabase_client.client