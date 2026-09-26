import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Bookmark,
  BusFront,
  Check,
  CheckCircle2,
  Leaf,
  Thermometer,
} from 'lucide-react';

const recommendations = [
  { icon: BusFront, saving: '↓ 42.6 kg CO₂e / mo', title: 'Switch to public transport', detail: 'Full transit substitution for all weekday campus access.', feasibility: 'High feasibility • Shuttle stops 8 min away' },
  { icon: Thermometer, saving: '↓ 18.2 kg CO₂e / mo', title: 'Reduce AC & heating usage', detail: 'Eco-thermostat schedule: 2 hours daily reduction + night setback.', feasibility: 'Instant activation • Smart plug sync' },
  { icon: Leaf, saving: '↓ 24.8 kg CO₂e / mo', title: 'Eat plant-based meals', detail: 'Swap 4 meat lunches weekly for campus dining hall plant bowls.', feasibility: 'Low friction • 12 certified campus vendors' },
];

const RecommendationsPage = () => {
  const [saved, setSaved] = useState(false);

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Highest Impact Opportunity</span>
        <h1 className="text-[36px] font-semibold tracking-tight text-white">Switch 10 car trips to public transport.</h1>
        <p className="max-w-3xl text-[15px] leading-6 text-[#C7C6C6]">Subway & inter-campus transit lines eliminate up to 82% of transit combustion per passenger mile.</p>
      </header>

      <section className="relative overflow-hidden rounded-2xl bg-[#1C1B1B] p-6 shadow-xl lg:p-8">
        <div className="grid items-center gap-6 lg:grid-cols-12">
          <div className="flex flex-col gap-4 lg:col-span-8"><span className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.12em] text-white"><span className="h-2 w-2 animate-pulse rounded-full bg-white" />Highest Sensitivity Lever</span><h2 className="text-[24px] font-medium tracking-tight text-white">Switch 10 car trips to public transport</h2><p className="max-w-2xl text-[16px] leading-6 text-[#C7C6C6]">Replacing 10 monthly combustion commutes with the University Electric Shuttle or Oxford City Line eliminates 31.4 kg CO₂e — achieving 72% of your semester net-zero milestone in one behavioral switch.</p><div className="flex flex-wrap gap-2 pt-1"><Link to="/simulator" className="rounded-lg bg-white px-4 py-2.5 text-[13px] font-medium text-[#0B0B0B] transition-colors hover:bg-[#E2E2E2]">Explore scenario</Link><button type="button" onClick={() => setSaved((value) => !value)} className="inline-flex items-center gap-2 rounded-lg bg-[#2A2A2A] px-4 py-2.5 text-[13px] text-white transition-colors hover:bg-[#353534]">{saved ? <Check size={16} /> : <Bookmark size={16} />}{saved ? 'Added to Personal Target' : 'Add to Personal Target'}</button></div></div>
          <div className="flex flex-col items-center justify-center rounded-xl bg-[#201F1F] p-6 text-center shadow-inner lg:col-span-4"><span className="text-[10px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Projected Net Benefit</span><span className="text-[40px] font-semibold tracking-tight text-white">31.4</span><span className="text-[13px] text-[#C7C6C6]">kg CO₂e / month saved</span><span className="mt-3 rounded-full bg-[#2A2A2A] px-3 py-1 text-[11px] text-white">High Peer Adoption (84%)</span></div>
        </div>
      </section>

      <section className="flex flex-col gap-4"><div><h2 className="text-[20px] font-medium tracking-tight text-white">Try another scenario</h2><p className="text-[14px] text-[#C4C7C8]">One-click behavioral archetypes modeled from high-performing campus peers.</p></div><div className="grid grid-cols-1 gap-4 md:grid-cols-3">{recommendations.map(({ icon: Icon, saving: amount, title, detail, feasibility }) => <article key={title} className="group flex flex-col justify-between gap-5 rounded-2xl bg-[#1C1B1B] p-5 shadow-sm transition-colors hover:bg-[#201F1F]"><div className="flex flex-col gap-3"><div className="flex items-center justify-between"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#2A2A2A]"><Icon size={18} /></span><span className="rounded-full bg-[#2A2A2A] px-2 py-0.5 text-[11px] font-medium text-white">{amount}</span></div><div><h3 className="text-[13px] font-semibold text-white">{title}</h3><p className="mt-1 text-[12px] leading-4 text-[#C4C7C8]">{detail}</p></div></div><div className="flex flex-col gap-3"><div className="flex items-center gap-1.5 text-[11px] text-[#C4C7C8]"><CheckCircle2 size={15} />{feasibility}</div><Link to="/simulator" className="flex w-full items-center justify-between rounded-lg bg-[#2A2A2A] px-3 py-2 text-[13px] font-medium text-white transition-colors hover:bg-[#353534]">Load scenario<ArrowRight size={16} className="transition-transform group-hover:translate-x-1" /></Link></div></article>)}</div></section>
    </div>
  );
};

export default RecommendationsPage;