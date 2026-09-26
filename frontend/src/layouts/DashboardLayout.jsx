import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

const DashboardLayout = () => {
  return (
    <div className="metal-layout pl-64 bg-[#0B0B0B] min-h-screen text-[#F2F2F2]">
      <Sidebar />
      <Topbar />
      <main className="metal-main relative pt-16 min-h-screen bg-[#0B0B0B]">
        <div className="w-full max-w-[1400px] mx-auto px-6 xl:px-8 py-8 flex flex-col gap-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;