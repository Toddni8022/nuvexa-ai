/**
 * Product card component for displaying product information
 */
export default function ProductCard({ product }) {
  return (
    <div className="product-card">
      <img
        src={product.images[0]}
        alt={product.name}
        className="product-image"
        loading="lazy"
      />
      <div className="product-name">{product.name}</div>
      <div className="product-price">${product.price.toFixed(2)}</div>
      <div className="product-description">{product.description}</div>
      <div className="product-meta">
        <span>⭐ {product.rating}</span>
        <span>{product.source}</span>
      </div>
    </div>
  );
}
