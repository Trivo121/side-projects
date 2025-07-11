import React from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';

const MicButton = ({ isListening, isProcessing, onToggle }) => {
  const getButtonState = () => {
    if (isProcessing) return 'processing';
    if (isListening) return 'listening';
    return 'idle';
  };

  const getIconAndText = () => {
    if (isProcessing) {
      return {
        icon: <Loader2 size={28} className="animate-spin" />,
        text: 'Processing...'
      };
    }
    
    if (isListening) {
      return {
        icon: <Square size={28} />,
        text: 'Stop'
      };
    }
    
    return {
      icon: <Mic size={28} />,
      text: 'Speak'
    };
  };

  const { icon, text } = getIconAndText();
  const buttonState = getButtonState();

  return (
    <div className="mic-container">
      <button
        className={`mic-button ${buttonState}`}
        onClick={onToggle}
        disabled={isProcessing}
      >
        <div className="mic-content">
          {icon}
          <span className="mic-text">{text}</span>
        </div>
        
        {isListening && (
          <div className="listening-rings">
            <div className="ring ring-1"></div>
            <div className="ring ring-2"></div>
            <div className="ring ring-3"></div>
          </div>
        )}
      </button>

      <style jsx>{`
        .mic-container {
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .mic-button {
          position: relative;
          width: 160px;
          height: 160px;
          border-radius: 50%;
          border: 2px solid rgba(255, 255, 255, 0.2);
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-family: inherit;
          outline: none;
          overflow: hidden;
        }

        .mic-button:hover {
          background: rgba(255, 255, 255, 0.15);
          border-color: rgba(255, 255, 255, 0.3);
          transform: translateY(-2px);
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }

        .mic-button:active {
          transform: translateY(0);
        }

        .mic-button:focus {
          border-color: rgba(99, 102, 241, 0.5);
          box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }

        .mic-button.listening {
          background: rgba(34, 197, 94, 0.15);
          border-color: rgba(34, 197, 94, 0.4);
          animation: listeningPulse 2s infinite;
        }

        .mic-button.listening:hover {
          background: rgba(34, 197, 94, 0.2);
        }

        .mic-button.processing {
          background: rgba(59, 130, 246, 0.15);
          border-color: rgba(59, 130, 246, 0.4);
          cursor: not-allowed;
        }

        .mic-button:disabled {
          opacity: 0.7;
          cursor: not-allowed;
          transform: none;
        }

        .mic-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          z-index: 2;
        }

        .mic-text {
          font-size: 14px;
          font-weight: 500;
          letter-spacing: 0.5px;
        }

        .animate-spin {
          animation: spin 1s linear infinite;
        }

        .listening-rings {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          pointer-events: none;
        }

        .ring {
          position: absolute;
          top: 50%;
          left: 50%;
          width: 160px;
          height: 160px;
          border: 2px solid rgba(34, 197, 94, 0.3);
          border-radius: 50%;
          transform: translate(-50%, -50%);
          animation: ripple 2s infinite;
        }

        .ring-1 {
          animation-delay: 0s;
        }

        .ring-2 {
          animation-delay: 0.5s;
        }

        .ring-3 {
          animation-delay: 1s;
        }

        @keyframes listeningPulse {
          0%, 100% {
            box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.3);
          }
          50% {
            box-shadow: 0 0 0 15px rgba(34, 197, 94, 0);
          }
        }

        @keyframes ripple {
          0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.8;
          }
          100% {
            transform: translate(-50%, -50%) scale(1.8);
            opacity: 0;
          }
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
          .mic-button {
            width: 140px;
            height: 140px;
          }

          .mic-content {
            gap: 6px;
          }

          .mic-text {
            font-size: 13px;
          }

          .ring {
            width: 140px;
            height: 140px;
          }
        }

        @media (max-width: 480px) {
          .mic-button {
            width: 120px;
            height: 120px;
          }

          .mic-text {
            font-size: 12px;
          }

          .ring {
            width: 120px;
            height: 120px;
          }
        }
      `}</style>
    </div>
  );
};

export default MicButton;
