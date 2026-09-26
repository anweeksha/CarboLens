import OverviewHeader from '../components/overview/OverviewHeader';
import HeroCarbonCard from '../components/overview/HeroCarbonCard';
import CarbonBreakdown from '../components/overview/CarbonBreakdown';
import CarbonTrend from '../components/overview/CarbonTrend';
import AttributionCards from '../components/overview/AttributionCards';
import SimulatorPreview from '../components/overview/SimulatorPreview';
import CampusImpact from '../components/overview/CampusImpact';
import ChallengesSection from '../components/overview/ChallengesSection';

const OverviewPage = () => {
  return (
    <div className="flex flex-col gap-6">
      <OverviewHeader />
      <HeroCarbonCard />
      <CarbonBreakdown />
      <CarbonTrend />
      <AttributionCards />
      <SimulatorPreview />
      <CampusImpact />
      <ChallengesSection />
    </div>
  );
};

export default OverviewPage;