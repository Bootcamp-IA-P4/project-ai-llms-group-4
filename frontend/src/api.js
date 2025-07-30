import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor para manejar errores
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response || error);
    return Promise.reject(error);
  }
);

export const generateContent = async (formData) => {
  try {
    // Si se solicita imagen, forzar modelo 'remote:all' para máxima compatibilidad
    let img_model = formData.img_model;
    if (formData.generateImage) {
      img_model = 'remote:all';
    }
    const requestData = {
      topic: formData.topic,
      platform: formData.platform,
      company: formData.company,
      tone: formData.tone,
      language: formData.language,
      audience: formData.audience,
      img_model: img_model,
      model_writer: formData.model_writer,
      model_research: formData.model_research,
      generate_image: formData.generateImage
    };

    const response = await api.post('/generate', requestData);
    return response.data;
  } catch (error) {
    console.error('Error generando contenido:', error);
    throw error;
  }
};

// Nueva función para búsqueda semántica
export const searchContent = async (query, topK = 3) => {
  try {
    const requestData = {
      query: query,
      top_k: topK
    };

    const response = await api.post('/search', requestData);
    return response.data.results || [];
  } catch (error) {
    console.error('Error en búsqueda:', error);
    throw error;
  }
};

// ✅ NUEVA FUNCIÓN para obtener posts recientes
export const getRecentPosts = async (limit = 10) => {
  try {
    const response = await api.get(`/recent-posts?limit=${limit}`);
    return response.data.results || [];
  } catch (error) {
    console.error('Error obteniendo posts recientes:', error);
    throw error;
  }
};

// Nueva función para subir documentos
export const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/index_document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error subiendo documento:', error);
    throw error;
  }
};

// Nueva función para generar noticias financieras
export const generateFinancialNews = async (topic, company, language) => {
  try {
    const requestData = {
      topic: topic,
      company: company,
      language: language
    };

    const response = await api.post('/financial-news', requestData);
    return response.data;
  } catch (error) {
    console.error('Error generando noticia financiera:', error);
    throw error;
  }
};

// Nueva función para obtener todas las noticias financieras
export const getFinancialNews = async (limit = 10) => {
  try {
    const response = await api.get(`/financial-news?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error obteniendo noticias financieras:', error);
    throw error;
  }
};

export default api;