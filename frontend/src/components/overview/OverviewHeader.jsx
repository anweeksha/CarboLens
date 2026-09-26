const OverviewHeader = () => {
  return (
    <header className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <div className="flex items-center gap-2">
          <span className="inline-block w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
          <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-widest">PERSONAL CARBON PROFILE</span>
        </div>
        <h1 className="text-4xl lg:text-5xl text-[#F2F2F2] tracking-tight font-semibold">
          Your impact, in perspective.
        </h1>
        <p className="text-base text-[#AFAFAF] pt-2">
          Track what matters. Understand what drives your footprint. Make changes that actually count.
        </p>
      </div>
      {/* Right Controls */}
      <div className="flex flex-wrap items-center gap-3 self-start lg:self-end">
        {/* Time Range Segmented Selector */}
        <div className="inline-flex p-1 rounded-full bg-[#0e0e0e] shadow-inner">
          <button className="px-4 py-1.5 rounded-full text-[#F2F2F2] bg-[#2a2a2a] text-[13px] font-medium transition-all" type="button">This Month</button>
          <button className="px-4 py-1.5 rounded-full text-[#AFAFAF] hover:text-[#F2F2F2] text-[13px] font-medium transition-all" type="button">Semester</button>
          <button className="px-4 py-1.5 rounded-full text-[#AFAFAF] hover:text-[#F2F2F2] text-[13px] font-medium transition-all" type="button">Year</button>
        </div>
        {/* Minimalist Dark Graphite Export Button */}
        <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#1c1b1b] hover:bg-[#201f1f] text-[#F2F2F2] text-[13px] font-medium transition-all active:scale-95" type="button">
          <span className="material-symbols-outlined text-[16px]">file_download</span>
          <span>Export Report</span>
        </button>
      </div>
    </header>
  );
};

export default OverviewHeader;