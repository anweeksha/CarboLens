import { useState } from 'react';
import {
  Activity,
  ArrowDown,
  Bolt,
  BusFront,
  CalendarDays,
  Check,
  ChevronDown,
  Download,
  Edit2,
  Info,
  Plus,
  ReceiptText,
  Recycle,
  Search,
  Share,
  SlidersHorizontal,
  TrendingDown,
  Utensils,
  X,
} from 'lucide-react';

const categories = {
  transport: {
    label: 'Transportation',
    icon: BusFront,
    unit: 'km',
    options: [
      { text: 'Car (Solo Combustion) - 0.24 kg/km', factor: 0.24, amount: 18 },
      { text: 'Car (Carpool / EV) - 0.11 kg/km', factor: 0.11, amount: 18 },
      { text: 'Campus Shuttle Bus - 0.04 kg/km', factor: 0.04, amount: 12 },
      { text: 'Metro Transit Line - 0.03 kg/km', factor: 0.03, amount: 22 },
      { text: 'Bicycle / Micro-mobility - 0 kg/km', factor: 0, amount: 5 },
      { text: 'Walking - 0 kg/km', factor: 0, amount: 2 },
    ],
  },
  electricity: {
    label: 'Electricity',
    icon: Bolt,
    unit: 'hrs',
    options: [
      { text: 'Lab Heavy Compute Rig - 0.60 kg/hr', factor: 0.6, amount: 4 },
      { text: 'Dorm AC / Space Heater - 0.70 kg/hr', factor: 0.7, amount: 3 },
      { text: 'Laptop & External Monitor - 0.05 kg/hr', factor: 0.05, amount: 8 },
      { text: 'General Lab Lighting & Bench - 0.12 kg/hr', factor: 0.12, amount: 6 },
    ],
  },
  food: {
    label: 'Food',
    icon: Utensils,
    unit: 'trips',
    options: [
      { text: 'Cafeteria Red Meat Entrée - 4.50 kg/meal', factor: 4.5, amount: 1 },
      { text: 'Cafeteria Poultry / Fish Meal - 1.80 kg/meal', factor: 1.8, amount: 1 },
      { text: 'Campus Plant-based Bowl - 0.80 kg/meal', factor: 0.8, amount: 1 },
      { text: 'Espresso / Dairy Beverage - 0.35 kg/cup', factor: 0.35, amount: 2 },
      { text: 'Oat Milk Beverage - 0.09 kg/cup', factor: 0.09, amount: 2 },
    ],
  },
  waste: {
    label: 'Waste',
    icon: Recycle,
    unit: 'trips',
    options: [
      { text: 'Mixed Non-Recycled Landfill - 0.90 kg/bag', factor: 0.9, amount: 1 },
      { text: 'Single-use Plastic Lab Consumables - 0.45 kg/set', factor: 0.45, amount: 2 },
      { text: 'Composted Organic Waste - 0.10 kg/bin', factor: 0.1, amount: 1 },
      { text: 'Cardboard / Clean Paper Recycling - 0.05 kg/bin', factor: 0.05, amount: 3 },
    ],
  },
};

const initialActivities = [
  { id: 1, time: 'Today, 08:45', name: 'Car commute (North Campus to Lab)', detail: 'Solo passenger • Gasoline sedan', category: 'Transportation', magnitude: '18 km', impact: 4.32 },
  { id: 2, time: 'Yesterday, 17:15', name: 'Metro transit commute (Central Line)', detail: 'Oxford City Link • High density', category: 'Transportation', magnitude: '22 km', impact: 0.88 },
  { id: 3, time: 'Yesterday, 14:00', name: 'Engineering workstation compute & AC', detail: 'Dual GPU Rig • Lab 402 HVAC allocation', category: 'Electricity', magnitude: '3.5 hrs', impact: 2.1 },
  { id: 4, time: 'Sep 26, 12:30', name: 'Campus dining hall (Plant-based bowl)', detail: 'Sourced within 20 miles • Low packaging', category: 'Food', magnitude: '1 meal', impact: 0.8 },
  { id: 5, time: 'Sep 25, 19:10', name: 'Campus electric shuttle transit', detail: 'Zero tailpipe emissions circuit', category: 'Transportation', magnitude: '12 km', impact: 0.38 },
  { id: 6, time: 'Sep 24, 21:00', name: 'Dorm climate & ventilation heating cycle', detail: 'Geothermal campus microgrid', category: 'Electricity', magnitude: '3.0 hrs', impact: 2.1 },
];

const metricCards = [
  { label: 'Transportation', value: '72.4', share: '39%', detail: 'Commutes, transit trips & flights', footer: 'Quota Pace: Nominal', icon: BusFront },
  { label: 'Electricity', value: '51.2', share: '28%', detail: 'Studio workstations, dorm & HVAC', footer: 'Low Carbon Grid', icon: Bolt },
  { label: 'Food & Dining', value: '48.0', share: '26%', detail: 'Campus cafeteria, groceries & meals', footer: 'Plant-forward: 68%', icon: Utensils },
  { label: 'Waste & Landfill', value: '13.0', share: '7%', detail: 'Single-use items & lab packaging', footer: 'Compost Diversion: 82%', icon: Recycle },
];

const fieldClass = 'w-full rounded-xl border border-white/[0.07] bg-[#1E1E1E] px-3 py-2.5 text-[13px] text-[#F2F2F2] outline-none transition-colors focus:border-white/25';

const ActivitiesPage = () => {
  const [category, setCategory] = useState('transport');
  const [optionIndex, setOptionIndex] = useState(0);
  const [amount, setAmount] = useState(18);
  const [unit, setUnit] = useState('km');
  const [activities, setActivities] = useState(initialActivities);
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const config = categories[category];
  const selectedOption = config.options[optionIndex];
  const impact = (selectedOption.factor * Math.max(0, Number(amount) || 0)).toFixed(2);

  const selectCategory = (nextCategory) => {
    setCategory(nextCategory);
    setOptionIndex(0);
    setAmount(categories[nextCategory].options[0].amount);
    setUnit(categories[nextCategory].unit);
  };

  const addActivity = (event) => {
    event.preventDefault();
    setActivities((current) => [{
      id: Date.now(),
      time: 'Just now',
      name: selectedOption.text.split(' - ')[0],
      detail: 'Manual telemetry ingest • Just logged',
      category: config.label,
      magnitude: `${amount} ${unit}`,
      impact: Number(impact),
    }, ...current]);
  };

  const exportLog = () => {
    const rows = [['Timestamp', 'Activity Details', 'Domain', 'Magnitude', 'CO2e Delta'], ...activities.map((item) => [item.time, item.name, item.category, item.magnitude, `${item.impact.toFixed(2)} kg`])];
    const csv = rows.map((row) => row.map((value) => `"${String(value).replaceAll('"', '""')}"`).join(',')).join('\n');
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
    link.download = 'carbonlens-activity-log.csv';
    link.click();
    URL.revokeObjectURL(link.href);
  };

  const filteredActivities = activities.filter((item) => {
    const matchesQuery = `${item.name} ${item.detail} ${item.category}`.toLowerCase().includes(query.toLowerCase());
    return matchesQuery && (filter === 'all' || item.category === filter);
  });

  return (
    <div className="flex flex-col gap-8">
      <section className="flex flex-col justify-between gap-6 pt-2 lg:flex-row lg:items-end">
        <div className="flex max-w-2xl flex-col gap-2">
          <div className="inline-flex items-center gap-2 self-start rounded-full border border-white/[0.08] bg-[#141414] px-2.5 py-1">
            <span className="h-1.5 w-1.5 rounded-full bg-[#F2F2F2]" />
            <span className="text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Activity Tracker</span>
          </div>
          <h1 className="text-[36px] font-semibold leading-tight tracking-tight text-[#F2F2F2] lg:text-[42px]">What did you do today?</h1>
          <p className="text-[14px] leading-relaxed text-[#AFAFAF]">Log your everyday activities and understand their carbon impact against the Oxford campus grid baseline.</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 rounded-xl border border-white/[0.07] bg-[#141414] px-3 py-2 text-[13px] text-[#AFAFAF]"><CalendarDays size={16} className="text-[#5F5F5F]" />Cycle: March 2025</div>
          <button type="button" onClick={exportLog} className="inline-flex items-center gap-2 rounded-xl border border-white/[0.08] bg-[#141414] px-4 py-2 text-[13px] font-medium text-[#F2F2F2] transition-colors hover:bg-white/[0.06]"><Share size={16} className="text-[#AFAFAF]" />Export Log</button>
          <button type="button" onClick={() => document.getElementById('log-activity-panel')?.scrollIntoView({ behavior: 'smooth' })} className="inline-flex items-center gap-2 rounded-xl bg-[#F2F2F2] px-4 py-2 text-[13px] font-semibold text-[#0B0B0B] transition-colors hover:bg-white"><Plus size={18} />Log Activity</button>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metricCards.map(({ label, value, share, detail, footer, icon: Icon }) => (
          <article key={label} className="flex flex-col justify-between gap-4 rounded-2xl border border-white/[0.07] bg-[#141414] p-5 transition-colors hover:border-white/15">
            <div className="flex items-start justify-between">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/[0.06] bg-[#1E1E1E] text-[#F2F2F2]"><Icon size={18} /></span>
              <span className="rounded-full border border-white/[0.06] bg-[#1E1E1E] px-2.5 py-0.5 text-[11px] font-semibold text-[#AFAFAF]">{share} Share</span>
            </div>
            <div>
              <div className="text-[13px] font-medium text-[#AFAFAF]">{label}</div>
              <div className="mt-0.5 text-[32px] font-semibold tracking-tight text-[#F2F2F2]">{value} <span className="text-[16px] font-normal text-[#5F5F5F]">kg</span></div>
              <p className="mt-1 text-[12px] text-[#5F5F5F]">{detail}</p>
            </div>
            <div className="flex flex-col gap-1.5 pt-1">
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-[#1E1E1E]"><div className="h-full rounded-full bg-[#B8B8B8]" style={{ width: share }} /></div>
              <div className="flex items-center justify-between text-[11px] text-[#5F5F5F]"><span>{footer}</span><span className="font-medium text-[#AFAFAF]">{share}</span></div>
            </div>
          </article>
        ))}
      </section>

      <section id="log-activity-panel" className="flex flex-col gap-6 rounded-2xl border border-white/[0.07] bg-[#141414] p-6 lg:p-7">
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
          <div>
            <div className="flex items-center gap-2 text-[#AFAFAF]"><Activity size={16} className="text-[#5F5F5F]" /><span className="text-[11px] font-semibold uppercase tracking-wider">Dynamic Ingestion</span></div>
            <h2 className="mt-1 text-[20px] font-semibold tracking-tight text-[#F2F2F2]">Quick Activity Log</h2>
            <p className="text-[13px] text-[#AFAFAF]">Telemetry-assisted emissions calculation based on Oxford campus grid baseline.</p>
          </div>
          <div className="flex items-center gap-4 self-start rounded-xl border border-white/[0.07] bg-[#1E1E1E] px-4 py-2.5 lg:self-auto">
            <div><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#5F5F5F]">Calculated Impact</span><span className="text-[18px] font-semibold text-[#F2F2F2]">~{impact} kg CO₂e</span></div>
            <span className="flex h-8 w-8 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-[#F2F2F2]">CO₂</span>
          </div>
        </div>

        <div className="flex max-w-lg items-center gap-1.5 rounded-xl border border-white/[0.06] bg-[#0B0B0B] p-1">
          {Object.entries(categories).map(([key, item]) => {
            const Icon = item.icon;
            return <button key={key} type="button" onClick={() => selectCategory(key)} className={`flex flex-1 items-center justify-center gap-1.5 rounded-lg px-2 py-1.5 text-[12px] font-medium transition-colors ${category === key ? 'border border-white/[0.08] bg-white/[0.08] text-[#F2F2F2]' : 'text-[#AFAFAF] hover:bg-white/[0.04] hover:text-[#F2F2F2]'}`}><Icon size={15} /><span>{item.label === 'Transportation' ? item.label : item.label === 'Electricity' ? item.label : item.label}</span></button>;
          })}
        </div>

        <form onSubmit={addActivity} className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
          <label className="flex flex-col gap-1.5"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Activity Type</span><span className="relative"><select value={optionIndex} onChange={(event) => setOptionIndex(Number(event.target.value))} className={`${fieldClass} appearance-none pr-9`}>{config.options.map((option, index) => <option key={option.text} value={index}>{option.text}</option>)}</select><ChevronDown size={16} className="pointer-events-none absolute right-3 top-3 text-[#5F5F5F]" /></span></label>
          <label className="flex flex-col gap-1.5"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Distance / Duration</span><span className="flex items-center rounded-xl border border-white/[0.07] bg-[#1E1E1E] px-2 py-1"><button type="button" aria-label="Decrease amount" onClick={() => setAmount((current) => Math.max(1, Number(current) - 1))} className="flex h-7 w-7 items-center justify-center rounded-lg text-[#AFAFAF] hover:bg-white/[0.08] hover:text-[#F2F2F2]">−</button><input aria-label="Distance or duration amount" type="number" min="1" value={amount} onChange={(event) => setAmount(event.target.value)} className="w-full bg-transparent text-center text-[18px] font-semibold text-[#F2F2F2] outline-none" /><button type="button" aria-label="Increase amount" onClick={() => setAmount((current) => Number(current) + 1)} className="flex h-7 w-7 items-center justify-center rounded-lg text-[#AFAFAF] hover:bg-white/[0.08] hover:text-[#F2F2F2]"><Plus size={16} /></button></span></label>
          <label className="flex flex-col gap-1.5"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Metric Unit</span><span className="relative"><select value={unit} onChange={(event) => setUnit(event.target.value)} className={`${fieldClass} appearance-none pr-9`}><option value="km">Kilometers (km)</option><option value="mi">Miles (mi)</option><option value="hrs">Duration (Hours)</option><option value="trips">Discrete Trips</option></select><SlidersHorizontal size={16} className="pointer-events-none absolute right-3 top-3 text-[#5F5F5F]" /></span></label>
          <div className="flex flex-col gap-1.5"><span className="text-[11px] font-semibold uppercase tracking-wider text-[#AFAFAF]">Logging Date</span><div className={`${fieldClass} flex items-center justify-between cursor-default`}>Today, Mar 28, 2025<CalendarDays size={16} className="text-[#5F5F5F]" /></div></div>
          <div className="flex flex-col gap-3 pt-2 sm:flex-row sm:items-center sm:justify-between lg:col-span-4">
            <div className="flex items-center gap-2 text-[12px] text-[#5F5F5F]"><Info size={15} /><span>Emission factor automatically pegged to Oxford 2024–25 campus baseline.</span></div>
            <div className="flex w-full justify-end gap-3 sm:w-auto"><button type="button" className="inline-flex items-center gap-2 rounded-xl border border-white/[0.08] bg-[#1E1E1E] px-4 py-2 text-[13px] font-medium text-[#F2F2F2] transition-colors hover:bg-white/[0.06]"><ReceiptText size={16} className="text-[#AFAFAF]" />Scan Transit Slip</button><button type="submit" className="inline-flex items-center gap-2 rounded-xl bg-[#F2F2F2] px-5 py-2 text-[13px] font-semibold text-[#0B0B0B] shadow-sm transition-colors hover:bg-white"><Check size={17} />Commit Activity</button></div>
          </div>
        </form>
      </section>

      <section className="flex flex-col gap-4">
        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
          <div><h2 className="text-[20px] font-semibold tracking-tight text-[#F2F2F2]">Recent Activity</h2><p className="text-[13px] text-[#AFAFAF]">Validated emissions recorded during current billing window.</p></div>
          <div className="flex flex-wrap items-center gap-2">
            <label className="relative"><Search size={16} className="absolute left-2.5 top-2.5 text-[#5F5F5F]" /><input value={query} onChange={(event) => setQuery(event.target.value)} type="search" placeholder="Filter logged events..." className="w-52 rounded-xl border border-white/[0.07] bg-[#141414] py-1.5 pl-8 pr-3 text-[13px] text-[#F2F2F2] outline-none placeholder:text-[#5F5F5F] focus:border-white/20 sm:w-64" /></label>
            <label className="relative"><select value={filter} onChange={(event) => setFilter(event.target.value)} className="appearance-none rounded-xl border border-white/[0.07] bg-[#141414] py-1.5 pl-3 pr-8 text-[13px] text-[#F2F2F2] outline-none"><option value="all">All Categories</option><option>Transportation</option><option>Electricity</option><option>Food</option><option>Waste</option></select><SlidersHorizontal size={15} className="pointer-events-none absolute right-2 top-2.5 text-[#5F5F5F]" /></label>
          </div>
        </div>
        <div className="overflow-x-auto rounded-2xl border border-white/[0.07] bg-[#141414]">
          <table className="w-full min-w-[900px] border-collapse text-left">
            <thead><tr className="border-b border-white/[0.06] text-[11px] font-semibold uppercase tracking-wider text-[#5F5F5F]"><th className="px-5 py-3.5">Timestamp</th><th className="px-5 py-3.5">Activity Details</th><th className="px-5 py-3.5">Domain</th><th className="px-5 py-3.5">Magnitude</th><th className="px-5 py-3.5">CO₂e Delta</th><th className="px-5 py-3.5 text-right">Actions</th></tr></thead>
            <tbody className="divide-y divide-white/[0.04] text-[13px]">
              {filteredActivities.map((item) => <tr key={item.id} className="group transition-colors hover:bg-white/[0.02]"><td className="whitespace-nowrap px-5 py-3.5 text-[#AFAFAF]">{item.time}</td><td className="px-5 py-3.5"><div className="font-medium text-[#F2F2F2]">{item.name}</div><div className="text-[11px] text-[#5F5F5F]">{item.detail}</div></td><td className="whitespace-nowrap px-5 py-3.5"><span className="inline-flex items-center gap-1.5 rounded-full border border-white/[0.06] bg-[#1E1E1E] px-2.5 py-1 text-[11px] font-medium text-[#AFAFAF]"><span className="h-1.5 w-1.5 rounded-full bg-[#B8B8B8]" />{item.category}</span></td><td className="whitespace-nowrap px-5 py-3.5 font-medium text-[#F2F2F2]">{item.magnitude}</td><td className="whitespace-nowrap px-5 py-3.5"><span className="rounded-md border border-white/[0.06] bg-[#1E1E1E] px-2 py-0.5 text-[12px] font-semibold text-[#F2F2F2]">+{item.impact.toFixed(2)} kg</span></td><td className="whitespace-nowrap px-5 py-3.5 text-right"><div className="inline-flex items-center gap-1 text-[#5F5F5F]"><button type="button" title="Edit" aria-label={`Edit ${item.name}`} className="rounded-lg p-1 transition-colors hover:bg-white/[0.06] hover:text-[#F2F2F2]"><Edit2 size={16} /></button><button type="button" title="Delete" aria-label={`Delete ${item.name}`} onClick={() => setActivities((current) => current.filter((activity) => activity.id !== item.id))} className="rounded-lg p-1 transition-colors hover:bg-white/[0.06] hover:text-white"><X size={16} /></button></div></td></tr>)}
              {filteredActivities.length === 0 && <tr><td colSpan="6" className="px-5 py-10 text-center text-[13px] text-[#5F5F5F]">No activity matches this filter.</td></tr>}
            </tbody>
          </table>
        </div>
      </section>

      <footer className="flex flex-col items-start justify-between gap-4 rounded-2xl border border-white/[0.07] bg-[#141414] p-5 lg:flex-row lg:items-center">
        <div className="flex flex-wrap items-center gap-6">
          <div><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#5F5F5F]">Audit Scope</span><span className="text-[13px] font-medium text-[#F2F2F2]">This Month Overview</span></div><div className="hidden h-8 w-px bg-white/[0.06] sm:block" />
          <div><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#5F5F5F]">Entries Logged</span><span className="text-[18px] font-semibold text-[#F2F2F2]">{36 + activities.length} events</span></div><div className="hidden h-8 w-px bg-white/[0.06] sm:block" />
          <div><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#5F5F5F]">Aggregated Total</span><span className="text-[18px] font-semibold text-[#F2F2F2]">184.6 kg CO₂e</span></div><div className="hidden h-8 w-px bg-white/[0.06] sm:block" />
          <div><span className="block text-[10px] font-semibold uppercase tracking-wider text-[#5F5F5F]">Cycle Delta</span><span className="flex items-center gap-1 text-[13px] font-semibold text-[#F2F2F2]"><TrendingDown size={16} />12.4% vs last cycle</span></div>
        </div>
        <div className="flex w-full justify-end gap-3 lg:w-auto"><button type="button" className="inline-flex items-center gap-2 rounded-xl border border-white/[0.07] bg-[#1E1E1E] px-3.5 py-2 text-[13px] font-medium text-[#F2F2F2] transition-colors hover:bg-white/[0.06]"><ArrowDown size={16} className="text-[#AFAFAF]" />Sync Smart Meters</button><button type="button" onClick={exportLog} className="inline-flex items-center gap-2 rounded-xl border border-white/[0.07] bg-[#1E1E1E] px-3.5 py-2 text-[13px] font-medium text-[#F2F2F2] transition-colors hover:bg-white/[0.06]"><Download size={16} className="text-[#AFAFAF]" />Download CSV</button></div>
      </footer>
    </div>
  );
};

export default ActivitiesPage;