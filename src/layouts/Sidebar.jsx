import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  const navigation = [
    { path: '/overview', label: 'Overview' },
    { path: '/activities', label: 'Activities' },
    { path: '/carbon', label: 'My Carbon' },
    { path: '/simulator', label: 'Simulator' },
    { path: '/recommendations', label: 'Recommendations' },
    { path: '/challenges', label: 'Challenges' },
    { path: '/leaderboard', label: 'Leaderboard' },
    { path: '/campus', label: 'Campus' },
    { path: '/reports', label: 'Reports' },
  ];

  return (
    <aside className="metal-sidebar fixed left-0 top-0 h-full w-64 bg-[#0B0B0B] border-r border-white/[0.07] z-50 flex flex-col justify-between py-5 px-4">
      <div className="flex flex-col gap-5">
        {/* Logo */}
        <div className="flex items-center gap-3 px-1">
          <img 
            alt="CarbonLens Logo" 
            className="h-8 w-auto object-contain" 
            src="https://lh3.googleusercontent.com/aida/AEtjO1XuyFxAyfFdv80Zvtdch2cmu2OWxvW5w3Q_7RSewlA9d1n8j8KuZxfTLnTDizFMyp3ljG02VC0BAHO595dK7lXjBd5IlQyK5HYBqat4LzyOgMzYLmgMtOvBHJL3t5KW4E3mQHrLpkaMxcnCSw11wu22VBZNOSlXMWru0U2HHvNDyOAeGR5g0ts146C256G24TlZCssNSN3Af_sY2jQVb2sw_GSVasv0cx87Xq4Nz1tfDZ4479tIQYkec7A"
          />
          <div className="flex flex-col">
            <span className="font-headline-md text-headline-md font-semibold text-[#F2F2F2] tracking-tight">
              CarbonLens
            </span>
            <span className="font-eyebrow-tag text-[10px] text-[#AFAFAF] uppercase tracking-wider">
              See impact. Change trajectory.
            </span>
          </div>
        </div>

        <div className="h-px w-full bg-[#1E1E1E]" />

        {/* Navigation */}
        <nav className="flex flex-col gap-1">
          {navigation.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-3 py-2 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'metal-nav-active bg-[#1E1E1E] text-[#F2F2F2] font-medium border border-white/10 shadow-sm'
                    : 'text-[#AFAFAF] hover:bg-[#1A1A1A] hover:text-[#F2F2F2]'
                }`
              }
            >
              <span className="font-label-md text-sm">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Bottom user section */}
      <div className="flex flex-col gap-3 pt-3 border-t border-[#1E1E1E]">
        <div className="flex items-center justify-between p-2 rounded-lg bg-[#141414] border border-[#1E1E1E]">
          <div className="flex items-center gap-2.5">
            <div className="relative">
              <div className="w-8 h-8 rounded-full bg-[#F2F2F2] flex items-center justify-center">
                <span className="material-symbols-outlined text-[#0E0E0E] text-[18px]">person</span>
              </div>
              <span className="absolute bottom-0 right-0 w-2 h-2 rounded-full bg-white ring-2 ring-[#141414]"></span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-[#F2F2F2]">Orni Bera                  </span>
              <span className="text-[11px] text-[#AFAFAF] truncate max-w-[100px]">Dept. of CSE</span>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <a className="p-1.5 rounded hover:bg-[#1E1E1E] text-[#AFAFAF] hover:text-[#F2F2F2] transition-colors flex items-center justify-center" href="#">
              <span className="material-symbols-outlined text-[16px]">settings</span>
            </a>
            <a className="p-1.5 rounded hover:bg-[#1E1E1E] text-[#AFAFAF] hover:text-[#F2F2F2] transition-colors flex items-center justify-center" href="#">
              <span className="material-symbols-outlined text-[16px]">logout</span>
            </a>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;