const CarbonBreakdown = () => {
  const categories = [
    { name: 'TRAVEL', sub: 'Commutes & transit', value: '72.4', percent: '39', icon: 'directions_car', barWidth: '39%' },
    { name: 'ELECTRICITY', sub: 'Labs & dorm supply', value: '51.2', percent: '28', icon: 'bolt', barWidth: '28%' },
    { name: 'FOOD', sub: 'Dining & groceries', value: '48.0', percent: '26', icon: 'restaurant', barWidth: '26%' },
    { name: 'WASTE', sub: 'Packaging & landfill', value: '13.0', percent: '7', icon: 'sync', barWidth: '7%' },
  ];

  return (
    <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {categories.map((cat, index) => (
        <div key={index} className="group relative flex flex-col justify-between p-6 rounded-[24px] bg-[#141414] hover:bg-[#1A1A1A] transition-all duration-300 transform hover:-translate-y-1 shadow-md">
          <div className="flex items-center justify-between pb-6">
            <div className="flex flex-col">
              <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] tracking-wider uppercase">{cat.name}</span>
              <span className="text-[11px] text-[#AFAFAF]">{cat.sub}</span>
            </div>
            <div className="w-10 h-10 rounded-full bg-[#2a2a2a] flex items-center justify-center text-[#F2F2F2] group-hover:scale-110 transition-transform">
              <span className="material-symbols-outlined text-[20px]">{cat.icon}</span>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <div className="flex items-baseline justify-between">
              <span className="text-3xl text-[#F2F2F2] font-semibold tracking-tight">{cat.value}</span>
              <span className="text-xl text-[#AFAFAF] font-light">{cat.percent}%</span>
            </div>
            <span className="text-[11px] text-[#AFAFAF] pb-2">kg CO₂e recorded</span>
            {/* Hairline Progress Bar */}
            <div className="w-full h-[2px] bg-[#353534] rounded-full overflow-hidden">
              <div className="h-full bg-white transition-all duration-700" style={{ width: cat.barWidth }}></div>
            </div>
          </div>
        </div>
      ))}
    </section>
  );
};

export default CarbonBreakdown;