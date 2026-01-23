/**
 * Message component for displaying chat messages
 */
import ProductCard from './ProductCard';

export default function Message({ message }) {
  const isUser = message.role === 'user';
  const avatar = isUser ? '👤' : '🤖';

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-avatar">{avatar}</div>
      <div className="message-content">
        <div>{message.content}</div>

        {/* Display products if available */}
        {message.products && message.products.length > 0 && (
          <div className="products-grid">
            {message.products.map((product, index) => (
              <ProductCard key={index} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
