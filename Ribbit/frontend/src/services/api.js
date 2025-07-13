// services/api.js
const API_BASE_URL = 'http://localhost:8000'; // FastAPI typically runs on 8000

export const sendAudioToAPI = async (audioBlob, language) => {
  try {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');
    formData.append('language', language);

    const response = await fetch(`${API_BASE_URL}/process-voice`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }

    return {
      userText: data.transcription || 'Could not transcribe audio',
      assistantResponse: data.llm_response || 'Sorry, I could not generate a response',
      audioUrl: data.tts_audio_url ? `${API_BASE_URL}${data.tts_audio_url}` : null,
      audioBlob: data.tts_audio_base64 ? base64ToBlob(data.tts_audio_base64, 'audio/wav') : null
    };
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to process audio. Please check your connection and try again.');
  }
};

export const getAvailableLanguages = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/languages`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.languages || getDefaultLanguages();
  } catch (error) {
    console.error('Failed to fetch languages:', error);
    return getDefaultLanguages();
  }
};

const getDefaultLanguages = () => [
  { code: 'hi-IN', name: 'Hindi' },
  { code: 'bn-IN', name: 'Bengali' },
  { code: 'ta-IN', name: 'Tamil' },
  { code: 'te-IN', name: 'Telugu' },
  { code: 'gu-IN', name: 'Gujarati' },
  { code: 'kn-IN', name: 'Kannada' },
  { code: 'ml-IN', name: 'Malayalam' },
  { code: 'mr-IN', name: 'Marathi' },
  { code: 'pa-IN', name: 'Punjabi' },
  { code: 'od-IN', name: 'Odia' },
  { code: 'en-IN', name: 'English'}
];

export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000)
    });
    
    if (!response.ok) {
      return false;
    }

    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    console.error('API Health Check Failed:', error);
    return false;
  }
};

export const sendTextToAPI = async (text, language) => {
  try {
    const response = await fetch(`${API_BASE_URL}/process-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        language: language
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }

    return {
      userText: text,
      assistantResponse: data.llm_response || 'Sorry, I could not generate a response',
      audioUrl: data.tts_audio_url ? `${API_BASE_URL}${data.tts_audio_url}` : null,
      audioBlob: data.tts_audio_base64 ? base64ToBlob(data.tts_audio_base64, 'audio/wav') : null
    };
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to process text. Please check your connection and try again.');
  }
};

export const downloadAudio = async (audioUrl) => {
  try {
    const response = await fetch(audioUrl);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.blob();
  } catch (error) {
    console.error('Audio Download Error:', error);
    throw new Error('Failed to download audio response');
  }
};

export const playAudioResponse = async (audioUrl) => {
  return new Promise((resolve, reject) => {
    try {
      const audio = new Audio(audioUrl);
      audio.volume = 0.8;
      audio.onended = resolve;
      audio.onerror = (error) => {
        console.error('Audio playback error:', error);
        reject(new Error('Failed to play audio response'));
      };
      audio.play().catch(reject);
    } catch (error) {
      console.error('Audio Playback Error:', error);
      reject(new Error('Failed to play audio response'));
    }
  });
};

export const playAudioBlob = async (audioBlob) => {
  return new Promise((resolve, reject) => {
    try {
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.volume = 0.8;
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
        resolve();
      };
      audio.onerror = (error) => {
        URL.revokeObjectURL(audioUrl);
        console.error('Audio playback error:', error);
        reject(new Error('Failed to play audio response'));
      };
      audio.play().catch(reject);
    } catch (error) {
      console.error('Audio Playback Error:', error);
      reject(new Error('Failed to play audio response'));
    }
  });
};

// Helper function to convert base64 to blob
const base64ToBlob = (base64, mimeType) => {
  const byteCharacters = atob(base64);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
};

// Function to get recording config optimized for Whisper
export const getRecordingConfig = () => ({
  mimeType: 'audio/webm;codecs=opus', // Fallback to audio/wav if not supported
  audioBitsPerSecond: 16000, // 16kHz sample rate works well with Whisper
});

// Function to test microphone permissions
export const testMicrophonePermissions = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach(track => track.stop());
    return true;
  } catch (error) {
    console.error('Microphone permission denied:', error);
    return false;
  }
};

// Function to get supported audio formats
export const getSupportedAudioFormats = () => {
  const formats = [
    'audio/webm;codecs=opus',
    'audio/mp4',
    'audio/wav',
    'audio/ogg;codecs=opus'
  ];
  
  return formats.filter(format => MediaRecorder.isTypeSupported(format));
};

// Function to handle API errors gracefully
export const handleAPIError = (error) => {
  if (error.name === 'AbortError') {
    return 'Request was cancelled';
  }
  if (error.message.includes('fetch')) {
    return 'Network error. Please check your connection';
  }
  if (error.message.includes('JSON')) {
    return 'Server response error. Please try again';
  }
  return error.message || 'An unexpected error occurred';
};
