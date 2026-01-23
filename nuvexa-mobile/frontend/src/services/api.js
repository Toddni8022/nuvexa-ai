/**
 * API service for backend communication
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Send chat message to backend
 * @param {string} message - User message
 * @param {string} mode - Conversation mode
 * @param {Array} history - Conversation history
 * @returns {Promise<Object>} Response data
 */
export async function sendMessage(message, mode = 'assistant', history = []) {
  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        mode,
        conversation_history: history,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

/**
 * Search for products
 * @param {string} query - Search query
 * @returns {Promise<Object>} Product results
 */
export async function searchProducts(query) {
  try {
    const response = await fetch(`${API_URL}/api/shop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to search products');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

/**
 * Get available modes
 * @returns {Promise<Object>} Available modes
 */
export async function getModes() {
  try {
    const response = await fetch(`${API_URL}/api/modes`);

    if (!response.ok) {
      throw new Error('Failed to fetch modes');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${API_URL}/api/health`);

    if (!response.ok) {
      throw new Error('Health check failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
}
