const AttributionCards = () => {
  const attributions = [
    { num: '01', title: 'Transportation', badge: 'Primary', desc: 'Commute between North Campus & Labs (approx. 14 trips/wk)', value: '72.4 kg CO₂e', percent: '39%' },
    { num: '02', title: 'Electricity', badge: 'High compute', desc: 'Studio workstation compute & dorm AC consumption', value: '51.2 kg CO₂e', percent: '28%' },
    { num: '03', title: 'Food', badge: 'Dietary', desc: 'Campus dining, red meat frequency & packaging impact', value: '48.0 kg CO₂e', percent: '26%' },
  ];

  return (
    <section className="flex flex-col gap-6 mb-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-widest">ACTIVITY ATTRIBUTION</span>
        <h2 className="text-2xl text-[#F2F2F2] font-semibold tracking-tight">What's driving your footprint?</h2>
        <p className="text-sm text-[#AFAFAF]">
          Granular sensor telemetry and logged receipts isolate the exact behavioral clusters generating campus carbon load.
        </p>
      </div>
      {/* 3 Large Horizontal Cards with oversized numbered indices */}
      <div className="flex flex-col gap-6">
        {attributions.map((attr, index) => (
          <div key={index} className="group relative flex flex-col md:flex-row items-start md:items-center justify-between p-6 rounded-[24px] bg-[#141414] hover:bg-[#1A1A1A] transition-all duration-300">
            <div className="flex items-start md:items-center gap-6">
              <span className="text-5xl text-white/20 group-hover:text-white/40 transition-colors font-light select-none">
                {attr.num}
              </span>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2">
                  <h3 className="text-xl text-[#F2F2F2] font-medium">{attr.title}</h3>
                  <span className="px-2 py-0.5 rounded bg-[#2a2a2a] text-[#F2F2F2] text-[11px]">{attr.badge}</span>
                </div>
                <p className="text-sm text-[#AFAFAF]">
                  {attr.desc}
                </p>
              </div>
            </div>
            <div className="flex items-end md:items-center gap-6 mt-4 md:mt-0 self-end md:self-auto">
              <div className="flex flex-col md:items-end">
                <span className="text-xl text-[#F2F2F2] font-semibold">{attr.value}</span>
                <span className="text-[11px] text-[#AFAFAF]">{attr.percent} of your total footprint</span>
              </div>
              <span className="material-symbols-outlined text-[#AFAFAF] group-hover:text-[#F2F2F2] group-hover:translate-x-1 transition-all">chevron_right</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default AttributionCards;