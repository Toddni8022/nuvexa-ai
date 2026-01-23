/**
 * Main App component
 */
import { AppProvider } from './contexts/AppContext';
import Header from './components/Header';
import ModeSelector from './components/ModeSelector';
import ChatInterface from './components/ChatInterface';
import './styles/App.css';

function App() {
  return (
    <AppProvider>
      <div className="app">
        <Header />
        <ModeSelector />
        <ChatInterface />
      </div>
    </AppProvider>
  );
}

export default App;
