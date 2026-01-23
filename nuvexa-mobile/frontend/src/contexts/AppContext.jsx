/**
 * Application context for global state management
 */
import { createContext, useContext, useState, useEffect } from 'react';
import { getModes } from '../services/api';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [mode, setMode] = useState('assistant');
  const [modes, setModes] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load available modes on mount
  useEffect(() => {
    loadModes();
  }, []);

  async function loadModes() {
    try {
      const data = await getModes();
      setModes(data.modes || []);
    } catch (err) {
      console.error('Failed to load modes:', err);
      // Fallback modes if API fails
      setModes([
        {
          id: 'assistant',
          name: 'Assistant',
          icon: '🤖',
          description: 'General AI assistant'
        },
        {
          id: 'shopping',
          name: 'Shopping',
          icon: '🛒',
          description: 'Find products'
        }
      ]);
    }
  }

  function addMessage(role, content, products = null) {
    const newMessage = {
      id: Date.now(),
      role,
      content,
      products,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, newMessage]);
  }

  function clearMessages() {
    setMessages([]);
  }

  function changeMode(newMode) {
    setMode(newMode);
    // Optionally clear messages when switching modes
    // clearMessages();
  }

  const value = {
    mode,
    modes,
    messages,
    isLoading,
    error,
    setIsLoading,
    setError,
    addMessage,
    clearMessages,
    changeMode,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
