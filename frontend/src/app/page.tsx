import Sidebar from "../components/Sidebar";
import UploadArea from "../components/UploadArea";
import ChatBox from "../components/ChatBox";
import ResultsArea from "../components/ResultsArea";

export default function Home() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] min-h-screen">
      {/* Sidebar (visible on lg+) */}
      <aside className="hidden lg:flex flex-col border-r border-black/10 dark:border-white/10 bg-white/50 dark:bg-black/20 p-4 gap-4">
        <Sidebar />
      </aside>

      {/* Main content */}
      <div className="flex flex-col">
        {/* Top bar (mobile) */}
        <div className="lg:hidden sticky top-0 z-10 border-b border-black/10 dark:border-white/10 bg-white/70 dark:bg-black/40 backdrop-blur-md">
          <div className="px-4 py-3">
            <div className="font-semibold">VisuLex</div>
            <div className="text-sm opacity-70">
              AI-assisted document analysis
            </div>
          </div>
        </div>

        {/* Content grid */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 p-4 xl:p-6">
          <div className="flex flex-col gap-4">
            <UploadArea />
            <ChatBox />
          </div>

          <div className="min-h-[40vh]">
            <ResultsArea />
          </div>
        </div>
      </div>
    </div>
  );
}
