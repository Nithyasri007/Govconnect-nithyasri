import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { DocumentUpload } from './pages/DocumentUpload';
import { VoiceInput } from './pages/VoiceInput';
import { ManualForm } from './pages/ManualForm';
import { SchemeResults } from './pages/SchemeResults';
import { ApplicationForm } from './pages/ApplicationForm';
import { Auth } from './pages/Auth';
import { BrowseSchemes } from './pages/BrowseSchemes';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload/document" element={<DocumentUpload />} />
          <Route path="/upload/voice" element={<VoiceInput />} />
          <Route path="/form/manual" element={<ManualForm />} />
          <Route path="/schemes" element={<BrowseSchemes />} />
          <Route path="/schemes/results" element={<SchemeResults />} />
          <Route path="/application/:schemeId" element={<ApplicationForm />} />
          <Route path="/auth" element={<Auth />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;