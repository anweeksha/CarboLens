import { useState } from 'react';

const SimulatorPreview = () => {
  const [sliderValue, setSliderValue] = useState(4);
  const [scenarioValue, setScenarioValue] = useState('153.2 kg');
  const [savedValue, setSavedValue] = useState('31.4 kg CO₂e');

  const handleSliderChange = (e) => {
    const newVal = parseInt(e.target.value);
    setSliderValue(newVal);
    const tripsRemaining = 12 - newVal;
    const saved = (tripsRemaining * 3.14).toFixed(1);
    const scenario = (184.6 - parseFloat(saved)).toFixed(1);
    setScenarioValue(`${scenario} kg`);
    setSavedValue(`${saved} kg CO₂e`);
  };

  return (
    <section className="p-6 lg:p-8 rounded-[24px] bg-[#141414] mb-8 shadow-xl flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div className="flex flex-col gap-2">
          <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase tracking-widest">DYNAMIC SIMULATION</span>
          <h2 className="text-2xl text-[#F2F2F2] font-semibold tracking-tight">What if you changed one thing?</h2>
          <p className="text-sm text-[#AFAFAF]">Model immediate behavioral interventions and inspect your projected trajectory.</p>
        </div>
        {/* Reactive Comparison Split Block */}
        <div className="flex items-center gap-4 bg-[#0e0e0e] p-4 rounded-2xl">
          <div className="flex flex-col">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase">CURRENT</span>
            <span className="text-xl text-[#AFAFAF] font-medium">184.6 kg</span>
          </div>
          <span className="material-symbols-outlined text-[#AFAFAF] text-[18px]">trending_flat</span>
          <div className="flex flex-col">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase">SCENARIO</span>
            <span className="text-xl text-[#F2F2F2] font-bold transition-all">{scenarioValue}</span>
          </div>
          <div className="h-8 w-px bg-[#2a2a2a] hidden sm:block"></div>
          <div className="hidden sm:flex flex-col items-end">
            <span className="font-eyebrow-tag text-[11px] text-[#AFAFAF] uppercase">SAVED</span>
            <span className="px-3 py-0.5 rounded-full bg-[#2a2a2a] text-[#F2F2F2] text-[13px] font-semibold">
              {savedValue}
            </span>
          </div>
        </div>
      </div>
      {/* Interactive Slider Component */}
      <div className="flex flex-col gap-2 bg-[#0e0e0e] p-6 rounded-2xl">
        <div className="flex items-center justify-between">
          <label className="text-[13px] text-[#F2F2F2] font-medium flex items-center gap-2" htmlFor="carTripSlider">
            <span className="material-symbols-outlined text-[16px]">directions_car</span>
            Car trips per month (replaced with campus shuttle or bike)
          </label>
          <span className="text-xl text-[#F2F2F2] font-bold">{12 - sliderValue} trips remaining</span>
        </div>
        <div className="relative py-2">
          <input
            className="w-full h-2 bg-[#353534] rounded-lg appearance-none cursor-pointer accent-white"
            id="carTripSlider"
            max="12"
            min="0"
            step="1"
            type="range"
            value={sliderValue}
            onChange={handleSliderChange}
          />
        </div>
        <div className="flex justify-between text-[11px] text-[#AFAFAF]">
          <span>0 (Full Shift: Max Save)</span>
          <span>Current Baseline: 12 trips</span>
        </div>
      </div>
    </section>
  );
};

export default SimulatorPreview;