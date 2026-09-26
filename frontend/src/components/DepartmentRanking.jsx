const DepartmentRanking = () => {
  const departments = [
    { rank: "01 CSE", peers: "820 peers • 39.5 kg/ea", value: "32.4 t", barWidth: "82%", barColor: "bg-white" },
    { rank: "02 ECE", peers: "640 peers • 42.3 kg/ea", value: "27.1 t", barWidth: "68%", barColor: "bg-[#B8B8B8]" },
    { rank: "03 ME", peers: "580 peers • 40.7 kg/ea", value: "23.6 t", barWidth: "59%", barColor: "bg-[#8E8E8E]" },
    { rank: "04 Civil", peers: "410 peers • 48.3 kg/ea", value: "19.8 t", barWidth: "49%", barColor: "bg-[#646464]" },
    { rank: "05 Hostel B", peers: "490 residents • 35.5 kg/ea", value: "17.4 t", barWidth: "43%", barColor: "bg-[#444444]" },
  ];

  return (
    <div className="rounded-xl bg-[#141414] border border-white/[0.07] p-6 flex flex-col gap-4 shadow-sm">
      <div className="flex items-center justify-between pb-3 border-b border-[#1E1E1E]">
        <div>
          <h3 className="text-base font-semibold text-[#F2F2F2]">Department comparison</h3>
          <p className="text-xs text-[#AFAFAF]">Aggregated gross emissions by division</p>
        </div>
        <span className="material-symbols-outlined text-[#5F5F5F] text-[18px]">domain</span>
      </div>
      {/* Rankings List */}
      <div className="flex flex-col gap-3.5 pt-1">
        {departments.map((dept, index) => (
          <div key={index} className="flex flex-col gap-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium text-[#F2F2F2]">{dept.rank} <span className="text-[11px] text-[#5F5F5F] font-normal">/ {dept.peers}</span></span>
              <span className="font-semibold text-[#F2F2F2] font-mono">{dept.value}</span>
            </div>
            <div className="w-full h-1 bg-[#1E1E1E] rounded-full overflow-hidden">
              <div className={`h-full ${dept.barColor} rounded-full`} style={{ width: dept.barWidth }}></div>
            </div>
          </div>
        ))}
      </div>
      <div className="pt-3 border-t border-[#1E1E1E] flex items-center justify-between">
        <span className="text-[11px] text-[#5F5F5F]">Normalizing per capita by lab operating hours</span>
        <a className="text-xs text-[#F2F2F2] hover:text-white hover:underline inline-flex items-center gap-0.5" href="#">
          <span className="">View full 14 units</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
        </a>
      </div>
    </div>
  );
};

export default DepartmentRanking;