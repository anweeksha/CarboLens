import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Bike,
  Bolt,
  Check,
  CheckCircle2,
  Clock3,
  Flame,
  Leaf,
  Recycle,
  RotateCw,
  TrainFront,
  Trophy,
  Utensils,
  UsersRound,
  Verified,
  TrendingDown,
} from 'lucide-react';

const challenges = [
  { id: 1, category: 'Commute', title: 'No-Car Week', eyebrow: 'COMMUTE', days: '3 days left', description: 'Replace private vehicle trips with campus shuttles, bike shares, or walking between campus quarters.', participants: 248, saved: 386, progress: 72, icon: TrainFront, joined: true },
  { id: 2, category: 'Energy', title: 'Low Energy Week', eyebrow: 'ELECTRICITY & HVAC', days: '5 days left', description: 'Switch dorm workstations to eco-profiles and reduce active HVAC runtime by 2 hours daily.', participants: 412, saved: 241, progress: 58, icon: Bolt, joined: false },
  { id: 3, category: 'Dietary', title: 'Plant-Based Week', eyebrow: 'FOOD & DINING', days: '6 days left', description: 'Commit to plant-forward dining hall selections for at least 4 lunches this week with digital scanner logs.', participants: 389, saved: 198, progress: 64, icon: Utensils, joined: false },
  { id: 4, category: 'Waste', title: 'Zero Waste Challenge', eyebrow: 'WASTE & PACKAGING', days: '4 days left', description: 'Eliminate single-use packaging with reusable campus dining containers and verified hall composting bins.', participants: 235, saved: 174, progress: 49, icon: Recycle, joined: false },
];

const ChallengeMetric = ({ label, value, detail, icon: Icon }) => (
  <article className="flex min-h-[148px] flex-col justify-between rounded-2xl border border-white/[0.07] bg-[#141414] p-5">
    <div className="flex items-center justify-between"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">{label}</span><Icon size={20} className="text-[#5F5F5F]" /></div>
    <div className="mt-3 flex items-baseline gap-2"><span className="text-[40px] font-semibold leading-none tracking-tight text-[#F2F2F2]">{value}</span><span className="text-[13px] text-[#AFAFAF]">{detail}</span></div>
    {label === 'IN CURRENT ROTATION' ? <div className="mt-2 flex items-center gap-2 text-[12px] text-[#AFAFAF]"><span className="h-1.5 w-1.5 rounded-full bg-white" />All verified campus-wide</div> : null}
    {label === 'VERIFIED CAMPUS PEERS' ? <div className="mt-2 text-[12px] text-[#AFAFAF]">Across 8 university departments</div> : null}
    {label === 'AGGREGATE THIS CYCLE' ? <div className="mt-2 flex items-center gap-2 text-[12px]"><span className="font-medium text-white">↑ 22%</span><span className="text-[#AFAFAF]">vs previous term pace</span></div> : null}
  </article>
);

const ChallengesPage = () => {
  const [filter, setFilter] = useState('All');
  const [items, setItems] = useState(challenges);
  const [joinedFeatured, setJoinedFeatured] = useState(false);
  const filters = ['All', 'Commute', 'Energy', 'Dietary', 'Waste'];
  const filtered = filter === 'All' ? items : items.filter((item) => item.category === filter);

  const toggleJoin = (id) => setItems((current) => current.map((item) => item.id === id ? { ...item, joined: !item.joined } : item));

  return (
    <div className="flex flex-col gap-8">
      <section className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div className="max-w-2xl"><div className="flex flex-wrap items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#AFAFAF]"><span>Campus Challenges</span><span className="h-1 w-1 rounded-full bg-[#5F5F5F]" /><span>Collective Action V2.4</span><span className="h-1 w-1 rounded-full bg-[#5F5F5F]" /><span className="text-[#5F5F5F]">Term 01</span></div><h1 className="mt-2 text-[36px] font-semibold leading-tight tracking-tight text-[#F2F2F2]">Make an impact together.</h1><p className="mt-1 text-[15px] leading-normal text-[#AFAFAF]">Join challenges, reduce CO₂e, and see your contribution to the campus collective trajectory in real time.</p></div>
        <div className="flex items-center gap-3 self-start lg:self-end"><button type="button" className="inline-flex items-center gap-2 rounded-xl border border-white/[0.07] bg-[#141414] px-4 py-2 text-[13px] font-medium text-[#F2F2F2] transition-colors hover:bg-[#1E1E1E]"><Clock3 size={16} className="text-[#AFAFAF]" />Explore Past Archive</button><button type="button" className="inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2 text-[13px] font-medium text-[#0B0B0B] shadow-sm transition-colors hover:bg-[#E5E5E5]"><Trophy size={16} />Propose Challenge</button></div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3"><ChallengeMetric label="IN CURRENT ROTATION" value="6" detail="Active challenges" icon={RotateCw} /><ChallengeMetric label="VERIFIED CAMPUS PEERS" value="1,284" detail="Participants" icon={UsersRound} /><ChallengeMetric label="AGGREGATE THIS CYCLE" value={<>{'2.8'} <span className="text-[24px] font-medium text-[#AFAFAF]">t</span></>} detail="CO₂e eliminated" icon={TrendingDown} /></section>

      <section className="relative overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414] p-6 md:p-8">
        <div className="pointer-events-none absolute right-6 top-1/2 hidden -translate-y-1/2 opacity-15 xl:block"><svg width="360" height="260" viewBox="0 0 420 280" fill="none" className="text-white" aria-hidden="true"><circle cx="210" cy="140" r="130" stroke="currentColor" strokeDasharray="4 6" /><circle cx="210" cy="140" r="90" stroke="currentColor" /><circle cx="210" cy="140" r="50" stroke="currentColor" strokeDasharray="2 4" /><path d="M70 140C70 62.68 132.68 0 210 0" stroke="currentColor" /><circle cx="210" cy="50" r="4" fill="currentColor" /><circle cx="300" cy="140" r="5" fill="currentColor" /></svg></div>
        <div className="relative z-10 flex max-w-3xl flex-col gap-6">
          <div className="flex flex-wrap items-center gap-2.5"><span className="inline-flex items-center gap-2 rounded-full border border-white/[0.07] bg-[#1E1E1E] px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-[#F2F2F2]"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-white" />Featured Collective Initiative</span><span className="rounded-full border border-white/[0.05] bg-[#1E1E1E] px-3 py-1 text-[12px] text-[#AFAFAF]">3 days remaining</span></div>
          <div><h2 className="text-[40px] font-semibold leading-none tracking-tight text-[#F2F2F2] md:text-[56px]">NO-CAR WEEK</h2><p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-[#AFAFAF]">7 days. One campus. Less carbon. Walk, cycle, or take the electric campus shuttle for 7 consecutive days to eliminate individual commute emissions across University North & South Quads.</p></div>
          <div className="flex flex-col gap-3"><div className="grid grid-cols-1 gap-4 rounded-xl border border-white/[0.06] bg-[#1E1E1E] p-4 sm:grid-cols-3">{[['ENROLLED', '248', 'students'], ['CO₂ REDUCED', '386', 'kg'], ['COLLECTIVE GOAL', '500', 'kg target']].map(([label, value, unit]) => <div key={label}><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#AFAFAF]">{label}</span><span className="mt-1 block text-[20px] font-semibold text-[#F2F2F2]">{value} <span className="text-[12px] font-normal text-[#AFAFAF]">{unit}</span></span></div>)}</div><div><div className="mb-1.5 flex items-center justify-between text-[12px]"><span className="text-[#AFAFAF]">Progress toward collective threshold</span><span className="font-medium text-[#F2F2F2]">72% Completed</span></div><div className="h-2 overflow-hidden rounded-full border border-white/[0.05] bg-[#0B0B0B]"><div className="h-full rounded-full bg-white transition-all duration-700" style={{ width: '72%' }} /></div></div></div>
          <div className="flex flex-wrap items-center gap-3"><button type="button" onClick={() => setJoinedFeatured((joined) => !joined)} className="rounded-xl bg-white px-5 py-2.5 text-[13px] font-medium text-[#0B0B0B] shadow-sm transition-colors hover:bg-[#E5E5E5]">{joinedFeatured ? 'Joined Challenge' : 'Join Challenge'}</button><Link to="/leaderboard" className="inline-flex items-center gap-2 rounded-xl border border-white/[0.07] bg-[#1E1E1E] px-4 py-2.5 text-[13px] font-medium text-[#F2F2F2] transition-colors hover:bg-[#282828]">View Cohort Standings<ArrowRight size={16} /></Link><span className="ml-auto hidden text-[12px] text-[#AFAFAF] sm:inline">Verification: Campus Geo-beacon & Transit Card</span></div>
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center"><div className="flex items-baseline gap-2.5"><h2 className="text-[24px] font-semibold tracking-tight text-[#F2F2F2]">Active challenges</h2><span className="text-[12px] text-[#AFAFAF]">Cohort Sprint 04</span></div><div className="flex items-center gap-2 overflow-x-auto pb-1">{filters.map((item) => <button key={item} type="button" onClick={() => setFilter(item)} className={`shrink-0 rounded-full px-3.5 py-1.5 text-[12px] transition-colors ${filter === item ? 'bg-white font-medium text-[#0B0B0B]' : 'border border-white/[0.07] bg-[#141414] text-[#AFAFAF] hover:bg-[#1E1E1E] hover:text-[#F2F2F2]'}`}>{item}{item === 'All' ? ' (6)' : ''}</button>)}</div></div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">{filtered.map((item) => { const Icon = item.icon; return <article key={item.id} className="flex flex-col justify-between gap-4 rounded-2xl border border-white/[0.07] bg-[#141414] p-5 transition-colors hover:border-white/[0.14]"><div className="flex flex-col gap-2.5"><div className="flex items-start justify-between gap-3"><div className="flex items-center gap-3"><span className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/[0.06] bg-[#1E1E1E]"><Icon size={20} /></span><div><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#AFAFAF]">{item.eyebrow}</span><h3 className="text-[18px] font-semibold text-[#F2F2F2]">{item.title}</h3></div></div><span className="whitespace-nowrap rounded-full border border-white/[0.05] bg-[#1E1E1E] px-2.5 py-0.5 text-[11px] text-[#AFAFAF]">{item.days}</span></div><p className="text-[13px] leading-normal text-[#AFAFAF]">{item.description}</p></div><div className="flex flex-col gap-2.5 border-t border-white/[0.06] pt-3"><div className="flex items-center justify-between gap-2 text-[12px]"><span className="inline-flex items-center gap-1.5 text-[#AFAFAF]"><UsersRound size={15} className="text-[#5F5F5F]" />{item.participants} students</span><span className="font-medium text-[#F2F2F2]">{item.saved} kg CO₂e saved</span></div><div className="h-1.5 overflow-hidden rounded-full bg-[#0B0B0B]"><div className="h-full rounded-full bg-white" style={{ width: `${item.progress}%` }} /></div><div className="flex items-center justify-between gap-2 pt-1"><span className="text-[11px] text-[#5F5F5F]">{item.progress}% of quota achieved</span><button type="button" onClick={() => toggleJoin(item.id)} className={`inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-[12px] font-medium transition-colors ${item.joined ? 'border-white/[0.07] bg-[#1E1E1E] text-[#F2F2F2]' : 'border-transparent bg-white text-[#0B0B0B] hover:bg-[#E5E5E5]'}`}>{item.joined && <span className="h-1.5 w-1.5 rounded-full bg-white" />}{item.joined ? 'Active (Joined)' : 'Join Challenge'}</button></div></div></article>; })}</div>
      </section>

      <section className="flex flex-col gap-4">
        <div><h2 className="text-[24px] font-semibold tracking-tight text-[#F2F2F2]">Your challenge progress</h2><p className="text-[14px] text-[#AFAFAF]">Track your personal contributions toward campus milestones and departmental standings.</p></div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">{[
          { label: 'CURRENT STREAK', value: '14 Days', detail: 'Personal best record', icon: Flame },
          { label: 'COMPLETED', value: '8', detail: '3 in current term', icon: Verified },
          { label: 'PERSONAL SAVINGS', value: '48.2 kg', detail: 'Top 8% contributor', icon: TrendingDown },
          { label: 'CURRENT RANK', value: '#12', detail: 'In Dept. of CSE', icon: Trophy },
        ].map(({ label, value, detail, icon: Icon }) => <article key={label} className="flex flex-col justify-between gap-3 rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div className="flex items-center justify-between"><span className="text-[10px] font-semibold uppercase tracking-wider text-[#AFAFAF]">{label}</span><Icon size={18} className="text-[#F2F2F2]" /></div><div><span className="block text-[28px] font-semibold tracking-tight text-[#F2F2F2]">{value}</span><span className="mt-0.5 text-[12px] text-[#AFAFAF]">{detail}</span></div></article>)}</div>
        <div className="flex flex-col gap-3 rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div className="flex items-center justify-between border-b border-white/[0.06] pb-3"><div className="flex items-center gap-2"><CheckCircle2 size={18} className="text-[#5F5F5F]" /><span className="text-[13px] font-medium text-[#F2F2F2]">Recent Completion Badges</span></div><span className="text-[12px] text-[#AFAFAF]">Verified telemetry logs</span></div><div className="grid grid-cols-1 gap-3 pt-1 md:grid-cols-2">{[{ title: 'Campus Transit Sprint', date: 'Completed Sep 20', saving: '+18.4 kg saved', icon: Bike }, { title: 'Dorm Night Eco-Mode', date: 'Completed Sep 12', saving: '+12.0 kg saved', icon: Check }].map(({ title, date, saving: amount, icon: Icon }) => <article key={title} className="flex items-center justify-between gap-3 rounded-xl border border-white/[0.06] bg-[#1E1E1E] p-3"><div className="flex items-center gap-3"><span className="flex h-8 w-8 items-center justify-center rounded-lg border border-white/[0.07] bg-[#141414]"><Icon size={16} /></span><div><span className="block text-[13px] font-medium leading-tight text-[#F2F2F2]">{title}</span><span className="text-[11px] text-[#AFAFAF]">{date}</span></div></div><span className="whitespace-nowrap text-[13px] font-medium text-[#F2F2F2]">{amount}</span></article>)}</div></div>
      </section>
    </div>
  );
};

export default ChallengesPage;