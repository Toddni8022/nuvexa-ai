/**
 * Mode selector component for switching between assistant modes
 */
import { useApp } from '../contexts/AppContext';

export default function ModeSelector() {
  const { mode, modes, changeMode } = useApp();

  if (modes.length === 0) return null;

  return (
    <div className="mode-selector">
      {modes.map((m) => (
        <button
          key={m.id}
          className={`mode-button ${mode === m.id ? 'active' : ''}`}
          onClick={() => changeMode(m.id)}
        >
          <span className="icon">{m.icon}</span>
          <span>{m.name}</span>
        </button>
      ))}
    </div>
  );
}
