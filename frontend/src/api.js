import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

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
    const response = await api.post('/generate-content', {
      topic: formData.topic,
      platform: formData.platform,
      company: formData.company,
      tone: formData.tone,
      language: formData.language,
      audience: formData.audience,
      model: formData.model,
      generateImage: formData.generateImage,
      imageMode: formData.imageMode,
      imageSize: formData.imageSize,
      imageStyle: formData.imageStyle,
      imagePrompt: formData.imagePrompt
    });
    return response.data;
  } catch (error) {
    console.error('Error generando contenido:', error);
    throw error;
  }
};

export default api;
