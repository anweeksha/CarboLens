import { useState } from 'react';
import { ArrowDown, ArrowRight, Trophy, UsersRound } from 'lucide-react';

const cohorts = [
  { rank: '01', name: 'Hostel B', detail: 'Residential Quad', value: '18.4 kg/user' },
  { rank: '02', name: 'Dept. of CSE (You)', detail: 'Engineering Division', value: '16.9 kg/user', current: true },
  { rank: '03', name: 'Hostel A', detail: 'Residential Quad', value: '14.7 kg/user' },
  { rank: '04', name: 'Dept. of ECE', detail: 'Engineering Division', value: '12.8 kg/user' },
];

const departments = [
  { rank: '01 CSE', peers: '820 peers • 39.5 kg/ea', value: '32.4 t', width: '82%' },
  { rank: '02 ECE', peers: '640 peers • 42.3 kg/ea', value: '27.1 t', width: '68%' },
  { rank: '03 ME', peers: '580 peers • 40.7 kg/ea', value: '23.6 t', width: '59%' },
  { rank: '04 Civil', peers: '410 peers • 48.3 kg/ea', value: '19.8 t', width: '49%' },
  { rank: '05 Hostel B', peers: '490 residents • 35.5 kg/ea', value: '17.4 t', width: '43%' },
];

const LeaderboardPage = () => {
  const [view, setView] = useState('cohort');

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col justify-between gap-5 md:flex-row md:items-end"><div><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Campus Green League</span><h1 className="mt-2 text-[36px] font-semibold tracking-tight text-white">Cohort Standings</h1><p className="mt-1 text-[14px] text-[#C7C6C6]">Verified campus carbon performance by cohort and university division.</p></div><span className="rounded-full bg-[#1C1B1B] px-3 py-1.5 text-[11px] text-[#C7C6C6]">Cycle 03</span></header>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2"><article className="flex items-center justify-between rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div><span className="block text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Current Rank</span><span className="mt-2 block text-[40px] font-semibold leading-none tracking-tight text-white">#12</span><span className="mt-1 block text-[12px] text-[#AFAFAF]">In Dept. of CSE</span></div><Trophy size={22} className="text-[#C7C6C6]" /></article><article className="flex items-center justify-between rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div><span className="block text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Verified Campus Peers</span><span className="mt-2 block text-[40px] font-semibold leading-none tracking-tight text-white">1,284</span><span className="mt-1 block text-[12px] text-[#AFAFAF]">Across 8 university departments</span></div><UsersRound size={22} className="text-[#C7C6C6]" /></article></section>

      <section className="flex flex-col gap-5 rounded-[24px] bg-[#141414] p-6 shadow-lg lg:p-8">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center"><div><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Cycle 03</span><h2 className="mt-1 text-[23px] font-medium tracking-tight text-white">{view === 'cohort' ? 'Cohort Standings' : 'Department comparison'}</h2></div><div className="inline-flex w-fit rounded-lg bg-[#1C1B1B] p-1" role="group" aria-label="Leaderboard view"><button type="button" onClick={() => setView('cohort')} className={`rounded-md px-3 py-1.5 text-[12px] transition-colors ${view === 'cohort' ? 'bg-[#353534] text-white' : 'text-[#C4C7C8] hover:text-white'}`}>Cohorts</button><button type="button" onClick={() => setView('department')} className={`rounded-md px-3 py-1.5 text-[12px] transition-colors ${view === 'department' ? 'bg-[#353534] text-white' : 'text-[#C4C7C8] hover:text-white'}`}>Departments</button></div></div>

        {view === 'cohort' ? <div className="divide-y divide-white/5">{cohorts.map((item) => <article key={item.rank} className={`flex items-center justify-between gap-4 py-4 ${item.current ? 'rounded-xl bg-white/[0.03] px-3' : ''}`}><div className="flex items-center gap-4"><span className={`w-8 text-[22px] font-light ${item.current ? 'text-white' : 'text-[#C7C6C6]'}`}>{item.rank}</span><div><span className={`block text-[14px] font-semibold ${item.current ? 'text-white' : 'text-[#E5E2E1]'}`}>{item.name}</span><span className="text-[12px] text-[#C4C7C8]">{item.detail}</span></div></div><span className="inline-flex items-center gap-1.5 whitespace-nowrap rounded bg-[#1C1B1B] px-3 py-1.5 text-[12px] text-white"><ArrowDown size={14} />{item.value}</span></article>)}</div> : <div className="flex flex-col gap-5">{departments.map((item) => <article key={item.rank} className="flex flex-col gap-2"><div className="flex items-center justify-between gap-3 text-[13px]"><span className="font-medium text-white">{item.rank} <span className="text-[11px] font-normal text-[#5F5F5F]">/ {item.peers}</span></span><span className="font-mono font-semibold text-white">{item.value}</span></div><div className="h-1.5 w-full overflow-hidden rounded-full bg-[#1E1E1E]"><div className="h-full rounded-full bg-[#B8B8B8]" style={{ width: item.width }} /></div></article>)}</div>}

        <div className="flex flex-col justify-between gap-2 border-t border-[#1E1E1E] pt-4 sm:flex-row sm:items-center"><span className="text-[11px] text-[#5F5F5F]">{view === 'cohort' ? 'Lower per-user footprint ranks higher' : 'Normalizing per capita by lab operating hours'}</span>{view === 'department' && <span className="inline-flex items-center gap-1 self-start text-[12px] text-[#F2F2F2]">View full 14 units<ArrowRight size={14} /></span>}</div>
      </section>
    </div>
  );
};

export default LeaderboardPage;