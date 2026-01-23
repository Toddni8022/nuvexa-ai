/**
 * Welcome screen displayed when no messages
 */
import { useApp } from '../contexts/AppContext';

export default function WelcomeScreen() {
  const { mode } = useApp();

  const features = {
    assistant: [
      '💡 Get helpful advice and answers',
      '📝 Plan projects and tasks',
      '🎯 Solve problems efficiently',
    ],
    shopping: [
      '🛍️ Find products easily',
      '💰 Compare prices',
      '⭐ See ratings and reviews',
    ],
  };

  return (
    <div className="welcome">
      <div className="welcome-icon">🤖</div>
      <h2>Welcome to NUVEXA</h2>
      <p>Your AI assistant is ready to help</p>

      <div className="welcome-features">
        {(features[mode] || features.assistant).map((feature, index) => (
          <div key={index} className="feature-item">
            {feature}
          </div>
        ))}
      </div>
    </div>
  );
}
