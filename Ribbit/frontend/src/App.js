import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Settings, Sparkles, Trash2, X } from 'lucide-react';
import LanguageSelector from './components/Langselector';
import MicButton from './components/Mic';
import ResponseDisplay from './components/Response';
import { sendAudioToAPI } from './services/api';

const App = () => {
  const [isListening, setIsListening] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en-IN');
  const [conversations, setConversations] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  useEffect(() => {
    // Initialize microphone
    const initializeMicrophone = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        setMediaRecorder(recorder);

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            setAudioChunks(prev => [...prev, event.data]);
          }
        };

        recorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          setAudioChunks([]);
          await handleAudioSubmit(audioBlob);
        };
      } catch (error) {
        console.error('Error accessing microphone:', error);
      }
    };

    initializeMicrophone();
  }, [audioChunks]);

  const handleAudioSubmit = async (audioBlob) => {
    setIsProcessing(true);
    try {
      const response = await sendAudioToAPI(audioBlob, selectedLanguage);
      
      const newConversation = {
        id: Date.now(),
        userText: response.userText,
        assistantResponse: response.assistantResponse,
        audioUrl: response.audioUrl,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setConversations(prev => [newConversation, ...prev]);
    } catch (error) {
      console.error('Error processing audio:', error);
      const errorConversation = {
        id: Date.now(),
        userText: 'Error processing audio',
        assistantResponse: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true
      };
      setConversations(prev => [errorConversation, ...prev]);
    } finally {
      setIsProcessing(false);
    }
  };

  const startListening = () => {
    if (mediaRecorder && mediaRecorder.state === 'inactive') {
      setIsListening(true);
      mediaRecorder.start();
    }
  };

  const stopListening = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      setIsListening(false);
      mediaRecorder.stop();
    }
  };

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const clearConversations = () => {
    setConversations([]);
    setShowSettings(false);
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

  return (
    <div className="app">
      <div className="container glass">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <Sparkles className="logo-icon" />
            <h1>Ribbit</h1>
          </div>
          <button 
            className="settings-toggle"
            onClick={() => setShowSettings(!showSettings)}
          >
            <Settings />
          </button>
        </header>

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
              <LanguageSelector 
                selectedLanguage={selectedLanguage}
                onLanguageChange={setSelectedLanguage}
              />
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
              {isProcessing ? (
                <div className="status processing">
                  <div className="spinner"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                <div className={`status ${isListening ? 'listening' : 'idle'}`}>
                  {isListening ? (
                    <>
                      <MicOff className="status-icon" />
                      <span>Listening...</span>
                    </>
                  ) : (
                    <>
                      <Mic className="status-icon" />
                      <span>Ready</span>
                    </>
                  )}
                </div>
              )}
            </div>

            <MicButton 
              isListening={isListening}
              isProcessing={isProcessing}
              onToggle={toggleListening}
            />

            <div className="language-info">
              <span>{getLanguageName(selectedLanguage)}</span>
            </div>
          </div>

          {/* Conversations */}
          <div className="conversations-section">
            <ResponseDisplay conversations={conversations} />
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
        }

        .container {
          width: 100%;
          max-width: 900px;
          min-height: 600px;
          display: flex;
          flex-direction: column;
          position: relative;
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

        .language-info {
          color: rgba(255, 255, 255, 0.6);
          font-size: 14px;
          font-weight: 500;
          padding: 6px 12px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 16px;
          border: 1px solid rgba(255, 255, 255, 0.1);
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
        }
      `}</style>
    </div>
  );
};

export default App;
