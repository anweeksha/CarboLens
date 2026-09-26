const HeroCarbonCard = () => {
  return (
    <section className="relative w-full rounded-[24px] bg-[#141414] overflow-hidden p-6 lg:p-8 mb-8 shadow-2xl transition-all duration-500 hover:shadow-[0_20px_50px_rgba(0,0,0,0.8)]">
      {/* Atmospheric Ambient Glow */}
      <div className="pointer-events-none absolute -top-40 -left-40 w-96 h-96 rounded-full bg-white/5 blur-3xl"></div>
      <div className="pointer-events-none absolute top-1/2 right-10 -translate-y-1/2 w-[520px] h-[520px] rounded-full bg-gradient-to-br from-white/[0.04] to-transparent blur-2xl"></div>
      {/* Orbit concentric vector rings background */}
      <div className="pointer-events-none absolute -right-24 -top-24 w-[600px] h-[600px] opacity-25 hidden md:block">
        <svg className="w-full h-full animate-[spin_120s_linear_infinite]" fill="none" stroke="currentColor" viewBox="0 0 600 600">
          <circle className="text-white/20" cx="300" cy="300" r="280" strokeDasharray="4 8" strokeWidth="1"></circle>
          <circle className="text-white/30" cx="300" cy="300" r="220" strokeWidth="1.5"></circle>
          <circle className="text-white/40" cx="300" cy="300" r="160" strokeDasharray="2 6" strokeWidth="1"></circle>
          <circle className="text-white/20" cx="300" cy="300" r="100" strokeWidth="1"></circle>
          <circle className="text-white/60" cx="300" cy="300" r="40" strokeDasharray="6 6" strokeWidth="1.5"></circle>
          <line className="text-white/15" strokeDasharray="3 9" strokeWidth="0.75" x1="300" x2="300" y1="20" y2="580"></line>
          <line className="text-white/15" strokeDasharray="3 9" strokeWidth="0.75" x1="20" x2="580" y1="300" y2="300"></line>
        </svg>
      </div>
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Main Stat Block */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <span className="font-eyebrow-tag text-[11px] tracking-widest text-[#AFAFAF] uppercase">MONTHLY FOOTPRINT</span>
            <span className="w-1 h-1 rounded-full bg-[#AFAFAF]"></span>
            <span className="text-[11px] text-[#AFAFAF]">MARCH 2025 CYCLE</span>
          </div>
          <div className="flex flex-wrap items-baseline gap-x-4 gap-y-0">
            <span className="text-6xl text-[#F2F2F2] tracking-tight font-semibold">184.6</span>
            <span className="text-2xl text-[#AFAFAF] font-light">kg CO₂e</span>
          </div>
          <div className="flex flex-wrap items-center gap-2 pt-2">
            {/* Trend Pill */}
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#2a2a2a] text-[#F2F2F2] text-[13px] font-medium">
              <span className="material-symbols-outlined text-[16px]">arrow_downward</span>
              <span>12.4% from last month</span>
            </div>
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] tracking-wider uppercase">LOWER THAN YOUR PREVIOUS MONTH</span>
          </div>
        </div>
        {/* Sub-stat badges / benchmark cards on right side */}
        <div className="lg:col-span-5 flex flex-col sm:flex-row lg:flex-col gap-4 justify-end">
          <div className="flex items-center justify-between p-4 rounded-xl bg-[#0e0e0e] backdrop-blur-md transition-all hover:bg-[#1c1b1b]">
            <div className="flex flex-col">
              <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-wider">Target Profile</span>
              <span className="text-xl text-[#F2F2F2] font-medium">160.0 kg</span>
            </div>
            <div className="text-right flex flex-col items-end">
              <span className="text-[11px] text-[#AFAFAF]">24.6 kg surplus</span>
              <div className="w-24 h-1.5 rounded-full bg-[#353534] mt-1 overflow-hidden">
                <div className="h-full bg-white" style={{ width: '86%' }}></div>
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between p-4 rounded-xl bg-[#0e0e0e] backdrop-blur-md transition-all hover:bg-[#1c1b1b]">
            <div className="flex flex-col">
              <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-wider">Campus Avg</span>
              <span className="text-xl text-[#F2F2F2] font-medium">212.4 kg</span>
            </div>
            <div className="text-right">
              <span className="inline-flex items-center gap-1 text-[11px] text-[#F2F2F2]">
                <span className="material-symbols-outlined text-[14px]">check_circle</span>
                13.1% below avg
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between p-4 rounded-xl bg-[#0e0e0e] backdrop-blur-md transition-all hover:bg-[#1c1b1b]">
            <div className="flex flex-col">
              <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-wider">Global Net Zero Pace</span>
              <span className="text-xl text-[#F2F2F2] font-medium">-3.2%</span>
            </div>
            <div className="text-right">
              <span className="text-[11px] text-[#AFAFAF]">Annualized trajectory</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroCarbonCard;