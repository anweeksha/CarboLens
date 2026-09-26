const ChallengesSection = () => {
  const leaderboard = [
    { rank: '01', name: 'Hostel B', sub: 'Residential Quad', value: '18.4 kg/user', color: 'text-[#F2F2F2]' },
    { rank: '02', name: 'Dept. of CSE (You)', sub: 'Engineering Division', value: '16.9 kg/user', color: 'text-[#F2F2F2]' },
    { rank: '03', name: 'Hostel A', sub: 'Residential Quad', value: '14.7 kg/user', color: 'text-[#AFAFAF]' },
    { rank: '04', name: 'Dept. of ECE', sub: 'Engineering Division', value: '12.8 kg/user', color: 'text-[#AFAFAF]' },
  ];

  return (
    <section className="grid grid-cols-1 lg:grid-cols-12 gap-6 pb-8">
      {/* Left Card: ACTIVE CHALLENGE (5 cols) */}
      <div className="lg:col-span-5 p-6 lg:p-8 rounded-[24px] bg-[#141414] flex flex-col justify-between relative overflow-hidden shadow-lg group">
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] tracking-wider uppercase">ACTIVE CHALLENGE</span>
            <span className="material-symbols-outlined text-[#F2F2F2] text-[20px]">emoji_events</span>
          </div>
          <div className="flex flex-col gap-2">
            <h3 className="text-2xl text-[#F2F2F2] font-semibold tracking-tight">NO-CAR WEEK</h3>
            <p className="text-sm text-[#AFAFAF]">Walk, cycle, or board the campus shuttle for 7 consecutive days.</p>
          </div>
          <div className="grid grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-xl bg-[#0e0e0e] flex flex-col">
              <span className="text-[11px] text-[#AFAFAF]">Participants</span>
              <span className="text-xl text-[#F2F2F2] font-bold">248</span>
            </div>
            <div className="p-4 rounded-xl bg-[#0e0e0e] flex flex-col">
              <span className="text-[11px] text-[#AFAFAF]">Carbon Saved</span>
              <span className="text-xl text-[#F2F2F2] font-bold">386 kg</span>
            </div>
          </div>
          {/* Challenge Progress */}
          <div className="flex flex-col gap-1.5 pt-2">
            <div className="flex items-center justify-between text-[11px]">
              <span className="text-[#AFAFAF]">Progress</span>
              <span className="text-[#F2F2F2] font-semibold">72% Completed</span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-[#2a2a2a] overflow-hidden">
              <div className="h-full bg-white" style={{ width: '72%' }}></div>
            </div>
          </div>
        </div>
        <div className="pt-6">
          <button className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-[#1c1b1b] hover:bg-[#2a2a2a] text-[#F2F2F2] text-[13px] transition-all active:scale-[0.98]" type="button">
            <span>View challenge details</span>
            <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
          </button>
        </div>
      </div>
      {/* Right Card: CAMPUS GREEN LEAGUE (LEADERBOARD - 7 cols) */}
      <div className="lg:col-span-7 p-6 lg:p-8 rounded-[24px] bg-[#141414] flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between pb-4">
          <div className="flex flex-col">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] tracking-wider uppercase">CAMPUS GREEN LEAGUE</span>
            <h3 className="text-xl text-[#F2F2F2] font-medium tracking-tight">Cohort Standings</h3>
          </div>
          <span className="text-[11px] text-[#AFAFAF]">Cycle 03</span>
        </div>
        {/* Minimalist Grayscale Table List */}
        <div className="flex flex-col divide-y divide-white/5">
          {leaderboard.map((item, index) => (
            <div key={index} className="flex items-center justify-between py-3">
              <div className="flex items-center gap-4">
                <span className={`text-xl ${item.color} font-light w-8`}>{item.rank}</span>
                <div className="flex flex-col">
                  <span className={`text-[13px] ${index < 2 ? 'text-[#F2F2F2] font-semibold' : 'text-[#AFAFAF] font-medium'}`}>{item.name}</span>
                  <span className="text-[11px] text-[#AFAFAF]">{item.sub}</span>
                </div>
              </div>
              <div className="flex items-center gap-2 px-3 py-1 rounded bg-[#0e0e0e] text-[#F2F2F2] text-[13px]">
                <span className="material-symbols-outlined text-[14px]">arrow_downward</span>
                <span>{item.value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ChallengesSection;