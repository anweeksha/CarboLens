const EmissionsCategory = ({ icon, name, description, value, percentage, barColor, barWidth }) => {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-[#1E1E1E] border border-white/5 flex items-center justify-center text-[#F2F2F2]">
            <span className="material-symbols-outlined text-[16px]">{icon}</span>
          </div>
          <div>
            <span className="text-xs font-medium text-[#F2F2F2] block leading-tight">{name}</span>
            <span className="text-[11px] text-[#AFAFAF]">{description}</span>
          </div>
        </div>
        <div className="text-right">
          <span className="text-xs font-semibold text-[#F2F2F2]">{value}</span>
          <span className="text-[11px] text-[#AFAFAF] ml-1">({percentage})</span>
        </div>
      </div>
      <div className="w-full h-1.5 bg-[#1E1E1E] rounded-full overflow-hidden">
        <div className={`h-full ${barColor} rounded-full`} style={{ width: barWidth }}></div>
      </div>
    </div>
  );
};

export default EmissionsCategory;