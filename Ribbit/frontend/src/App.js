// App.js
import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Settings, Sparkles, Trash2, X, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import LanguageSelector from './components/Langselector';
import MicButton from './components/Mic';
import ResponseDisplay from './components/Response';
import { 
  sendAudioToAPI, 
  checkAPIHealth, 
  getRecordingConfig, 
  testMicrophonePermissions,
  getSupportedAudioFormats,
  handleAPIError,
  playAudioBlob,
  playAudioResponse
} from './services/api';

const App = () => {
  const [isListening, setIsListening] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en-IN');
  const [conversations, setConversations] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [apiStatus, setApiStatus] = useState('unknown'); // 'healthy', 'unhealthy', 'unknown'
  const [micPermission, setMicPermission] = useState('unknown'); // 'granted', 'denied', 'unknown'
  const [error, setError] = useState(null);
  const [currentAudioUrl, setCurrentAudioUrl] = useState(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  
  const audioContextRef = useRef(null);
  const streamRef = useRef(null);

  // Initialize the app
  useEffect(() => {
    initializeApp();
  }, []);

  // Clean up audio chunks when recording stops
  useEffect(() => {
    if (!isListening && audioChunks.length > 0) {
      handleAudioProcessing();
    }
  }, [isListening, audioChunks]);

  const initializeApp = async () => {
    try {
      // Check API health
      const isHealthy = await checkAPIHealth();
      setApiStatus(isHealthy ? 'healthy' : 'unhealthy');

      // Check microphone permissions
      const hasMicPermission = await testMicrophonePermissions();
      setMicPermission(hasMicPermission ? 'granted' : 'denied');

      // Initialize audio recording if permissions are granted
      if (hasMicPermission && isHealthy) {
        await initializeAudioRecording();
      }
    } catch (error) {
      console.error('App initialization error:', error);
      setError('Failed to initialize the application');
    }
  };

  const initializeAudioRecording = async () => {
    try {
      const supportedFormats = getSupportedAudioFormats();
      const recordingConfig = getRecordingConfig();
      
      // Use the best supported format
      const mimeType = supportedFormats.find(format => 
        format.includes('opus') || format.includes('webm')
      ) || supportedFormats[0] || 'audio/wav';

      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 16000, // Optimal for Whisper
          channelCount: 1,   // Mono audio
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      });

      streamRef.current = stream;
      
      const recorder = new MediaRecorder(stream, {
        mimeType: mimeType,
        audioBitsPerSecond: recordingConfig.audioBitsPerSecond
      });

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setAudioChunks(prev => [...prev, event.data]);
        }
      };

      recorder.onstop = () => {
        console.log('Recording stopped, processing audio...');
      };

      recorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        setError('Recording error occurred');
        setIsListening(false);
      };

      setMediaRecorder(recorder);
    } catch (error) {
      console.error('Error initializing audio recording:', error);
      setError('Failed to initialize microphone');
      setMicPermission('denied');
    }
  };

  const handleAudioProcessing = async () => {
    if (audioChunks.length === 0) return;

    setIsProcessing(true);
    setError(null);

    try {
      // Create audio blob from chunks
      const audioBlob = new Blob(audioChunks, { 
        type: mediaRecorder?.mimeType || 'audio/wav' 
      });

      // Clear audio chunks
      setAudioChunks([]);

      // Send audio to backend for processing
      const response = await sendAudioToAPI(audioBlob, selectedLanguage);
      
      const newConversation = {
        id: Date.now(),
        userText: response.userText,
        assistantResponse: response.assistantResponse,
        audioUrl: response.audioUrl,
        audioBlob: response.audioBlob,
        timestamp: new Date().toLocaleTimeString([], { 
          hour: '2-digit', 
          minute: '2-digit' 
        }),
        language: selectedLanguage
      };

      setConversations(prev => [newConversation, ...prev]);

      // Auto-play TTS response if available
      if (response.audioUrl || response.audioBlob) {
        await playTTSResponse(response.audioUrl, response.audioBlob);
      }

    } catch (error) {
      console.error('Error processing audio:', error);
      const errorMessage = handleAPIError(error);
      
      const errorConversation = {
        id: Date.now(),
        userText: 'Audio processing failed',
        assistantResponse: errorMessage,
        timestamp: new Date().toLocaleTimeString([], { 
          hour: '2-digit', 
          minute: '2-digit' 
        }),
        isError: true,
        language: selectedLanguage
      };
      
      setConversations(prev => [errorConversation, ...prev]);
      setError(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const playTTSResponse = async (audioUrl, audioBlob) => {
    try {
      setIsPlayingAudio(true);
      
      if (audioBlob) {
        await playAudioBlob(audioBlob);
      } else if (audioUrl) {
        await playAudioResponse(audioUrl);
      }
    } catch (error) {
      console.error('Error playing TTS response:', error);
    } finally {
      setIsPlayingAudio(false);
    }
  };

  const startListening = async () => {
    if (!mediaRecorder) {
      await initializeAudioRecording();
      return;
    }

    if (mediaRecorder.state === 'inactive') {
      setIsListening(true);
      setError(null);
      setAudioChunks([]);
      
      try {
        mediaRecorder.start(100); // Collect data every 100ms
      } catch (error) {
        console.error('Error starting recording:', error);
        setError('Failed to start recording');
        setIsListening(false);
      }
    }
  };

  const stopListening = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      setIsListening(false);
      mediaRecorder.stop();
    }
  };

  const toggleListening = async () => {
    if (apiStatus !== 'healthy') {
      setError('Backend API is not available');
      return;
    }

    if (micPermission !== 'granted') {
      setError('Microphone permission is required');
      return;
    }

    if (isProcessing) {
      return; // Don't allow toggle while processing
    }

    if (isListening) {
      stopListening();
    } else {
      await startListening();
    }
  };

  const clearConversations = () => {
    setConversations([]);
    setShowSettings(false);
    setError(null);
  };

  const retryConnection = async () => {
    setError(null);
    await initializeApp();
  };

  const getLanguageName = (code) => {
    const languages = {
      'hi-IN': 'Hindi',
      'bn-IN': 'Bengali',
      'ta-IN': 'Tamil',
      'te-IN': 'Telugu',
      'gu-IN': 'Gujarati',
      'kn-IN': 'Kannada',
      'ml-IN': 'Malayalam',
      'mr-IN': 'Marathi',
      'pa-IN': 'Punjabi',
      'od-IN': 'Odia',
      'en-IN': 'English'
    };
    return languages[code] || 'English';
  };

  const getStatusColor = () => {
    if (isProcessing) return '#3b82f6';
    if (isListening) return '#22c55e';
    if (error) return '#ef4444';
    return '#ffffff';
  };

  const getStatusText = () => {
    if (isProcessing) return 'Processing...';
    if (isListening) return 'Listening...';
    if (error) return 'Error';
    if (apiStatus === 'unhealthy') return 'API Offline';
    if (micPermission === 'denied') return 'Mic Denied';
    return 'Ready';
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (currentAudioUrl) {
        URL.revokeObjectURL(currentAudioUrl);
      }
    };
  }, [currentAudioUrl]);

  return (
    <div className="app">
      <div className="container glass">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <Sparkles className="logo-icon" />
            <h1>Ribbit</h1>
          </div>
          <div className="header-controls">
            <div className="status-indicator">
              {apiStatus === 'healthy' ? (
                <Wifi className="status-icon healthy" />
              ) : (
                <WifiOff className="status-icon unhealthy" />
              )}
            </div>
            <button 
              className="settings-toggle"
              onClick={() => setShowSettings(!showSettings)}
            >
              <Settings />
            </button>
          </div>
        </header>

        {/* Error Banner */}
        {error && (
          <div className="error-banner">
            <AlertCircle className="error-icon" />
            <span>{error}</span>
            <button className="retry-btn" onClick={retryConnection}>
              Retry
            </button>
          </div>
        )}

        {/* Settings Panel */}
        {showSettings && (
          <div className="settings-panel glass">
            <div className="settings-header">
              <h3>Settings</h3>
              <button 
                className="close-btn"
                onClick={() => setShowSettings(false)}
              >
                <X />
              </button>
            </div>
            <div className="settings-content">
              <div className="setting-item">
                <label>Language</label>
                <LanguageSelector 
                  selectedLanguage={selectedLanguage}
                  onLanguageChange={setSelectedLanguage}
                />
              </div>
              <div className="setting-item">
                <label>System Status</label>
                <div className="status-grid">
                  <div className="status-item">
                    <span>API:</span>
                    <span className={`status-badge ${apiStatus}`}>
                      {apiStatus === 'healthy' ? 'Online' : 'Offline'}
                    </span>
                  </div>
                  <div className="status-item">
                    <span>Microphone:</span>
                    <span className={`status-badge ${micPermission}`}>
                      {micPermission === 'granted' ? 'Granted' : 'Denied'}
                    </span>
                  </div>
                </div>
              </div>
              <button className="clear-btn" onClick={clearConversations}>
                <Trash2 />
                Clear Conversations
              </button>
            </div>
          </div>
        )}

        {/* Main Content */}
        <main className="main">
          {/* Voice Control */}
          <div className="voice-section">
            <div className="status-display">
              <div className={`status ${isProcessing ? 'processing' : isListening ? 'listening' : error ? 'error' : 'idle'}`}>
                {isProcessing ? (
                  <>
                    <div className="spinner"></div>
                    <span>Processing...</span>
                  </>
                ) : isListening ? (
                  <>
                    <div className="pulse-indicator"></div>
                    <span>Listening...</span>
                  </>
                ) : error ? (
                  <>
                    <AlertCircle className="status-icon" />
                    <span>Error</span>
                  </>
                ) : (
                  <>
                    <Mic className="status-icon" />
                    <span>Ready</span>
                  </>
                )}
              </div>
            </div>

            <MicButton 
              isListening={isListening}
              isProcessing={isProcessing}
              isDisabled={apiStatus !== 'healthy' || micPermission !== 'granted'}
              onToggle={toggleListening}
            />

            <div className="controls-info">
              <div className="language-info">
                <span>{getLanguageName(selectedLanguage)}</span>
              </div>
              {isPlayingAudio && (
                <div className="audio-playing">
                  <span>Playing response...</span>
                </div>
              )}
            </div>
          </div>

          {/* Conversations */}
          <div className="conversations-section">
            <ResponseDisplay 
              conversations={conversations}
              onPlayAudio={playTTSResponse}
              isPlayingAudio={isPlayingAudio}
            />
          </div>
        </main>
      </div>

      <style jsx>{`
        .app {
          min-height: 100vh;
          padding: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .container {
          width: 100%;
          max-width: 900px;
          min-height: 600px;
          display: flex;
          flex-direction: column;
          position: relative;
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          border-radius: 24px;
          border: 1px solid rgba(255, 255, 255, 0.2);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 24px 32px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo-icon {
          width: 28px;
          height: 28px;
          color: #ff6b6b;
        }

        .logo h1 {
          font-size: 24px;
          font-weight: 600;
          color: #ffffff;
          margin: 0;
        }

        .header-controls {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .status-indicator {
          display: flex;
          align-items: center;
        }

        .status-icon {
          width: 20px;
          height: 20px;
        }

        .status-icon.healthy {
          color: #22c55e;
        }

        .status-icon.unhealthy {
          color: #ef4444;
        }

        .settings-toggle {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          padding: 10px;
          color: #ffffff;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .settings-toggle:hover {
          background: rgba(255, 255, 255, 0.1);
          transform: translateY(-1px);
        }

        .error-banner {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 24px;
          background: rgba(239, 68, 68, 0.1);
          border: 1px solid rgba(239, 68, 68, 0.2);
          border-radius: 12px;
          margin: 16px 24px;
          color: #ef4444;
        }

        .error-icon {
          width: 18px;
          height: 18px;
        }

        .retry-btn {
          background: rgba(239, 68, 68, 0.2);
          border: 1px solid rgba(239, 68, 68, 0.3);
          border-radius: 6px;
          padding: 4px 8px;
          color: #ef4444;
          cursor: pointer;
          font-size: 12px;
          margin-left: auto;
        }

        .retry-btn:hover {
          background: rgba(239, 68, 68, 0.3);
        }

        .settings-panel {
          position: absolute;
          top: 80px;
          right: 20px;
          width: 320px;
          z-index: 1000;
          animation: slideIn 0.3s ease;
        }

        .settings-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 24px 16px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .settings-header h3 {
          color: #ffffff;
          margin: 0;
          font-size: 18px;
          font-weight: 600;
        }

        .close-btn {
          background: none;
          border: none;
          color: rgba(255, 255, 255, 0.7);
          cursor: pointer;
          padding: 4px;
          border-radius: 6px;
          transition: all 0.2s ease;
        }

        .close-btn:hover {
          color: #ffffff;
          background: rgba(255, 255, 255, 0.1);
        }

        .settings-content {
          padding: 20px 24px;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .setting-item {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .setting-item label {
          color: rgba(255, 255, 255, 0.8);
          font-size: 14px;
          font-weight: 500;
        }

        .status-grid {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .status-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 12px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 8px;
          font-size: 14px;
        }

        .status-badge {
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 500;
        }

        .status-badge.healthy, .status-badge.granted {
          background: rgba(34, 197, 94, 0.2);
          color: #22c55e;
        }

        .status-badge.unhealthy, .status-badge.denied {
          background: rgba(239, 68, 68, 0.2);
          color: #ef4444;
        }

        .clear-btn {
          background: rgba(255, 59, 59, 0.1);
          border: 1px solid rgba(255, 59, 59, 0.2);
          border-radius: 12px;
          padding: 12px 16px;
          color: #ff6b6b;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 500;
        }

        .clear-btn:hover {
          background: rgba(255, 59, 59, 0.2);
          transform: translateY(-1px);
        }

        .main {
          flex: 1;
          padding: 40px 32px;
          display: flex;
          flex-direction: column;
          gap: 40px;
        }

        .voice-section {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 24px;
        }

        .status-display {
          height: 50px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .status {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 16px;
          border-radius: 20px;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: rgba(255, 255, 255, 0.8);
          font-size: 14px;
          font-weight: 500;
          transition: all 0.3s ease;
        }

        .status.listening {
          background: rgba(34, 197, 94, 0.1);
          border-color: rgba(34, 197, 94, 0.3);
          color: #22c55e;
        }

        .status.processing {
          background: rgba(59, 130, 246, 0.1);
          border-color: rgba(59, 130, 246, 0.3);
          color: #3b82f6;
        }

        .status.error {
          background: rgba(239, 68, 68, 0.1);
          border-color: rgba(239, 68, 68, 0.3);
          color: #ef4444;
        }

        .status-icon {
          width: 16px;
          height: 16px;
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid rgba(59, 130, 246, 0.3);
          border-top: 2px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        .pulse-indicator {
          width: 16px;
          height: 16px;
          background: #22c55e;
          border-radius: 50%;
          animation: pulse 1.5s ease-in-out infinite;
        }

        .controls-info {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
        }

        .language-info {
          color: rgba(255, 255, 255, 0.6);
          font-size: 14px;
          font-weight: 500;
          padding: 6px 12px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 16px;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .audio-playing {
          color: #3b82f6;
          font-size: 12px;
          font-weight: 500;
          padding: 4px 8px;
          background: rgba(59, 130, 246, 0.1);
          border-radius: 12px;
          border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .conversations-section {
          flex: 1;
          min-height: 200px;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        @keyframes pulse {
          0%, 100% { 
            transform: scale(1);
            opacity: 1;
          }
          50% { 
            transform: scale(1.2);
            opacity: 0.7;
          }
        }

        @media (max-width: 768px) {
          .app {
            padding: 10px;
          }

          .header {
            padding: 20px 24px;
          }

          .main {
            padding: 30px 24px;
            gap: 30px;
          }

          .settings-panel {
            width: 280px;
            right: 10px;
          }

          .error-banner {
            margin: 12px 20px;
            padding: 10px 16px;
          }
        }

        @media (max-width: 480px) {
          .header {
            padding: 16px 20px;
          }

          .logo h1 {
            font-size: 20px;
          }

          .main {
            padding: 24px 20px;
            gap: 24px;
          }

          .settings-panel {
            width: 260px;
            right: 5px;
          }

          .error-banner {
            margin: 8px 16px;
            padding: 8px 12px;
            font-size: 14px;
          }
        }
      `}</style>
    </div>
  );
};

export default App;
