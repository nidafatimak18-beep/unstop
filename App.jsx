import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInteractions } from './store/crmSlice';
import ChatInterface from './components/ChatInterface';
import StructuredForm from './components/StructuredForm';
import InteractionList from './components/InteractionList';
import { Activity, MessageSquare, LayoutList } from 'lucide-react';

function App() {
  const dispatch = useDispatch();
  const [activeTab, setActiveTab] = useState('chat');

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <Activity size={28} className="icon-pulse" />
          <h1>Nexus HCP CRM</h1>
        </div>
        <nav className="main-nav">
          <button 
            className={`nav-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageSquare size={18} /> Chat Assistant
          </button>
          <button 
            className={`nav-btn ${activeTab === 'form' ? 'active' : ''}`}
            onClick={() => setActiveTab('form')}
          >
            <LayoutList size={18} /> Manual Entry
          </button>
        </nav>
      </header>

      <main className="app-main">
        <div className="left-panel glass-panel">
          {activeTab === 'chat' ? <ChatInterface /> : <StructuredForm />}
        </div>
        <div className="right-panel glass-panel">
          <InteractionList />
        </div>
      </main>
    </div>
  );
}

export default App;
