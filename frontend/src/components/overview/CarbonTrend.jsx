import { useId } from 'react';

const CarbonTrend = () => {
  const gradientId = useId();
  const curveGradientId = `curveGradient-${gradientId}`;

  return (
    <section className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
      {/* Left (Wide Analytics Card - 8 Cols) */}
      <div className="lg:col-span-8 p-6 lg:p-8 rounded-[24px] bg-[#141414] flex flex-col justify-between relative shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6">
          <div>
            <h2 className="text-xl text-[#F2F2F2] font-medium tracking-tight">Carbon trajectory</h2>
            <p className="text-sm text-[#AFAFAF]">Your estimated footprint over the last 6 months</p>
          </div>
          <span className="inline-block px-3 py-1 rounded-full bg-[#2a2a2a] text-[#F2F2F2] text-[11px] tracking-wider uppercase self-start sm:self-auto">
            6 MONTHS
          </span>
        </div>
        {/* SVG Chart Visualization with Grayscale Area Gradient */}
        <div className="relative w-full h-64 mt-4">
          {/* Dashed Horizon Grids */}
          <div className="absolute inset-0 flex flex-col justify-between pointer-events-none opacity-20">
            <div className="w-full h-px bg-white border-b border-dashed border-white"></div>
            <div className="w-full h-px bg-white border-b border-dashed border-white"></div>
            <div className="w-full h-px bg-white border-b border-dashed border-white"></div>
            <div className="w-full h-px bg-white border-b border-dashed border-white"></div>
          </div>
          <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 700 220">
            <defs>
              <linearGradient id={curveGradientId} x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#ffffff" stopOpacity="0.18"></stop>
                <stop offset="100%" stopColor="#ffffff" stopOpacity="0"></stop>
              </linearGradient>
            </defs>
            {/* Secondary subtle benchmark dashed line (Campus Average) */}
            <path className="text-white/20" d="M 0,90 Q 140,85 280,80 T 560,75 T 700,70" fill="none" stroke="currentColor" strokeDasharray="4 6" strokeWidth="1.5"></path>
            {/* Area fill */}
            <path d="M 0,160 C 140,140 180,110 280,125 C 380,140 440,75 560,95 C 620,105 660,135 700,140 L 700,220 L 0,220 Z" fill={`url(#${curveGradientId})`}></path>
            {/* Primary Curve */}
            <path d="M 0,160 C 140,140 180,110 280,125 C 380,140 440,75 560,95 C 620,105 660,135 700,140" fill="none" stroke="#ffffff" strokeLinecap="round" strokeWidth="2.5"></path>
            {/* Key Active Data Points */}
            <circle className="cursor-pointer" cx="560" cy="95" fill="#ffffff" r="4.5" stroke="#141414" strokeWidth="2"></circle>
            <circle className="cursor-pointer animate-ping opacity-75" cx="700" cy="140" fill="#ffffff" r="5" stroke="#141414" strokeWidth="2"></circle>
            <circle cx="700" cy="140" fill="#ffffff" r="5"></circle>
          </svg>
          {/* Floating Data Tooltip Indicator positioned over February marker */}
          <div className="absolute top-10 left-[72%] -translate-x-1/2 rounded-xl bg-[#353534]/90 backdrop-blur-xl p-3 shadow-2xl pointer-events-none border border-white/5">
            <div className="flex items-center gap-2 text-[11px] text-[#AFAFAF]">
              <span className="w-1.5 h-1.5 rounded-full bg-white"></span>
              <span>February Peak</span>
            </div>
            <span className="text-xl text-[#F2F2F2] font-semibold">198.2 kg</span>
          </div>
        </div>
        {/* X-Axis Labels */}
        <div className="flex items-center justify-between text-[#AFAFAF] text-[11px] pt-4">
          <span>Oct</span>
          <span>Nov</span>
          <span>Dec</span>
          <span>Jan</span>
          <span className="text-[#F2F2F2] font-medium">Feb</span>
          <span className="text-[#F2F2F2] font-bold">Mar (Current)</span>
        </div>
      </div>
      {/* Right (Prominent Opportunity Card - 4 Cols) */}
      <div className="lg:col-span-4 p-6 lg:p-8 rounded-[24px] bg-[#1A1A1A] flex flex-col justify-between relative overflow-hidden shadow-xl">
        {/* Radial highlight */}
        <div className="pointer-events-none absolute -top-20 -right-20 w-64 h-64 rounded-full bg-white/5 blur-2xl"></div>
        <div className="flex flex-col gap-4 z-10">
          <div className="flex items-center justify-between">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] tracking-wider uppercase">HIGHEST IMPACT OPPORTUNITY</span>
            <span className="material-symbols-outlined text-[#F2F2F2] text-[20px]">bolt</span>
          </div>
          <h3 className="text-xl text-[#F2F2F2] font-semibold leading-tight pt-2">
            Switch 10 car trips to public transport.
          </h3>
          <p className="text-sm text-[#AFAFAF]">
            Subway & inter-campus transit lines eliminate up to 82% of transit combustion per passenger mile.
          </p>
          {/* Stat Highlight Block */}
          <div className="p-4 rounded-xl bg-[#0e0e0e] flex flex-col gap-1 mt-2">
            <span className="text-[11px] text-[#AFAFAF] uppercase tracking-wider">Potential saving</span>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl text-[#F2F2F2] font-semibold">31.4</span>
              <span className="text-[13px] text-[#AFAFAF]">kg CO₂e / month</span>
            </div>
          </div>
        </div>
        <div className="pt-6 z-10">
          <button className="w-full group flex items-center justify-between px-4 py-3 rounded-xl bg-white text-black hover:bg-[#AFAFAF] transition-all active:scale-[0.98]" type="button">
            <span className="text-[13px] font-semibold">Explore scenario</span>
            <span className="material-symbols-outlined text-[18px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
          </button>
        </div>
      </div>
    </section>
  );
};

export default CarbonTrend;