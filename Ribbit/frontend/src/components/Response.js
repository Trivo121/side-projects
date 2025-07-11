import React, { useState, useEffect } from 'react';
import { User, Bot, Play, Pause, AlertCircle, MessageSquare } from 'lucide-react';
import { playAudioResponse } from '../services/api';

const ResponseDisplay = ({ conversations }) => {
  const [playingAudio, setPlayingAudio] = useState(null);
  const [audioStates, setAudioStates] = useState({});

  useEffect(() => {
    setAudioStates({});
    setPlayingAudio(null);
  }, [conversations]);

  const handlePlayAudio = async (conversationId, audioUrl) => {
    if (playingAudio === conversationId) {
      setPlayingAudio(null);
      setAudioStates(prev => ({
        ...prev,
        [conversationId]: 'idle'
      }));
      return;
    }

    if (!audioUrl) {
      setAudioStates(prev => ({
        ...prev,
        [conversationId]: 'error'
      }));
      return;
    }

    try {
      setPlayingAudio(conversationId);
      setAudioStates(prev => ({
        ...prev,
        [conversationId]: 'playing'
      }));

      await playAudioResponse(audioUrl);
      
      setPlayingAudio(null);
      setAudioStates(prev => ({
        ...prev,
        [conversationId]: 'idle'
      }));
    } catch (error) {
      console.error('Error playing audio:', error);
      setPlayingAudio(null);
      setAudioStates(prev => ({
        ...prev,
        [conversationId]: 'error'
      }));
    }
  };

  const getAudioIcon = (conversationId, audioUrl) => {
    const state = audioStates[conversationId] || 'idle';
    
    if (state === 'playing') {
      return <Pause size={16} />;
    }
    
    if (state === 'error' || !audioUrl) {
      return <AlertCircle size={16} className="text-red-400" />;
    }
    
    return <Play size={16} />;
  };

  if (conversations.length === 0) {
    return (
      <div className="response-display">
        <div className="empty-state">
          <MessageSquare size={48} className="empty-icon" />
          <h3 className="empty-title">Start a conversation</h3>
          <p className="empty-subtitle">Press the microphone to begin speaking</p>
        </div>

        <style jsx>{`
          .response-display {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 300px;
          }

          .empty-state {
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            padding: 40px 20px;
          }

          .empty-icon {
            color: rgba(255, 255, 255, 0.4);
            margin-bottom: 16px;
          }

          .empty-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
            color: rgba(255, 255, 255, 0.9);
          }

          .empty-subtitle {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.6);
            font-weight: 400;
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="response-display">
      <div className="conversations-container">
        {conversations.map((conversation) => (
          <div 
            key={conversation.id} 
            className={`conversation ${conversation.isError ? 'error' : ''}`}
          >
            <div className="conversation-header">
              <span className="timestamp">{conversation.timestamp}</span>
            </div>

            <div className="messages">
              {/* User Message */}
              <div className="message user">
                <div className="avatar user-avatar">
                  <User size={16} />
                </div>
                <div className="content">
                  <p className="message-text">{conversation.userText}</p>
                </div>
              </div>

              {/* Assistant Message */}
              <div className="message assistant">
                <div className="avatar assistant-avatar">
                  <Bot size={16} />
                </div>
                <div className="content">
                  <p className="message-text">{conversation.assistantResponse}</p>
                  {conversation.audioUrl && (
                    <button
                      className={`audio-btn ${audioStates[conversation.id] || 'idle'}`}
                      onClick={() => handlePlayAudio(conversation.id, conversation.audioUrl)}
                      disabled={audioStates[conversation.id] === 'playing'}
                    >
                      {getAudioIcon(conversation.id, conversation.audioUrl)}
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <style jsx>{`
        .response-display {
          height: 100%;
          display: flex;
          flex-direction: column;
        }

        .conversations-container {
          flex: 1;
          overflow-y: auto;
          padding: 16px 0;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .conversation {
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 20px;
          padding: 20px;
          transition: all 0.2s ease;
          animation: fadeIn 0.3s ease;
        }

        .conversation:hover {
          background: rgba(255, 255, 255, 0.08);
          border-color: rgba(255, 255, 255, 0.15);
        }

        .conversation.error {
          background: rgba(239, 68, 68, 0.08);
          border-color: rgba(239, 68, 68, 0.2);
        }

        .conversation-header {
          display: flex;
          justify-content: flex-end;
          margin-bottom: 16px;
          padding-bottom: 8px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .timestamp {
          color: rgba(255, 255, 255, 0.5);
          font-size: 12px;
          font-weight: 500;
        }

        .messages {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .message {
          display: flex;
          gap: 12px;
          align-items: flex-start;
        }

        .avatar {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .user-avatar {
          background: rgba(59, 130, 246, 0.15);
          border: 1px solid rgba(59, 130, 246, 0.3);
          color: #60a5fa;
        }

        .assistant-avatar {
          background: rgba(34, 197, 94, 0.15);
          border: 1px solid rgba(34, 197, 94, 0.3);
          color: #4ade80;
        }

        .content {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .message-text {
          background: rgba(255, 255, 255, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 16px;
          padding: 12px 16px;
          color: rgba(255, 255, 255, 0.9);
          font-size: 14px;
          line-height: 1.5;
          margin: 0;
          word-wrap: break-word;
        }

        .user .message-text {
          background: rgba(59, 130, 246, 0.1);
          border-color: rgba(59, 130, 246, 0.2);
        }

        .assistant .message-text {
          background: rgba(34, 197, 94, 0.1);
          border-color: rgba(34, 197, 94, 0.2);
        }

        .audio-btn {
          width: 28px;
          height: 28px;
          border-radius: 50%;
          border: 1px solid rgba(255, 255, 255, 0.2);
          background: rgba(255, 255, 255, 0.1);
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          color: rgba(255, 255, 255, 0.8);
          align-self: flex-start;
        }

        .audio-btn:hover {
          background: rgba(255, 255, 255, 0.15);
          border-color: rgba(255, 255, 255, 0.3);
          transform: scale(1.05);
        }

        .audio-btn.playing {
          background: rgba(34, 197, 94, 0.2);
          border-color: rgba(34, 197, 94, 0.4);
          color: #4ade80;
        }

        .audio-btn.error {
          background: rgba(239, 68, 68, 0.1);
          border-color: rgba(239, 68, 68, 0.3);
          cursor: not-allowed;
        }

        .audio-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .conversations-container::-webkit-scrollbar {
          width: 6px;
        }

        .conversations-container::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }

        .conversations-container::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.2);
          border-radius: 10px;
        }

        .conversations-container::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        @media (max-width: 768px) {
          .conversation {
            padding: 16px;
          }

          .avatar {
            width: 28px;
            height: 28px;
          }

          .message-text {
            font-size: 13px;
            padding: 10px 14px;
          }

          .audio-btn {
            width: 26px;
            height: 26px;
          }
        }

        @media (max-width: 480px) {
          .conversations-container {
            padding: 12px 0;
          }

          .conversation {
            padding: 12px;
          }

          .messages {
            gap: 12px;
          }

          .message {
            gap: 10px;
          }

          .avatar {
            width: 26px;
            height: 26px;
          }

          .message-text {
            font-size: 12px;
            padding: 8px 12px;
          }

          .audio-btn {
            width: 24px;
            height: 24px;
          }
        }
      `}</style>
    </div>
  );
};

export default ResponseDisplay;
