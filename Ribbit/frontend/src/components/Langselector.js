import React, { useState } from 'react';
import { ChevronDown, Globe, Check } from 'lucide-react';

const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  const languages = [
    { code: 'hi-IN', name: 'Hindi', nativeName: 'हिंदी' },
    { code: 'bn-IN', name: 'Bengali', nativeName: 'বাংলা' },
    { code: 'ta-IN', name: 'Tamil', nativeName: 'தமிழ்' },
    { code: 'te-IN', name: 'Telugu', nativeName: 'తెలుగు' },
    { code: 'gu-IN', name: 'Gujarati', nativeName: 'ગુજરાતી' },
    { code: 'kn-IN', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
    { code: 'ml-IN', name: 'Malayalam', nativeName: 'മലയാളം' },
    { code: 'mr-IN', name: 'Marathi', nativeName: 'मराठी' },
    { code: 'pa-IN', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' },
    { code: 'od-IN', name: 'Odia', nativeName: 'ଓଡ଼ିଆ' },
    { code: 'en-IN', name: 'English', nativeName: 'English' }
  ];

  const selectedLang = languages.find(lang => lang.code === selectedLanguage) || languages[10];

  const handleLanguageSelect = (languageCode) => {
    onLanguageChange(languageCode);
    setIsOpen(false);
  };

  return (
    <div className="language-selector">
      <div className="language-label">
        <Globe size={16} />
        <span>Language</span>
      </div>
      
      <div className="language-dropdown">
        <button
          className={`language-button ${isOpen ? 'open' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className="language-info">
            <span className="language-name">{selectedLang.name}</span>
            <span className="language-native">{selectedLang.nativeName}</span>
          </div>
          <ChevronDown 
            size={18} 
            className={`chevron ${isOpen ? 'rotated' : ''}`} 
          />
        </button>

        {isOpen && (
          <div className="language-menu">
            {languages.map((language) => (
              <button
                key={language.code}
                className={`language-option ${selectedLanguage === language.code ? 'selected' : ''}`}
                onClick={() => handleLanguageSelect(language.code)}
              >
                <div className="language-info">
                  <span className="language-name">{language.name}</span>
                  <span className="language-native">{language.nativeName}</span>
                </div>
                {selectedLanguage === language.code && (
                  <Check size={16} className="check-icon" />
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      <style jsx>{`
        .language-selector {
          width: 100%;
          margin-bottom: 24px;
        }

        .language-label {
          display: flex;
          align-items: center;
          gap: 8px;
          color: rgba(255, 255, 255, 0.9);
          font-weight: 500;
          font-size: 14px;
          margin-bottom: 8px;
          letter-spacing: 0.5px;
        }

        .language-dropdown {
          position: relative;
        }

        .language-button {
          width: 100%;
          padding: 16px 20px;
          background: rgba(255, 255, 255, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 16px;
          color: white;
          cursor: pointer;
          transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-family: inherit;
          outline: none;
        }

        .language-button:hover {
          background: rgba(255, 255, 255, 0.12);
          border-color: rgba(255, 255, 255, 0.2);
          transform: translateY(-1px);
        }

        .language-button:focus {
          border-color: rgba(99, 102, 241, 0.5);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .language-button.open {
          background: rgba(255, 255, 255, 0.12);
          border-color: rgba(255, 255, 255, 0.2);
        }

        .language-info {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          gap: 4px;
        }

        .language-name {
          font-weight: 500;
          font-size: 14px;
          color: white;
        }

        .language-native {
          font-size: 12px;
          color: rgba(255, 255, 255, 0.6);
          font-weight: 400;
        }

        .chevron {
          transition: transform 0.2s ease;
          color: rgba(255, 255, 255, 0.7);
        }

        .chevron.rotated {
          transform: rotate(180deg);
        }

        .language-menu {
          position: absolute;
          top: calc(100% + 8px);
          left: 0;
          right: 0;
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(20px);
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 16px;
          z-index: 100;
          max-height: 280px;
          overflow-y: auto;
          animation: slideDown 0.2s ease;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        .language-option {
          width: 100%;
          padding: 14px 20px;
          background: transparent;
          border: none;
          color: white;
          cursor: pointer;
          transition: all 0.15s ease;
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-family: inherit;
          outline: none;
        }

        .language-option:hover {
          background: rgba(255, 255, 255, 0.08);
        }

        .language-option:focus {
          background: rgba(255, 255, 255, 0.1);
        }

        .language-option.selected {
          background: rgba(99, 102, 241, 0.15);
          border-color: rgba(99, 102, 241, 0.3);
        }

        .check-icon {
          color: #6366f1;
          flex-shrink: 0;
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-8px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .language-menu::-webkit-scrollbar {
          width: 6px;
        }

        .language-menu::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }

        .language-menu::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.3);
          border-radius: 10px;
        }

        .language-menu::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.5);
        }

        @media (max-width: 480px) {
          .language-button {
            padding: 14px 16px;
          }
          
          .language-option {
            padding: 12px 16px;
          }
        }
      `}</style>
    </div>
  );
};

export default LanguageSelector;
