import KPICard from '../components/KPICard';
import TrajectoryChart from '../components/TrajectoryChart';
import EmissionsCategory from '../components/EmissionsCategory';
import ParticipationDonut from '../components/ParticipationDonut';
import OpportunityCard from '../components/OpportunityCard';
import DepartmentRanking from '../components/DepartmentRanking';

const CampusPage = () => {
  return (
    <div className="flex flex-col gap-6">
      {/* Campus Page Header */}
      <section className="flex flex-col lg:flex-row lg:items-end justify-between gap-4 pb-6 border-b border-[#1E1E1E]">
        <div className="flex flex-col gap-1.5 max-w-3xl">
          <div className="flex items-center gap-2">
            <span className="inline-flex w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-wider font-semibold">
              Campus Analytics • Institutional Telemetry v2.4
            </span>
          </div>
          <h1 className="text-3xl lg:text-4xl text-[#F2F2F2] font-semibold tracking-tight">
            The campus, in numbers.
          </h1>
          <p className="text-sm text-[#AFAFAF] leading-relaxed">
            Track emissions, participation, and systemic reduction opportunities across the institution in real time.
          </p>
        </div>
        {/* Header Controls */}
        <div className="flex items-center flex-wrap gap-2.5">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#141414] border border-[#1E1E1E] text-[#AFAFAF] hover:text-[#F2F2F2] hover:border-white/20 transition-colors cursor-pointer text-xs font-medium">
            <span className="material-symbols-outlined text-[16px] text-[#AFAFAF]">calendar_today</span>
            <span className="text-[#F2F2F2]">Term 01 (Fall Cycle)</span>
            <span className="material-symbols-outlined text-[16px] text-[#5F5F5F]">expand_more</span>
          </div>
          <button className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-[#1E1E1E] hover:bg-white hover:text-black border border-white/10 text-[#F2F2F2] text-xs font-medium transition-all shadow-sm" type="button">
            <span className="material-symbols-outlined text-[16px]">file_download</span>
            <span className="">Export Institutional Audit</span>
          </button>
        </div>
      </section>

      {/* Top KPI Matrix (4 Cards) */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          label="Total Campus Footprint"
          icon="co2"
          value="142.6"
          unit="t CO₂e"
          trend={{ value: -8.4, label: "vs previous cycle benchmark" }}
        />
        <KPICard
          label="Cycle Pace Change"
          icon="trending_down"
          value="↓ 8.4%"
          showArrow={false}
          footer={{ left: "Net Decarbonization Pacing", right: "2030 Target" }}
        />
        <KPICard
          label="Community Engagement"
          icon="groups"
          value="3,421"
          unit="active"
          footer={{ left: "Students & Faculty", right: "14 Divisions" }}
        />
        <KPICard
          label="Verified Telemetry"
          icon="verified"
          value="12,482"
          unit="events"
          footer={{ left: "Hardware & RFID feed", right: "98.4% Confidence" }}
        />
      </section>

      {/* Main Chart Section: Trajectory */}
      <TrajectoryChart />

      {/* Asymmetric 2-Column Institutional Deep Dive */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN: Categories & Community (7 Cols) */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          {/* Emissions by Category */}
          <div className="rounded-xl bg-[#141414] border border-white/[0.07] p-6 flex flex-col gap-4 shadow-sm">
            <div className="flex items-center justify-between pb-3 border-b border-[#1E1E1E]">
              <div>
                <h3 className="text-base font-semibold text-[#F2F2F2]">Emissions by category</h3>
                <p className="text-xs text-[#AFAFAF]">Breakdown of gross carbon equivalents across primary campus ops</p>
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#1E1E1E] border border-white/5 text-[#AFAFAF]">4 Sectors Logged</span>
            </div>
            
            <div className="flex flex-col gap-4 pt-1">
              <EmissionsCategory
                icon="directions_bus"
                name="Transportation"
                description="Commuter trips, shuttle fleets & deliveries"
                value="68.4 t"
                percentage="48.0%"
                barColor="bg-white"
                barWidth="48%"
              />
              <EmissionsCategory
                icon="bolt"
                name="Electricity & Power"
                description="HPC clusters, cleanrooms & campus HVAC"
                value="41.2 t"
                percentage="28.9%"
                barColor="bg-[#B8B8B8]"
                barWidth="28.9%"
              />
              <EmissionsCategory
                icon="restaurant"
                name="Dining & Sustenance"
                description="Central cafeteria, mess halls & vending cold-chain"
                value="23.8 t"
                percentage="16.7%"
                barColor="bg-[#757575]"
                barWidth="16.7%"
              />
              <EmissionsCategory
                icon="delete_sweep"
                name="Waste & Materials"
                description="Landfill loads, e-waste & packaging disposal"
                value="9.2 t"
                percentage="6.4%"
                barColor="bg-[#444444]"
                barWidth="6.4%"
              />
            </div>
          </div>

          {/* Campus Participation Card with Orbital Donut Visual */}
          <ParticipationDonut />
        </div>

        {/* RIGHT COLUMN: Highest Opportunity Hero Lever & Department Rankings (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* Highest Reduction Opportunity (Hero Lever Card) */}
          <OpportunityCard />

          {/* Department Comparison Rankings */}
          <DepartmentRanking />
        </div>
      </div>
    </div>
  );
};

export default CampusPage;