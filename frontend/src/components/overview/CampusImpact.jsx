const CampusImpact = () => {
  const departments = [
    { name: 'CSE (Your Dept.)', value: '32.4 t', barWidth: '82%', color: 'bg-white' },
    { name: 'ECE', value: '27.1 t', barWidth: '68%', color: 'bg-[#AFAFAF]' },
    { name: 'ME', value: '23.6 t', barWidth: '59%', color: 'bg-[#AFAFAF]' },
    { name: 'Hostel B', value: '19.8 t', barWidth: '48%', color: 'bg-[#c4c7c8]' },
  ];

  return (
    <section className="flex flex-col gap-6 mb-8">
      <div className="flex flex-col gap-2 max-w-3xl">
        <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-widest">NETWORK BENCHMARK</span>
        <h2 className="text-2xl text-[#F2F2F2] font-semibold tracking-tight">Your footprint is part of something bigger.</h2>
        <p className="text-sm text-[#AFAFAF]">Aggregated emissions and collective progress across Oxford University West Campus.</p>
      </div>
      {/* Campus Top Banner */}
      <div className="flex flex-wrap items-center justify-between p-4 lg:p-6 rounded-2xl bg-[#0e0e0e] gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-[#2a2a2a] flex items-center justify-center text-[#F2F2F2]">
            <span className="material-symbols-outlined text-[24px]">domain</span>
          </div>
          <div className="flex flex-col">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase">CAMPUS AGGREGATE</span>
            <span className="text-xl text-[#F2F2F2] font-semibold">142.6 t CO₂e this month</span>
          </div>
        </div>
        <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#2a2a2a] text-[#F2F2F2] text-[13px]">
          <span className="material-symbols-outlined text-[16px]">arrow_downward</span>
          <span>↓ 8.4% vs previous month</span>
        </div>
      </div>
      {/* 2-Column Campus Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Department emissions comparison bars (7 cols) */}
        <div className="lg:col-span-7 p-6 rounded-[24px] bg-[#141414] flex flex-col justify-between gap-4 shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-xl text-[#F2F2F2] font-medium">Department Emissions</h3>
            <span className="text-[11px] text-[#AFAFAF]">Active cycle tally</span>
          </div>
          <div className="flex flex-col gap-4 pt-2">
            {departments.map((dept, index) => (
              <div key={index} className="flex flex-col gap-1">
                <div className="flex items-center justify-between text-[13px]">
                  <span className={`${index === 0 ? 'text-[#F2F2F2] font-medium' : 'text-[#AFAFAF]'}`}>{dept.name}</span>
                  <span className="text-[#F2F2F2] font-semibold">{dept.value}</span>
                </div>
                <div className="w-full h-2 rounded-full bg-[#2a2a2a] overflow-hidden">
                  <div className={`h-full ${dept.color}`} style={{ width: dept.barWidth }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* Right: Grid Intensity Gauge & Facility Metrics (5 cols) */}
        <div className="lg:col-span-5 p-6 rounded-[24px] bg-[#141414] flex flex-col justify-between gap-4 shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-xl text-[#F2F2F2] font-medium">Energy Grid Intensity</h3>
            <span className="inline-block px-2 py-0.5 rounded bg-[#2a2a2a] text-[#F2F2F2] text-[11px]">LIVE FEED</span>
          </div>
          {/* Inline Minimal Circular Arc / Gauge */}
          <div className="flex items-center justify-center py-4 relative">
            <svg className="w-48 overflow-visible" viewBox="0 0 140 80">
              <path className="text-[#2a2a2a]" d="M 15 70 A 55 55 0 0 1 125 70" fill="none" stroke="currentColor" strokeLinecap="round" strokeWidth="8"></path>
              <path d="M 15 70 A 55 55 0 0 1 95 24" fill="none" stroke="#ffffff" strokeLinecap="round" strokeWidth="8"></path>
            </svg>
            <div className="absolute bottom-2 flex flex-col items-center">
              <span className="text-xl text-[#F2F2F2] font-bold">142</span>
              <span className="text-[11px] text-[#AFAFAF]">g CO₂/kWh</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-[#0e0e0e] flex items-center justify-between text-[#AFAFAF] text-[13px]">
            <span>Renewables Contribution:</span>
            <span className="text-[#F2F2F2] font-semibold">68.4% Wind + Solar</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CampusImpact;