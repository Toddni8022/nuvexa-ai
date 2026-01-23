/**
 * Chat interface with messages and input
 */
import { useState, useRef, useEffect } from 'react';
import { useApp } from '../contexts/AppContext';
import { sendMessage } from '../services/api';
import Message from './Message';
import WelcomeScreen from './WelcomeScreen';

export default function ChatInterface() {
  const { mode, messages, isLoading, setIsLoading, setError, addMessage } = useApp();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [input]);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setError(null);

    // Add user message
    addMessage('user', userMessage);

    // Prepare conversation history
    const history = messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));

    setIsLoading(true);

    try {
      // Send to backend
      const response = await sendMessage(userMessage, mode, history);

      // Add assistant response
      addMessage('assistant', response.message, response.products);
    } catch (err) {
      setError(err.message || 'Failed to send message');
      addMessage('assistant', '❌ Sorry, I encountered an error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.length === 0 ? (
          <WelcomeScreen />
        ) : (
          <>
            {messages.map((msg) => (
              <Message key={msg.id} message={msg} />
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <span className="loading"></span>
                  <span className="loading" style={{ animationDelay: '0.2s' }}></span>
                  <span className="loading" style={{ animationDelay: '0.4s' }}></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <form onSubmit={handleSubmit} className="input-area">
        <div className="input-container">
          <textarea
            ref={textareaRef}
            className="message-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              mode === 'shopping'
                ? 'What are you looking for?'
                : 'Ask me anything...'
            }
            rows={1}
            disabled={isLoading}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!input.trim() || isLoading}
            aria-label="Send message"
          >
            ➤
          </button>
        </div>
      </form>
    </div>
  );
}
