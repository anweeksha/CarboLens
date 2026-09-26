const ParticipationDonut = () => {
  return (
    <div className="rounded-xl bg-[#141414] border border-white/[0.07] p-6 flex flex-col md:flex-row items-center gap-6 shadow-sm">
      <div className="relative w-40 h-40 flex-shrink-0 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
          <circle cx="80" cy="80" fill="none" r="68" stroke="#1E1E1E" strokeWidth="2"></circle>
          <circle cx="80" cy="80" fill="none" r="56" stroke="#2A2A2A" strokeDasharray="2 3" strokeWidth="1.5"></circle>
          <ellipse cx="80" cy="80" fill="none" rx="70" ry="32" stroke="#444444" strokeOpacity="0.3" strokeWidth="1" transform="rotate(30 80 80)"></ellipse>
          <circle cx="80" cy="80" fill="none" r="56" stroke="#F2F2F2" strokeDasharray="351.8" strokeDashoffset="112.5" strokeLinecap="round" strokeWidth="3.5"></circle>
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-3xl leading-tight text-[#F2F2F2] font-semibold tracking-tight">68%</span>
          <span className="text-[10px] text-[#AFAFAF] uppercase tracking-wider font-semibold">Adherence</span>
        </div>
      </div>
      <div className="flex flex-col gap-2 w-full">
        <div className="flex items-center justify-between">
          <span className="text-base text-[#F2F2F2] font-semibold">Institutional Participation</span>
          <span className="text-xs text-[#F2F2F2] bg-[#1E1E1E] border border-white/5 px-2.5 py-0.5 rounded-full font-medium">+12.4% vs Term 02</span>
        </div>
        <p className="text-xs text-[#AFAFAF] leading-relaxed">
          3,421 out of 5,030 total campus residents and day-scholars regularly authenticate commute and energy telemetry logs.
        </p>
        <div className="grid grid-cols-2 gap-3 pt-3 mt-1 border-t border-[#1E1E1E]">
          <div>
            <span className="text-[10px] text-[#5F5F5F] block uppercase font-semibold">Hostel Residents</span>
            <span className="text-xs text-[#F2F2F2] font-medium">84.2% Active</span>
          </div>
          <div>
            <span className="text-[10px] text-[#5F5F5F] block uppercase font-semibold">Faculty & Staff</span>
            <span className="text-xs text-[#F2F2F2] font-medium">54.9% Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParticipationDonut;