const OpportunityCard = () => {
  return (
    <div className="relative overflow-hidden rounded-xl bg-[#141414] border border-white/[0.07] p-6 flex flex-col justify-between gap-5 shadow-sm">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            <span className="material-symbols-outlined text-[18px] text-white">crisis_alert</span>
            <span className="text-[11px] text-white uppercase font-semibold tracking-wider">
              Highest Sensitivity Lever
            </span>
          </div>
          <span className="px-2 py-0.5 rounded-full bg-[#1E1E1E] border border-white/5 text-[#AFAFAF] text-[11px]">
            Transit Fleet
          </span>
        </div>
        <h3 className="text-base text-[#F2F2F2] font-medium leading-snug mt-1">
          An estimated <span className="font-semibold underline decoration-white/40 decoration-1 underline-offset-4 text-white">8.7 t CO₂e/month</span> could be avoided through increased public transport adoption.
        </h3>
        <p className="text-xs text-[#AFAFAF] leading-relaxed">
          Optimizing North Campus electric shuttle frequency from 15m to 7m headway and subsidizing local metro card taps will immediately capture 420 single-occupant commuter trips.
        </p>
      </div>
      {/* Key Metrics Mini Strip */}
      <div className="grid grid-cols-3 gap-2 py-2.5 px-3 bg-[#1A1A1A] rounded-lg border border-[#252525]">
        <div className="flex flex-col">
          <span className="text-[10px] text-[#5F5F5F] uppercase font-semibold">Net Saving</span>
          <span className="text-xs text-[#F2F2F2] font-bold">8.7 t / mo</span>
        </div>
        <div className="flex flex-col">
          <span className="text-[10px] text-[#5F5F5F] uppercase font-semibold">Feasibility</span>
          <span className="text-xs text-[#F2F2F2] font-medium">Immediate</span>
        </div>
        <div className="flex flex-col">
          <span className="text-[10px] text-[#5F5F5F] uppercase font-semibold">Impact</span>
          <span className="text-xs text-[#F2F2F2] font-semibold">-6.1% Gross</span>
        </div>
      </div>
      {/* Action CTA Group */}
      <div className="flex items-center gap-2.5 pt-1">
        <button className="w-full inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg bg-white hover:bg-[#E5E5E5] transition-all text-black text-xs font-semibold shadow-sm" type="button">
          <span className="">Explore opportunity</span>
          <span className="material-symbols-outlined text-[15px]">arrow_forward</span>
        </button>
        <button className="inline-flex items-center justify-center px-4 py-2 rounded-lg bg-[#1E1E1E] hover:bg-[#252525] border border-white/5 text-[#F2F2F2] text-xs font-medium transition-colors" type="button">
          <span className="">Simulator</span>
        </button>
      </div>
    </div>
  );
};

export default OpportunityCard;