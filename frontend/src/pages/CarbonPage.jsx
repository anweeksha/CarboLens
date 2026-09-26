import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowDown,
  ArrowRight,
  Bolt,
  BusFront,
  CheckCircle2,
  ChevronRight,
  Download,
  Gauge,
  Leaf,
  Recycle,
  TrendingDown,
  Utensils,
} from 'lucide-react';

const categories = [
  { label: 'TRAVEL', sub: 'Commutes & transit', value: '72.4', share: '39%', icon: BusFront },
  { label: 'ELECTRICITY', sub: 'Labs & dorm supply', value: '51.2', share: '28%', icon: Bolt },
  { label: 'FOOD', sub: 'Dining & groceries', value: '48.0', share: '26%', icon: Utensils },
  { label: 'WASTE', sub: 'Packaging & landfill', value: '13.0', share: '7%', icon: Recycle },
];

const attribution = [
  { index: '01', title: 'Transportation', tag: 'Primary', detail: 'Commute between North Campus & Labs (approx. 14 trips/wk)', value: '72.4 kg CO₂e', share: '39% of your total footprint' },
  { index: '02', title: 'Electricity', tag: 'High compute', detail: 'Studio workstation compute & dorm AC consumption', value: '51.2 kg CO₂e', share: '28% of your total footprint' },
  { index: '03', title: 'Food', tag: 'Dietary', detail: 'Campus dining, red meat frequency & packaging impact', value: '48.0 kg CO₂e', share: '26% of your total footprint' },
];

const departments = [
  { name: 'CSE (Your Dept.)', value: '32.4 t', width: '82%' },
  { name: 'ECE', value: '27.1 t', width: '68%' },
  { name: 'ME', value: '23.6 t', width: '59%' },
  { name: 'Hostel B', value: '19.8 t', width: '48%' },
];

const standings = [
  { rank: '01', name: 'Hostel B', detail: 'Residential Quad', value: '18.4 kg/user' },
  { rank: '02', name: 'Dept. of CSE (You)', detail: 'Engineering Division', value: '16.9 kg/user' },
  { rank: '03', name: 'Hostel A', detail: 'Residential Quad', value: '14.7 kg/user' },
  { rank: '04', name: 'Dept. of ECE', detail: 'Engineering Division', value: '12.8 kg/user' },
];

const CarbonPage = () => {
  const [period, setPeriod] = useState('This Month');
  const [remainingTrips, setRemainingTrips] = useState(4);
  const saved = Math.max(0, (12 - remainingTrips) * 3.925);
  const projected = 184.6 - saved;

  const exportReport = () => {
    const report = [
      ['Personal Carbon Profile', period],
      ['Monthly footprint', '184.6 kg CO₂e'],
      ['Target Profile', '160.0 kg'],
      ['Campus Avg', '212.4 kg'],
      ...categories.map((item) => [item.label, `${item.value} kg CO₂e`, item.share]),
    ].map((row) => row.join(',')).join('\n');
    const url = URL.createObjectURL(new Blob([report], { type: 'text/csv' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'carbonlens-personal-carbon-report.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col gap-10">
      <header className="flex flex-col justify-between gap-6 pb-2 lg:flex-row lg:items-end">
        <div className="flex max-w-2xl flex-col gap-2">
          <div className="flex items-center gap-2"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-white" /><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#AFAFAF]">Personal Carbon Profile</span></div>
          <h1 className="text-[48px] font-semibold leading-[1.08] tracking-tight text-white lg:text-[56px]">Your impact, in perspective.</h1>
          <p className="pt-1 text-[16px] leading-6 text-[#C7C6C6]">Track what matters. Understand what drives your footprint. Make changes that actually count.</p>
        </div>
        <div className="flex flex-wrap items-center gap-2 self-start lg:self-end">
          <div className="inline-flex rounded-full bg-[#1C1B1B] p-1" role="group" aria-label="Time range">
            {['This Month', 'Semester', 'Year'].map((item) => <button key={item} type="button" onClick={() => setPeriod(item)} className={`rounded-full px-4 py-1.5 text-[13px] transition-colors ${period === item ? 'bg-[#2A2A2A] text-white' : 'text-[#C7C6C6] hover:text-white'}`}>{item}</button>)}
          </div>
          <button type="button" onClick={exportReport} className="inline-flex items-center gap-2 rounded-lg bg-[#201F1F] px-4 py-2 text-[13px] font-medium text-white transition-colors hover:bg-[#2A2A2A]"><Download size={16} />Export Report</button>
        </div>
      </header>

      <section className="relative overflow-hidden rounded-[24px] border border-white/[0.06] bg-[#141414] p-6 shadow-2xl lg:p-10">
        <div className="pointer-events-none absolute inset-y-0 right-0 hidden w-[47%] items-center justify-center opacity-40 md:flex">
          <svg viewBox="0 0 600 600" className="h-[560px] max-w-full" fill="none" aria-hidden="true"><circle cx="300" cy="300" r="280" stroke="white" strokeOpacity=".2" strokeDasharray="4 8" /><circle cx="300" cy="300" r="220" stroke="white" strokeOpacity=".3" strokeWidth="1.5" /><circle cx="300" cy="300" r="160" stroke="white" strokeOpacity=".4" strokeDasharray="2 6" /><circle cx="300" cy="300" r="100" stroke="white" strokeOpacity=".25" /><circle cx="300" cy="300" r="40" stroke="white" strokeOpacity=".6" strokeDasharray="6 6" /><path d="M300 20v560M20 300h560" stroke="white" strokeOpacity=".12" strokeDasharray="3 9" /></svg>
        </div>
        <div className="relative grid items-center gap-8 lg:grid-cols-12">
          <div className="flex flex-col gap-4 lg:col-span-7">
            <div className="flex items-center gap-2"><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Monthly Footprint</span><span className="h-1 w-1 rounded-full bg-[#C7C6C6]" /><span className="text-[11px] text-[#C7C6C6]">March 2025 Cycle</span></div>
            <div className="flex flex-wrap items-baseline gap-x-4"><span className="text-[72px] font-semibold leading-none tracking-tight text-white sm:text-[80px]">184.6</span><span className="text-[24px] font-light text-[#C4C7C8]">kg CO₂e</span></div>
            <div className="flex flex-wrap items-center gap-3 pt-1"><span className="inline-flex items-center gap-1.5 rounded-full bg-[#2A2A2A] px-3 py-1 text-[13px] text-white"><ArrowDown size={16} />12.4% from last month</span><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Lower than your previous month</span></div>
          </div>
          <div className="flex flex-col justify-end gap-2 sm:flex-row lg:col-span-5 lg:flex-col">
              <div className="flex items-center justify-between rounded-xl bg-[#1C1B1B] p-4 transition-colors hover:bg-[#201F1F]"><div><span className="block text-[11px] uppercase tracking-wider text-[#C4C7C8]">Target Profile</span><span className="text-[20px] font-medium text-white">160.0 kg</span></div><div className="text-right"><span className="text-[11px] text-[#C7C6C6]">24.6 kg surplus</span><div className="mt-1 h-1.5 w-24 overflow-hidden rounded-full bg-[#353534]"><div className="h-full bg-white" style={{ width: '86%' }} /></div></div></div>
            <div className="flex items-center justify-between rounded-xl bg-[#1C1B1B] p-4 transition-colors hover:bg-[#201F1F]"><div><span className="block text-[11px] uppercase tracking-wider text-[#C4C7C8]">Campus Avg</span><span className="text-[20px] font-medium text-white">212.4 kg</span></div><span className="inline-flex items-center gap-1 text-[11px] text-white"><CheckCircle2 size={14} />13.1% below avg</span></div>
            <div className="flex items-center justify-between rounded-xl bg-[#1C1B1B] p-4 transition-colors hover:bg-[#201F1F]"><div><span className="block text-[11px] uppercase tracking-wider text-[#C4C7C8]">Global Net Zero Pace</span><span className="text-[20px] font-medium text-white">-3.2%</span></div><span className="text-[11px] text-[#C7C6C6]">Annualized trajectory</span></div>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {categories.map(({ label, sub, value, share, icon: Icon }) => <article key={label} className="group flex flex-col justify-between rounded-[24px] bg-[#141414] p-6 transition-all duration-300 hover:-translate-y-1 hover:bg-[#1A1A1A]"><div className="flex items-center justify-between pb-7"><div><span className="block text-[11px] uppercase tracking-wider text-[#C4C7C8]">{label}</span><span className="text-[11px] text-[#C7C6C6]">{sub}</span></div><span className="flex h-10 w-10 items-center justify-center rounded-full bg-[#2A2A2A] text-white transition-transform group-hover:scale-110"><Icon size={20} /></span></div><div><div className="flex items-baseline justify-between"><span className="text-[28px] font-semibold tracking-tight text-white">{value}</span><span className="text-[20px] font-light text-[#C4C7C8]">{share}</span></div><span className="block pb-3 text-[11px] text-[#C4C7C8]">kg CO₂e recorded</span><div className="h-[2px] overflow-hidden rounded-full bg-[#353534]"><div className="h-full bg-white transition-all duration-700" style={{ width: share }} /></div></div></article>)}
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="relative flex flex-col justify-between rounded-[24px] bg-[#141414] p-6 shadow-lg lg:col-span-8 lg:p-8">
          <div className="flex flex-col justify-between gap-2 pb-5 sm:flex-row sm:items-center"><div><h2 className="text-[24px] font-medium tracking-tight text-white">Carbon trajectory</h2><p className="text-[14px] text-[#C7C6C6]">Your estimated footprint over the last 6 months</p></div><span className="self-start rounded-full bg-[#2A2A2A] px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-white sm:self-auto">6 Months</span></div>
          <div className="relative h-64 w-full">
            <div className="pointer-events-none absolute inset-0 flex flex-col justify-between opacity-30"><span className="border-t border-dashed border-white/30" /><span className="border-t border-dashed border-white/30" /><span className="border-t border-dashed border-white/30" /><span className="border-t border-dashed border-white/30" /></div>
            <svg viewBox="0 0 700 220" preserveAspectRatio="none" className="relative h-full w-full overflow-visible" role="img" aria-label="Carbon trajectory, October through March"><defs><linearGradient id="carbon-area" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="white" stopOpacity=".18" /><stop offset="100%" stopColor="white" stopOpacity="0" /></linearGradient></defs><path d="M0 90 Q140 85 280 80 T560 75 T700 70" fill="none" stroke="white" strokeOpacity=".2" strokeDasharray="4 6" strokeWidth="1.5" /><path d="M0 160 C140 140 180 110 280 125 C380 140 440 75 560 95 C620 105 660 135 700 140 L700 220 L0 220Z" fill="url(#carbon-area)" /><path d="M0 160 C140 140 180 110 280 125 C380 140 440 75 560 95 C620 105 660 135 700 140" fill="none" stroke="white" strokeLinecap="round" strokeWidth="2.5" /><circle cx="560" cy="95" r="4.5" fill="white" stroke="#141414" strokeWidth="2" /><circle cx="700" cy="140" r="5" fill="white" stroke="#141414" strokeWidth="2" /></svg>
            <div className="absolute left-[72%] top-8 -translate-x-1/2 rounded-xl border border-white/5 bg-[#353534]/90 p-3 shadow-2xl backdrop-blur-xl"><span className="flex items-center gap-2 text-[11px] text-[#C7C6C6]"><span className="h-1.5 w-1.5 rounded-full bg-white" />February Peak</span><span className="text-[20px] font-semibold text-white">198.2 kg</span></div>
          </div>
          <div className="flex justify-between pt-4 text-[11px] text-[#C4C7C8]"><span>Oct</span><span>Nov</span><span>Dec</span><span>Jan</span><span className="text-white">Feb</span><span className="font-bold text-white">Mar (Current)</span></div>
        </div>
        <aside className="relative flex flex-col justify-between overflow-hidden rounded-[24px] bg-[#1A1A1A] p-6 shadow-xl lg:col-span-4 lg:p-8">
          <div className="flex flex-col gap-4"><div className="flex items-center justify-between"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Highest Impact Opportunity</span><Bolt size={20} /></div><h3 className="pt-1 text-[24px] font-semibold leading-tight text-white">Switch 10 car trips to public transport.</h3><p className="text-[14px] leading-5 text-[#C7C6C6]">Subway & inter-campus transit lines eliminate up to 82% of transit combustion per passenger mile.</p><div className="mt-2 flex flex-col gap-1 rounded-xl bg-[#1C1B1B] p-4"><span className="text-[11px] uppercase tracking-wider text-[#C4C7C8]">Potential saving</span><div className="flex items-baseline gap-2"><span className="text-[28px] font-semibold text-white">31.4</span><span className="text-[13px] text-[#C7C6C6]">kg CO₂e / month</span></div></div></div>
          <Link to="/simulator" className="mt-6 flex w-full items-center justify-between rounded-xl bg-white px-4 py-2.5 text-[13px] font-semibold text-[#0B0B0B] transition-colors hover:bg-[#C7C6C6]">Explore scenario<ArrowRight size={18} /></Link>
        </aside>
      </section>

      <section className="flex flex-col gap-6">
        <div className="max-w-2xl"><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Activity Attribution</span><h2 className="mt-2 text-[32px] font-semibold tracking-tight text-white">What's driving your footprint?</h2><p className="mt-2 text-[14px] text-[#C7C6C6]">Granular sensor telemetry and logged receipts isolate the exact behavioral clusters generating campus carbon load.</p></div>
        <div className="flex flex-col gap-3">{attribution.map((item) => <article key={item.index} className="group flex flex-col justify-between gap-4 rounded-[24px] bg-[#141414] p-5 transition-colors hover:bg-[#1A1A1A] md:flex-row md:items-center md:p-6"><div className="flex items-start gap-5 md:items-center"><span className="text-[40px] font-light leading-none text-white/20 transition-colors group-hover:text-white/40">{item.index}</span><div><div className="flex flex-wrap items-center gap-2"><h3 className="text-[20px] font-medium text-white">{item.title}</h3><span className="rounded bg-[#2A2A2A] px-2 py-0.5 text-[11px] text-white">{item.tag}</span></div><p className="mt-1 text-[14px] text-[#C7C6C6]">{item.detail}</p></div></div><div className="flex items-center justify-between gap-4 md:justify-end"><div className="md:text-right"><span className="block text-[18px] font-semibold text-white">{item.value}</span><span className="text-[11px] text-[#C4C7C8]">{item.share}</span></div><ChevronRight size={20} className="text-[#C7C6C6] transition-transform group-hover:translate-x-1 group-hover:text-white" /></div></article>)}</div>
      </section>

      <section className="flex flex-col gap-6 rounded-[24px] bg-[#141414] p-6 shadow-xl lg:p-8">
        <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end"><div><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Dynamic Simulation</span><h2 className="mt-2 text-[30px] font-semibold tracking-tight text-white">What if you changed one thing?</h2><p className="mt-1 text-[14px] text-[#C7C6C6]">Model immediate behavioral interventions and inspect your projected trajectory.</p></div><div className="flex flex-wrap items-center gap-4 rounded-2xl bg-[#1C1B1B] p-4"><div><span className="block text-[10px] uppercase text-[#C4C7C8]">Current</span><span className="text-[18px] font-medium text-[#C7C6C6]">184.6 kg</span></div><ArrowRight size={18} className="text-[#C4C7C8]" /><div><span className="block text-[10px] uppercase text-[#C4C7C8]">Scenario</span><span className="text-[18px] font-bold text-white">{projected.toFixed(1)} kg</span></div><div className="hidden h-8 w-px bg-[#2A2A2A] sm:block" /><div><span className="block text-[10px] uppercase text-[#C4C7C8]">Saved</span><span className="rounded-full bg-[#2A2A2A] px-2 py-0.5 text-[13px] font-semibold text-white">{saved.toFixed(1)} kg CO₂e</span></div></div></div>
        <div className="flex flex-col gap-3 rounded-2xl bg-[#1C1B1B] p-5"><div className="flex flex-wrap items-center justify-between gap-3"><label htmlFor="carbon-trip-slider" className="flex items-center gap-2 text-[13px] font-medium text-white"><BusFront size={16} />Car trips per month (replaced with campus shuttle or bike)</label><span className="text-[18px] font-bold text-white">{remainingTrips === 0 ? '0 trips (Car-free)' : `${remainingTrips} trips remaining`}</span></div><input id="carbon-trip-slider" type="range" min="0" max="12" step="1" value={remainingTrips} onChange={(event) => setRemainingTrips(Number(event.target.value))} className="h-2 w-full cursor-pointer accent-white" /><div className="flex justify-between text-[11px] text-[#C7C6C6]"><span>0 (Full Shift: Max Save)</span><span>Current Baseline: 12 trips</span></div></div>
      </section>

      <section className="flex flex-col gap-6">
        <div className="max-w-3xl"><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Network Benchmark</span><h2 className="mt-2 text-[32px] font-semibold tracking-tight text-white">Your footprint is part of something bigger.</h2><p className="mt-2 text-[14px] text-[#C7C6C6]">Aggregated emissions and collective progress across Oxford University West Campus.</p></div>
        <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-[#1C1B1B] p-5"><div className="flex items-center gap-4"><span className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#2A2A2A]"><Gauge size={24} /></span><div><span className="block text-[11px] uppercase text-[#C4C7C8]">Campus Aggregate</span><span className="text-[23px] font-semibold text-white">142.6 t CO₂e this month</span></div></div><span className="inline-flex items-center gap-1 rounded-full bg-[#2A2A2A] px-4 py-1.5 text-[13px] text-white"><ArrowDown size={16} />↓ 8.4% vs previous month</span></div>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-12"><article className="flex flex-col gap-5 rounded-[24px] bg-[#141414] p-6 shadow-md lg:col-span-7"><div className="flex items-center justify-between"><h3 className="text-[20px] font-medium text-white">Department Emissions</h3><span className="text-[11px] text-[#C7C6C6]">Active cycle tally</span></div>{departments.map((item, index) => <div key={item.name} className="flex flex-col gap-1"><div className="flex items-center justify-between text-[13px]"><span className={index === 0 ? 'font-medium text-white' : 'text-[#C7C6C6]'}>{item.name}</span><span className="font-semibold text-white">{item.value}</span></div><div className="h-2 overflow-hidden rounded-full bg-[#2A2A2A]"><div className={`h-full ${index === 0 ? 'bg-white' : 'bg-[#AFAFAF]'}`} style={{ width: item.width }} /></div></div>)}</article>
          <article className="flex flex-col justify-between gap-4 rounded-[24px] bg-[#141414] p-6 shadow-md lg:col-span-5"><div className="flex items-center justify-between"><h3 className="text-[20px] font-medium text-white">Energy Grid Intensity</h3><span className="rounded bg-[#2A2A2A] px-2 py-1 text-[10px] font-semibold tracking-wider text-white">LIVE FEED</span></div><div className="relative flex items-center justify-center py-2"><svg viewBox="0 0 140 80" className="w-48" aria-hidden="true"><path d="M15 70 A55 55 0 0 1 125 70" fill="none" stroke="#2A2A2A" strokeLinecap="round" strokeWidth="8" /><path d="M15 70 A55 55 0 0 1 95 24" fill="none" stroke="white" strokeLinecap="round" strokeWidth="8" /></svg><div className="absolute bottom-2 flex flex-col items-center"><span className="text-[28px] font-bold text-white">142</span><span className="text-[11px] text-[#C7C6C6]">g CO₂/kWh</span></div></div><div className="flex items-center justify-between rounded-xl bg-[#1C1B1B] p-3 text-[13px] text-[#C7C6C6]"><span>Renewables Contribution:</span><span className="font-semibold text-white">68.4% Wind + Solar</span></div></article></div>
      </section>

      <section className="grid grid-cols-1 gap-4 pb-6 lg:grid-cols-12">
        <article className="flex flex-col justify-between gap-6 rounded-[24px] bg-[#141414] p-6 shadow-lg lg:col-span-5 lg:p-8"><div className="flex flex-col gap-4"><div className="flex items-center justify-between"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Active Challenge</span><Leaf size={20} /></div><div><h3 className="text-[30px] font-semibold tracking-tight text-white">NO-CAR WEEK</h3><p className="mt-1 text-[14px] text-[#C7C6C6]">Walk, cycle, or board the campus shuttle for 7 consecutive days.</p></div><div className="grid grid-cols-2 gap-2"><div className="rounded-xl bg-[#1C1B1B] p-3"><span className="block text-[11px] text-[#C4C7C8]">Participants</span><span className="text-[20px] font-bold text-white">248</span></div><div className="rounded-xl bg-[#1C1B1B] p-3"><span className="block text-[11px] text-[#C4C7C8]">Carbon Saved</span><span className="text-[20px] font-bold text-white">386 kg</span></div></div><div><div className="mb-1.5 flex justify-between text-[11px]"><span className="text-[#C7C6C6]">Progress</span><span className="font-semibold text-white">72% Completed</span></div><div className="h-1.5 overflow-hidden rounded-full bg-[#2A2A2A]"><div className="h-full bg-white" style={{ width: '72%' }} /></div></div></div><Link to="/challenges" className="flex items-center justify-center gap-2 rounded-xl bg-[#1C1B1B] py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#2A2A2A]">View challenge details<ArrowRight size={16} /></Link></article>
        <article className="flex flex-col rounded-[24px] bg-[#141414] p-6 shadow-lg lg:col-span-7 lg:p-8"><div className="flex items-center justify-between pb-4"><div><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Campus Green League</span><h3 className="text-[23px] font-medium tracking-tight text-white">Cohort Standings</h3></div><span className="text-[11px] text-[#C7C6C6]">Cycle 03</span></div><div className="divide-y divide-white/5">{standings.map((item) => <div key={item.rank} className="flex items-center justify-between gap-3 py-3"><div className="flex items-center gap-4"><span className="w-8 text-[20px] font-light text-white">{item.rank}</span><div><span className="block text-[13px] font-semibold text-white">{item.name}</span><span className="text-[11px] text-[#C4C7C8]">{item.detail}</span></div></div><span className="whitespace-nowrap rounded bg-[#1C1B1B] px-3 py-1 text-[12px] text-white">{item.value}</span></div>)}</div><Link to="/leaderboard" className="mt-3 inline-flex items-center justify-end gap-1 text-[12px] text-[#C7C6C6] hover:text-white">Full leaderboard<ChevronRight size={15} /></Link></article>
      </section>
    </div>
  );
};

export default CarbonPage;