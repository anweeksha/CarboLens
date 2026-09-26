import { useId } from 'react';

const TrajectoryChart = () => {
  const gradientId = useId();
  const currentGradientId = `currentGradient-${gradientId}`;
  const baselineGradientId = `baselineGradient-${gradientId}`;

  return (
    <section className="rounded-xl bg-[#141414] border border-white/[0.07] p-6 flex flex-col gap-4 shadow-sm">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-[#1E1E1E]">
        <div>
          <h2 className="text-lg font-semibold text-[#F2F2F2] tracking-tight">Campus carbon trajectory</h2>
          <p className="text-xs text-[#AFAFAF]">6-month institutional telemetry trend versus targeted decarbonization glidepath.</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-[#F2F2F2]"></span>
            <span className="text-xs text-[#F2F2F2]">Current Period (Verified)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-[#5F5F5F]"></span>
            <span className="text-xs text-[#AFAFAF]">Previous Period</span>
          </div>
          <div className="hidden sm:flex items-center gap-1.5">
            <span className="w-3 h-0.5 border-t border-dashed border-[#5F5F5F]"></span>
            <span className="text-xs text-[#5F5F5F]">Target Ceiling</span>
          </div>
        </div>
      </div>

      {/* Chart Graphic */}
      <div className="relative w-full h-72 pt-2">
        <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 900 240">
          <defs>
            <linearGradient id={currentGradientId} x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.14"></stop>
              <stop offset="100%" stopColor="#ffffff" stopOpacity="0.00"></stop>
            </linearGradient>
            <linearGradient id={baselineGradientId} x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#5F5F5F" stopOpacity="0.08"></stop>
              <stop offset="100%" stopColor="#5F5F5F" stopOpacity="0.00"></stop>
            </linearGradient>
          </defs>
          {/* Horizontal Reference Lines */}
          <line stroke="#1E1E1E" strokeWidth="1" x1="40" x2="880" y1="30" y2="30"></line>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="10" textAnchor="end" x="30" y="34">180t</text>
          <line stroke="#1E1E1E" strokeWidth="1" x1="40" x2="880" y1="80" y2="80"></line>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="10" textAnchor="end" x="30" y="84">160t</text>
          <line stroke="#1E1E1E" strokeWidth="1" x1="40" x2="880" y1="130" y2="130"></line>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="10" textAnchor="end" x="30" y="134">140t</text>
          <line stroke="#1E1E1E" strokeWidth="1" x1="40" x2="880" y1="180" y2="180"></line>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="10" textAnchor="end" x="30" y="184">120t</text>
          {/* Target ceiling dashline */}
          <line stroke="#444444" strokeDasharray="4,4" strokeWidth="1" x1="40" x2="880" y1="110" y2="148"></line>
          {/* Previous Period Area & Line */}
          <path d="M 60,75 C 200,85 360,95 500,90 C 640,86 760,98 860,105 L 860,200 L 60,200 Z" fill={`url(#${baselineGradientId})`}></path>
          <path d="M 60,75 C 200,85 360,95 500,90 C 640,86 760,98 860,105" fill="none" stroke="#444444" strokeDasharray="3,3" strokeWidth="1.5"></path>
          {/* Current Period Area & Line */}
          <path d="M 60,60 C 210,72 370,110 520,122 C 670,134 760,120 860,124 L 860,200 L 60,200 Z" fill={`url(#${currentGradientId})`}></path>
          <path d="M 60,60 C 210,72 370,110 520,122 C 670,134 760,120 860,124" fill="none" stroke="#F2F2F2" strokeWidth="2.5"></path>
          {/* Data Points */}
          <circle cx="60" cy="60" fill="#0B0B0B" r="3.5" stroke="#F2F2F2" strokeWidth="2"></circle>
          <circle cx="220" cy="74" fill="#0B0B0B" r="3.5" stroke="#F2F2F2" strokeWidth="2"></circle>
          <circle cx="380" cy="112" fill="#0B0B0B" r="3.5" stroke="#F2F2F2" strokeWidth="2"></circle>
          <circle cx="540" cy="123" fill="#0B0B0B" r="3.5" stroke="#F2F2F2" strokeWidth="2"></circle>
          <circle cx="700" cy="122" fill="#0B0B0B" r="3.5" stroke="#F2F2F2" strokeWidth="2"></circle>
          <circle cx="860" cy="124" fill="#ffffff" r="4.5" stroke="#0B0B0B" strokeWidth="2"></circle>
          {/* Callout Marker for Record Low */}
          <g transform="translate(720, 68)">
            <rect fill="#1E1E1E" height="28" rx="6" stroke="#333333" strokeWidth="1" width="150"></rect>
            <text fill="#F2F2F2" fontFamily="Geist" fontSize="11" fontWeight="500" x="10" y="18">Nov: 142.6 t CO₂e (Low)</text>
            <line stroke="#F2F2F2" strokeWidth="1" x1="140" x2="140" y1="28" y2="52"></line>
          </g>
          {/* X Axis Markers */}
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="11" textAnchor="middle" x="60" y="222">Jun</text>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="11" textAnchor="middle" x="220" y="222">Jul</text>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="11" textAnchor="middle" x="380" y="222">Aug</text>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="11" textAnchor="middle" x="540" y="222">Sep</text>
          <text fill="#5F5F5F" fontFamily="Geist" fontSize="11" textAnchor="middle" x="700" y="222">Oct</text>
          <text fill="#F2F2F2" fontFamily="Geist" fontSize="11" fontWeight="600" textAnchor="middle" x="860" y="222">Nov (Active)</text>
        </svg>
      </div>
      {/* Footer Note of Telemetry */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between text-[#AFAFAF] text-xs pt-3 border-t border-[#1E1E1E] gap-2">
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1.5 text-[#F2F2F2]">
            <span className="w-1.5 h-1.5 rounded-full bg-white"></span>
            1,480 telemetry sensors online
          </span>
          <span className="text-[#5F5F5F]">•</span>
          <span className="text-[#5F5F5F]">Gateway poll frequency: 60s</span>
        </div>
        <div>
          <span className="">Decarbonization pathway delta: <span className="text-[#F2F2F2] font-medium">-15.4%</span> against 2023 baseline</span>
        </div>
      </div>
    </section>
  );
};

export default TrajectoryChart;