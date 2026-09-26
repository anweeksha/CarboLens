import { useState } from 'react';
import {
  ArrowRight,
  Bookmark,
  BusFront,
  Check,
  CheckCircle2,
  Leaf,
  Minus,
  Plus,
  Recycle,
  RotateCcw,
  Thermometer,
  Utensils,
} from 'lucide-react';

const initialValues = { car: 4, ac: 2, food: 2, waste: 2.5 };
const baselineValues = { car: 12, ac: 4, food: 6, waste: 4 };

const parameters = [
  { key: 'car', title: 'Car trips / month', detail: 'Baseline: 12 trips • ~3.14 kg CO₂e per campus round-trip', unit: 'trips / month', shortUnit: 'trips', min: 0, max: 20, step: 1, rate: 3.925, baselineImpact: 72.4, icon: BusFront, quick: [-2, 2], preset: 'Zero Car', presetValue: 0, scale: 'Scale: 0 – 20 trips' },
  { key: 'ac', title: 'AC & climate usage / day', detail: 'Baseline: 4.0 hrs/day • Dorm HVAC load ~0.70 kg/hr', unit: 'hrs / day', shortUnit: 'hrs', min: 0, max: 12, step: 0.5, rate: 3.5, baselineImpact: 51.2, icon: Thermometer, quick: [-1, 1], preset: 'Eco 1.5h', presetValue: 1.5, scale: 'Scale: 0 – 12 hrs' },
  { key: 'food', title: 'Meat-centric meals / week', detail: 'Baseline: 6 meals • ~2.4 kg CO₂e delta vs plant-based', unit: 'meals / week', shortUnit: 'meals', min: 0, max: 14, step: 1, rate: 2.4, baselineImpact: 48, icon: Utensils, quick: [-1, 1], preset: 'Plant Only (0)', presetValue: 0, scale: 'Scale: 0 – 14 meals' },
  { key: 'waste', title: 'Waste & landfill / week', detail: 'Baseline: 4.0 kg • Packaging & uncomposted solid waste', unit: 'kg / week', shortUnit: 'kg', min: 0, max: 10, step: 0.5, rate: 1.6667, baselineImpact: 13, quick: [-0.5, 0.5], preset: 'Min Waste (1kg)', presetValue: 1, scale: 'Scale: 0 – 10 kg' },
];

const scenarios = [
  { title: 'Switch to public transport', detail: 'Full transit substitution for all weekday campus access.', saving: '↓ 42.6 kg CO₂e / mo', feasibility: 'High feasibility • Shuttle stops 8 min away', values: { ac: 2, car: 0, food: 2, waste: 2.5 }, icon: BusFront },
  { title: 'Reduce AC & heating usage', detail: 'Eco-thermostat schedule: 2 hours daily reduction + night setback.', saving: '↓ 18.2 kg CO₂e / mo', feasibility: 'Instant activation • Smart plug sync', values: { ac: 1, car: 4, food: 4, waste: 3 }, icon: Thermometer },
  { title: 'Eat plant-based meals', detail: 'Swap 4 meat lunches weekly for campus dining hall plant bowls.', saving: '↓ 24.8 kg CO₂e / mo', feasibility: 'Low friction • 12 certified campus vendors', values: { ac: 2, car: 4, food: 0, waste: 2.5 }, icon: Leaf },
];

const ParameterSlider = ({ parameter, value, onChange }) => {
  const Icon = parameter.key === 'car'
    ? BusFront
    : parameter.key === 'ac'
      ? Thermometer
      : parameter.key === 'food'
        ? Utensils
        : Recycle;
  const reduction = (baselineValues[parameter.key] - value) * parameter.rate;
  return (
    <article className="flex flex-col gap-3 rounded-xl bg-[#1C1B1B] p-4 shadow-sm transition-colors hover:bg-[#201F1F]">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#2A2A2A] text-white"><Icon size={20} /></span><div><span className="block text-[13px] font-medium text-white">{parameter.title}</span><span className="text-[11px] text-[#C4C7C8]">{parameter.detail}</span></div></div>
        <div className="shrink-0 text-right"><span className="block text-[13px] font-semibold text-white">{value} {parameter.unit}</span><span className="text-[11px] text-[#C4C7C8]">Delta: {value <= baselineValues[parameter.key] ? '-' : '+'}{Math.abs(baselineValues[parameter.key] - value)} {parameter.shortUnit} ({reduction >= 0 ? '-' : '+'}{Math.abs(reduction).toFixed(1)} kg)</span></div>
      </div>
      <input aria-label={parameter.title} type="range" min={parameter.min} max={parameter.max} step={parameter.step} value={value} onChange={(event) => onChange(parameter.key, Number(event.target.value))} className="h-1.5 w-full cursor-pointer appearance-none rounded-lg bg-[#353534] accent-white focus:outline-none" />
      <div className="flex flex-wrap items-center justify-between gap-2"><div className="flex items-center gap-1.5">{parameter.quick.map((delta) => <button key={delta} type="button" onClick={() => onChange(parameter.key, Math.min(parameter.max, Math.max(parameter.min, value + delta)))} className="rounded bg-[#2A2A2A] px-2 py-1 text-[11px] text-[#E5E2E1] transition-colors hover:bg-[#3A3939]">{delta < 0 ? <Minus size={11} className="inline" /> : <Plus size={11} className="inline" />}{Math.abs(delta)}{parameter.key === 'ac' ? ' hr' : parameter.key === 'food' ? ' meal' : parameter.key === 'waste' ? ' kg' : ''}</button>)}<button type="button" onClick={() => onChange(parameter.key, parameter.presetValue)} className="rounded bg-[#2A2A2A] px-2 py-1 text-[11px] text-[#E5E2E1] transition-colors hover:bg-[#3A3939]">{parameter.preset}</button></div><span className="text-[11px] text-[#5F5F5F]">{parameter.scale}</span></div>
    </article>
  );
};

const SimulatorPage = () => {
  const [values, setValues] = useState(initialValues);
  const [saved, setSaved] = useState(false);
  const setValue = (key, value) => {
    setValues((current) => ({ ...current, [key]: value }));
    setSaved(false);
  };
  const projected = 153.2 + (values.car - 4) * 3.925 + (values.ac - 2) * 3.5 + (values.food - 2) * 2.4 + (values.waste - 2.5) * 1.6667;
  const saving = 184.6 - projected;
  const reduction = (saving / 184.6) * 100;
  const categories = [
    { label: 'Transportation', original: 72.4, value: parameters[0].baselineImpact - (baselineValues.car - values.car) * parameters[0].rate },
    { label: 'Electricity (HVAC)', original: 51.2, value: parameters[1].baselineImpact - (baselineValues.ac - values.ac) * parameters[1].rate },
    { label: 'Food & Dining', original: 48, value: parameters[2].baselineImpact - (baselineValues.food - values.food) * parameters[2].rate },
    { label: 'Solid Waste', original: 13, value: parameters[3].baselineImpact - (baselineValues.waste - values.waste) * parameters[3].rate },
  ];
  const setPreset = (preset) => {
    if (preset === 'commute' || preset === 'reset') setValues(initialValues);
    if (preset === 'dorm') setValues({ car: 4, ac: 1.5, food: 4, waste: 3 });
    if (preset === 'plant') setValues({ car: 4, ac: 2, food: 0, waste: 2.5 });
    setSaved(false);
  };

  return (
    <div className="flex flex-col gap-7">
      <header className="flex flex-col justify-between gap-6 xl:flex-row xl:items-end">
        <div className="flex max-w-3xl flex-col gap-2"><div className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-white" /><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">Scenario Lab • Interactive Modeling Engine V3.1</span></div><h1 className="text-[32px] font-semibold tracking-tight text-white">What if you changed one thing?</h1><p className="max-w-2xl text-[16px] leading-6 text-[#C7C6C6]">Explore realistic choices and see their potential carbon impact before you make them. Recalculate your projected cycle trajectory in real time against campus baselines.</p></div>
        <div className="flex flex-wrap items-center gap-2 self-start xl:self-end"><div className="flex items-center rounded-lg bg-[#1C1B1B] p-0.5">{[['commute', 'Commute Shift'], ['dorm', 'Dorm Energy'], ['plant', 'Plant-Forward']].map(([key, label]) => <button key={key} type="button" onClick={() => setPreset(key)} className={`rounded-md px-3 py-1.5 text-[11px] transition-colors ${key === 'commute' ? 'bg-[#2A2A2A] text-white' : 'text-[#C4C7C8] hover:text-white'}`}>{label}</button>)}</div><button type="button" onClick={() => setPreset('reset')} className="inline-flex items-center gap-1.5 rounded-lg bg-[#201F1F] px-3 py-2 text-[13px] text-[#C4C7C8] transition-colors hover:bg-[#2A2A2A] hover:text-white"><RotateCcw size={16} />Reset</button><button type="button" onClick={() => setSaved(true)} className="inline-flex items-center gap-1.5 rounded-lg bg-white px-4 py-2 text-[13px] font-medium text-[#0B0B0B] transition-colors hover:bg-[#E2E2E2]">{saved ? <Check size={16} /> : <Bookmark size={16} />}{saved ? 'Scenario Saved' : 'Save Scenario'}</button></div>
      </header>

      <div className="grid items-start gap-6 lg:grid-cols-12">
        <section className="flex flex-col gap-4 lg:col-span-7">
          <div className="flex items-center justify-between gap-3"><div><h2 className="text-[20px] font-medium tracking-tight text-white">Your current habits</h2><p className="text-[12px] text-[#C4C7C8]">Tune behavioral variables across key emission drivers. Real-time sensitivity telemetry.</p></div><span className="whitespace-nowrap rounded-full bg-[#2A2A2A] px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Active Runtime</span></div>
          <div className="flex flex-col gap-3">{parameters.map((parameter) => <ParameterSlider key={parameter.key} parameter={parameter} value={values[parameter.key]} onChange={setValue} />)}</div>
        </section>

        <section className="flex flex-col gap-4 lg:col-span-5">
          <div className="flex items-center justify-between"><h2 className="text-[20px] font-medium tracking-tight text-white">Projected impact</h2><span className="text-[11px] text-[#C4C7C8]">30-Day Cycle Projection</span></div>
          <div className="relative flex flex-col gap-5 overflow-hidden rounded-2xl bg-[#1C1B1B] p-5 shadow-md lg:p-6">
            <div className="flex flex-col gap-3"><div className="flex items-center justify-between text-[10px] uppercase tracking-wider text-[#C4C7C8]"><span>Baseline Footprint</span><span>Modeled Scenario</span></div><div className="flex items-center justify-between gap-3"><div><span className="block text-[24px] text-[#C4C7C8] line-through opacity-70">184.6</span><span className="text-[11px] text-[#5F5F5F]">kg CO₂e / mo</span></div><span className="flex h-8 w-8 items-center justify-center rounded-full bg-[#2A2A2A]"><ArrowRight size={18} /></span><div className="text-right"><span className="block text-[42px] font-semibold leading-none tracking-tight text-white">{projected.toFixed(1)}</span><span className="text-[11px] text-[#C4C7C8]">kg CO₂e / mo</span></div></div><div className="grid grid-cols-2 gap-2 pt-1"><div className="flex flex-col rounded-lg bg-[#201F1F] p-3"><span className="text-[11px] text-[#C4C7C8]">Potential saving</span><span className="text-[13px] font-semibold text-white">{saving.toFixed(1)} kg CO₂e</span></div><div className="flex flex-col rounded-lg bg-[#201F1F] p-3"><span className="text-[11px] text-[#C4C7C8]">Net Reduction</span><span className="text-[13px] font-semibold text-white">{reduction.toFixed(1)}%</span></div></div></div>
            <div className="flex flex-col gap-4 rounded-xl bg-[#201F1F] p-4"><div className="flex items-center justify-between gap-2 text-[11px]"><span className="text-[#C4C7C8]">Trajectory vs. Target Envelope</span><span className="rounded-full bg-[#353534] px-2 py-0.5 text-[10px] font-semibold text-white">{projected <= 160 ? 'UNDER TARGET CEILING' : 'ABOVE TARGET CEILING'}</span></div><div className="flex justify-center py-1"><svg viewBox="0 0 200 120" className="w-full max-w-[240px]" role="img" aria-label={`${saving.toFixed(1)} kilograms net shift`}><path d="M20 100 A80 80 0 0 1 180 100" pathLength="100" fill="none" stroke="#2A2A2A" strokeLinecap="round" strokeWidth="12" /><path d="M20 100 A80 80 0 0 1 180 100" pathLength="100" fill="none" stroke="white" strokeDasharray={`${Math.min(projected / 220 * 100, 100)} 100`} strokeLinecap="round" strokeWidth="12" /><path d="M152 48l8-6" stroke="#C4C7C8" strokeWidth="2" /><text x="100" y="88" textAnchor="middle" fill="white" fontSize="27" fontWeight="600">-{saving.toFixed(1)}</text><text x="100" y="105" textAnchor="middle" fill="#C4C7C8" fontSize="9" letterSpacing="1">kg net shift</text></svg></div><div className="flex justify-between text-[10px] text-[#5F5F5F]"><span>0 kg</span><span className="text-white">Campus Ceiling: 160.0 kg</span><span>220 kg</span></div><div className="relative h-2 overflow-hidden rounded-full bg-[#353534]"><div className="absolute bottom-0 top-0 z-10 w-0.5 bg-white" style={{ left: `${160 / 220 * 100}%` }} /><div className="h-full rounded-full bg-white transition-all" style={{ width: `${Math.min(projected / 220 * 100, 100)}%` }} /></div><div className="flex justify-between text-[10px] text-[#5F5F5F]"><span>Optimal Efficiency (&lt;120kg)</span><span className="text-[#C7C6C6]">{(160 - projected).toFixed(1)} kg {projected <= 160 ? 'headroom' : 'over target'}</span></div></div>
            <div className="flex flex-col gap-3"><span className="text-[10px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Category Breakdown (Baseline vs Model)</span>{categories.map((item) => <div key={item.label} className="flex flex-col gap-1"><div className="flex justify-between text-[11px]"><span className="text-[#E5E2E1]">{item.label}</span><span className="text-[#C4C7C8]"><span className="mr-1 text-[#5F5F5F] line-through">{item.original.toFixed(1)}</span><span className="font-medium text-white">{item.value.toFixed(1)}</span> kg</span></div><div className="h-1.5 overflow-hidden rounded-full bg-[#201F1F]"><div className="h-full bg-white transition-all" style={{ width: `${Math.max(0, item.value / item.original * 100)}%` }} /></div></div>)}</div>
          </div>
        </section>
      </div>

      <section className="relative overflow-hidden rounded-2xl bg-[#1C1B1B] p-6 shadow-xl lg:p-8"><div className="grid items-center gap-6 lg:grid-cols-12"><div className="flex flex-col gap-3 lg:col-span-8"><div className="flex items-center gap-2"><span className="h-2 w-2 animate-pulse rounded-full bg-white" /><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-white">Highest Sensitivity Lever</span></div><h2 className="text-[24px] font-medium tracking-tight text-white">Switch 10 car trips to public transport</h2><p className="max-w-2xl text-[16px] leading-6 text-[#C7C6C6]">Replacing 10 monthly combustion commutes with the University Electric Shuttle or Oxford City Line eliminates 31.4 kg CO₂e — achieving 72% of your semester net-zero milestone in one behavioral switch.</p><div className="flex flex-wrap gap-2 pt-2"><button type="button" onClick={() => setValue('car', 2)} className="rounded-lg bg-white px-4 py-2.5 text-[13px] font-medium text-[#0B0B0B] transition-colors hover:bg-[#E2E2E2]">Apply this change</button><button type="button" onClick={() => setSaved(true)} className="rounded-lg bg-[#2A2A2A] px-4 py-2.5 text-[13px] text-white transition-colors hover:bg-[#353534]">Add to Personal Target</button></div></div><div className="flex flex-col items-center justify-center rounded-xl bg-[#201F1F] p-6 text-center shadow-inner lg:col-span-4"><span className="text-[10px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Projected Net Benefit</span><span className="text-[40px] font-semibold tracking-tight text-white">31.4</span><span className="text-[13px] text-[#C7C6C6]">kg CO₂e / month saved</span><span className="mt-3 rounded-full bg-[#2A2A2A] px-3 py-1 text-[11px] text-white">High Peer Adoption (84%)</span></div></div></section>

      <section className="flex flex-col gap-4"><div><h2 className="text-[20px] font-medium tracking-tight text-white">Try another scenario</h2><p className="text-[14px] text-[#C4C7C8]">One-click behavioral archetypes modeled from high-performing campus peers.</p></div><div className="grid grid-cols-1 gap-4 md:grid-cols-3">{scenarios.map(({ title, detail, saving: scenarioSaving, feasibility, values: scenarioValues, icon: Icon }) => <article key={title} className="group flex flex-col justify-between gap-5 rounded-2xl bg-[#1C1B1B] p-5 shadow-sm transition-colors hover:bg-[#201F1F]"><div className="flex flex-col gap-3"><div className="flex items-center justify-between"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#2A2A2A]"><Icon size={18} /></span><span className="rounded-full bg-[#2A2A2A] px-2 py-0.5 text-[11px] font-medium text-white">{scenarioSaving}</span></div><div><h3 className="text-[13px] font-semibold text-white">{title}</h3><p className="mt-1 text-[12px] leading-4 text-[#C4C7C8]">{detail}</p></div></div><div className="flex flex-col gap-3"><div className="flex items-center gap-1.5 text-[11px] text-[#C4C7C8]"><CheckCircle2 size={15} />{feasibility}</div><button type="button" onClick={() => { setValues(scenarioValues); setSaved(false); }} className="flex w-full items-center justify-between rounded-lg bg-[#2A2A2A] px-3 py-2 text-[13px] font-medium text-white transition-colors hover:bg-[#353534]">Load scenario<ArrowRight size={16} className="transition-transform group-hover:translate-x-1" /></button></div></article>)}</div></section>
    </div>
  );
};

export default SimulatorPage;