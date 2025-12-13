import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';

import CampaignManager from './pages/CampaignManager';
import TemplateGenerator from './pages/TemplateGenerator';

import UserResults from './pages/UserResults';
import Education from './pages/Education';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="campaigns" element={<CampaignManager />} />
        <Route path="templates" element={<TemplateGenerator />} />
        <Route path="targets" element={<UserResults />} />
      </Route>
    </Routes>
  );
}

export default App;
