import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import {
  OverviewPage,
  ActivitiesPage,
  CarbonPage,
  SimulatorPage,
  RecommendationsPage,
  ChallengesPage,
  LeaderboardPage,
  CampusPage,
  ReportsPage,
} from './pages';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/overview" replace />} />
          <Route path="overview" element={<OverviewPage />} />
          <Route path="activities" element={<ActivitiesPage />} />
          <Route path="carbon" element={<CarbonPage />} />
          <Route path="simulator" element={<SimulatorPage />} />
          <Route path="recommendations" element={<RecommendationsPage />} />
          <Route path="challenges" element={<ChallengesPage />} />
          <Route path="leaderboard" element={<LeaderboardPage />} />
          <Route path="campus" element={<CampusPage />} />
          <Route path="reports" element={<ReportsPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
