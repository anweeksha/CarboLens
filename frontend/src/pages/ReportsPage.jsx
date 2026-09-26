import { Download, FileSpreadsheet, FileText } from 'lucide-react';

const personalCategories = [
  { label: 'Travel', value: '72.4 kg', share: '39%' },
  { label: 'Electricity', value: '51.2 kg', share: '28%' },
  { label: 'Food', value: '48.0 kg', share: '26%' },
  { label: 'Waste', value: '13.0 kg', share: '7%' },
];

const recentActivities = [
  ['Today, 08:45', 'Car commute (North Campus to Lab)', 'Transportation', '18 km', '4.32 kg'],
  ['Yesterday, 17:15', 'Metro transit commute (Central Line)', 'Transportation', '22 km', '0.88 kg'],
  ['Yesterday, 14:00', 'Engineering workstation compute & AC', 'Electricity', '3.5 hrs', '2.10 kg'],
  ['Sep 26, 12:30', 'Campus dining hall (Plant-based bowl)', 'Food', '1 meal', '0.80 kg'],
  ['Sep 25, 19:10', 'Campus electric shuttle transit', 'Transportation', '12 km', '0.38 kg'],
  ['Sep 24, 21:00', 'Dorm climate & ventilation heating cycle', 'Electricity', '3.0 hrs', '2.10 kg'],
];

const downloadCsv = (filename, rows) => {
  const content = rows.map((row) => row.map((value) => `"${String(value).replaceAll('"', '""')}"`).join(',')).join('\n');
  const url = URL.createObjectURL(new Blob([content], { type: 'text/csv' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
};

const ReportsPage = () => {
  const exportPersonal = () => downloadCsv('carbonlens-personal-carbon-report.csv', [
    ['Personal Carbon Profile', 'March 2025 Cycle'],
    ['Monthly Footprint', '184.6 kg CO₂e'],
    ['Target Profile', '160.0 kg'],
    ['Campus Avg', '212.4 kg'],
    ['Global Net Zero Pace', '-3.2%'],
    ...personalCategories.map((item) => [item.label, item.value, item.share]),
  ]);

  const exportActivities = () => downloadCsv('carbonlens-activity-log.csv', [
    ['Timestamp', 'Activity Details', 'Domain', 'Magnitude', 'CO₂e Delta'],
    ...recentActivities,
    ['This Month Overview', '42 events', 'Aggregated Total', '184.6 kg CO₂e', '12.4% vs last cycle'],
  ]);

  const exportCampus = () => downloadCsv('carbonlens-institutional-audit.csv', [
    ['Institutional Audit', 'Campus Analytics • Institutional Telemetry v2.4'],
    ['Total Campus Footprint', '142.6 t CO₂e'],
    ['Cycle Pace Change', '-8.4%'],
    ['Community Engagement', '3,421 active'],
    ['Verified Telemetry', '12,482 events', '98.4% Confidence'],
    ['Transportation', '68.4 t', '48.0%'],
    ['Electricity & Power', '41.2 t', '28.9%'],
    ['Dining & Sustenance', '23.8 t', '16.7%'],
    ['Waste & Materials', '9.2 t', '6.4%'],
  ]);

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2"><span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C4C7C8]">CarbonLens • March 2025 Cycle</span><h1 className="text-[36px] font-semibold tracking-tight text-white">Reports & Exports</h1><p className="max-w-3xl text-[15px] leading-6 text-[#C7C6C6]">Export the personal, activity, and institutional audit data recorded across CarbonLens.</p></header>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <article className="flex flex-col gap-5 rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div className="flex items-start justify-between"><div><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Personal Carbon Profile</span><h2 className="mt-2 text-[28px] font-semibold tracking-tight text-white">184.6 <span className="text-[16px] font-normal text-[#AFAFAF]">kg CO₂e</span></h2><p className="mt-1 text-[12px] text-[#AFAFAF]">Monthly Footprint • March 2025 Cycle</p></div><FileText size={20} className="text-[#AFAFAF]" /></div><div className="flex flex-col divide-y divide-white/[0.05]">{personalCategories.map((item) => <div key={item.label} className="flex items-center justify-between py-2.5 text-[13px]"><span className="text-[#C7C6C6]">{item.label}</span><span className="text-white">{item.value} <span className="text-[#AFAFAF]">· {item.share}</span></span></div>)}</div><div className="flex items-center justify-between border-t border-white/[0.06] pt-4"><span className="text-[12px] text-[#AFAFAF]">Target Profile 160.0 kg</span><button type="button" onClick={exportPersonal} className="inline-flex items-center gap-2 rounded-lg bg-white px-3.5 py-2 text-[12px] font-semibold text-[#0B0B0B] transition-colors hover:bg-[#E5E5E5]"><Download size={15} />Export Report</button></div></article>

        <article className="flex flex-col gap-5 rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div className="flex items-start justify-between"><div><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Activity Log</span><h2 className="mt-2 text-[28px] font-semibold tracking-tight text-white">42 <span className="text-[16px] font-normal text-[#AFAFAF]">events</span></h2><p className="mt-1 text-[12px] text-[#AFAFAF]">This Month Overview • 184.6 kg CO₂e</p></div><FileSpreadsheet size={20} className="text-[#AFAFAF]" /></div><div className="flex flex-col divide-y divide-white/[0.05]">{recentActivities.slice(0, 4).map(([time, title, domain, magnitude, delta]) => <div key={time} className="flex items-center justify-between gap-3 py-2.5"><div className="min-w-0"><span className="block truncate text-[12px] font-medium text-white">{title}</span><span className="text-[11px] text-[#5F5F5F]">{time} · {domain}</span></div><span className="whitespace-nowrap text-[12px] text-[#C7C6C6]">+{delta}</span></div>)}</div><div className="flex items-center justify-between border-t border-white/[0.06] pt-4"><span className="text-[12px] text-[#AFAFAF]">12.4% vs last cycle</span><button type="button" onClick={exportActivities} className="inline-flex items-center gap-2 rounded-lg bg-[#2A2A2A] px-3.5 py-2 text-[12px] font-medium text-white transition-colors hover:bg-[#353534]"><Download size={15} />Download CSV</button></div></article>

        <article className="flex flex-col gap-5 rounded-2xl border border-white/[0.07] bg-[#141414] p-5"><div className="flex items-start justify-between"><div><span className="text-[11px] font-semibold uppercase tracking-wider text-[#C4C7C8]">Campus Analytics • Institutional Telemetry v2.4</span><h2 className="mt-2 text-[28px] font-semibold tracking-tight text-white">142.6 <span className="text-[16px] font-normal text-[#AFAFAF]">t CO₂e</span></h2><p className="mt-1 text-[12px] text-[#AFAFAF]">Total Campus Footprint</p></div><FileText size={20} className="text-[#AFAFAF]" /></div><div className="grid grid-cols-2 gap-3"><div className="rounded-lg bg-[#1C1B1B] p-3"><span className="block text-[10px] uppercase tracking-wider text-[#5F5F5F]">Cycle Pace Change</span><span className="mt-1 block text-[16px] font-semibold text-white">↓ 8.4%</span></div><div className="rounded-lg bg-[#1C1B1B] p-3"><span className="block text-[10px] uppercase tracking-wider text-[#5F5F5F]">Community Engagement</span><span className="mt-1 block text-[16px] font-semibold text-white">3,421 active</span></div><div className="col-span-2 rounded-lg bg-[#1C1B1B] p-3"><span className="block text-[10px] uppercase tracking-wider text-[#5F5F5F]">Verified Telemetry</span><span className="mt-1 block text-[16px] font-semibold text-white">12,482 events <span className="text-[12px] font-normal text-[#AFAFAF]">· 98.4% Confidence</span></span></div></div><div className="flex items-center justify-between border-t border-white/[0.06] pt-4"><span className="text-[12px] text-[#AFAFAF]">4 Sectors Logged</span><button type="button" onClick={exportCampus} className="inline-flex items-center gap-2 rounded-lg bg-[#2A2A2A] px-3.5 py-2 text-[12px] font-medium text-white transition-colors hover:bg-[#353534]"><Download size={15} />Export Institutional Audit</button></div></article>
      </section>
    </div>
  );
};

export default ReportsPage;