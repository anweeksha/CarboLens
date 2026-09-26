const KPICard = ({ label, icon, value, unit, trend, showArrow = true, footer }) => {
  return (
    <div className="rounded-xl bg-[#141414] border border-white/[0.07] p-5 flex flex-col justify-between gap-4 shadow-sm hover:border-white/20 transition-all">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-semibold text-[#AFAFAF] tracking-wider uppercase">{label}</span>
        <span className="material-symbols-outlined text-[#5F5F5F] text-[18px]">{icon}</span>
      </div>
      <div className="flex items-baseline gap-2 mt-1">
        <span className="text-4xl text-[#F2F2F2] font-semibold tracking-tight">{value}</span>
        {unit && <span className="text-base text-[#AFAFAF] font-medium">{unit}</span>}
      </div>
      {trend && (
        <div className="flex items-center gap-1.5 pt-3 border-t border-[#1E1E1E]">
          <span className="inline-flex items-center text-[#F2F2F2] text-xs font-semibold">
            {showArrow && <span className="material-symbols-outlined text-[14px] mr-0.5 text-white">arrow_downward</span>}
            {trend.value}%
          </span>
          <span className="text-xs text-[#5F5F5F] truncate">{trend.label}</span>
        </div>
      )}
      {footer && (
        <div className="flex items-center justify-between pt-3 border-t border-[#1E1E1E]">
          <span className="text-xs text-[#AFAFAF]">{footer.left}</span>
          {footer.right && (
            <span className="px-2 py-0.5 rounded bg-[#1E1E1E] border border-white/5 text-[#F2F2F2] text-[11px] font-medium">
              {footer.right}
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default KPICard;