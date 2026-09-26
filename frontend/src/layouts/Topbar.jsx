const Topbar = () => {
  return (
    <header className="metal-topbar fixed top-0 left-64 right-0 h-16 bg-[#0B0B0B]/90 backdrop-blur-xl border-b border-[#1E1E1E] z-40">
      <div className="h-16 w-full px-8 flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#141414] border border-[#1E1E1E] text-[#AFAFAF] hover:text-[#F2F2F2] hover:border-white/20 transition-all" type="button">
            <span className="material-symbols-outlined text-[18px]">search</span>
            <span className="text-xs font-medium">Quick Jump...</span>
            <kbd className="text-[10px] px-1.5 py-0.5 rounded bg-[#1E1E1E] text-[#AFAFAF] border border-white/5">⌘K</kbd>
          </button>
          <div className="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#141414] border border-[#1E1E1E]">
            <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
            <span className="text-xs text-[#AFAFAF]">Campus Grid: Low Carbon Intensity • 142g/kWh</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="px-2.5 py-1 rounded-full bg-[#141414] border border-[#1E1E1E] text-[10px] font-semibold tracking-wider uppercase text-[#AFAFAF]">
            STUDENT TIER
          </div>
          <button className="relative p-2 rounded-lg hover:bg-[#141414] border border-transparent hover:border-[#1E1E1E] text-[#AFAFAF] hover:text-[#F2F2F2] transition-colors" type="button">
            <span className="material-symbols-outlined text-[20px]">notifications</span>
            <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-white"></span>
          </button>
          <div className="w-8 h-8 rounded-full bg-[#F2F2F2] flex items-center justify-center">
            <span className="material-symbols-outlined text-[#0E0E0E] text-[18px]">person</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Topbar;