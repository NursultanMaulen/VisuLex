export default function Sidebar() {
  return (
    <div className="flex flex-col gap-4 h-full">
      <div className="px-2">
        <div className="text-xl font-semibold">VisuLex</div>
        <div className="text-xs opacity-70">Dashboard</div>
      </div>

      <nav className="flex flex-col gap-1 text-sm">
        <a
          className="px-2 py-2 rounded hover:bg-black/[0.04] dark:hover:bg-white/[0.06]"
          href="#"
        >
          Upload
        </a>
        <a
          className="px-2 py-2 rounded hover:bg-black/[0.04] dark:hover:bg-white/[0.06]"
          href="#"
        >
          Chat
        </a>
        <a
          className="px-2 py-2 rounded hover:bg-black/[0.04] dark:hover:bg-white/[0.06]"
          href="#"
        >
          Results
        </a>
      </nav>

      <div className="mt-2 text-xs uppercase tracking-wide opacity-60 px-2">
        History
      </div>
      <div className="flex-1 overflow-auto">
        <ul className="space-y-1 px-2 pb-4">
          {[
            "Contract_A.pdf",
            "NDA_ClientB.pdf",
            "Policy_abochert.docx",
            "Lease_2025.pdf",
          ].map((item, idx) => (
            <li key={idx}>
              <button className="w-full text-left px-2 py-2 rounded border border-transparent hover:border-black/10 dark:hover:border-white/10">
                <div className="text-sm">{item}</div>
                <div className="text-[10px] opacity-60">Processed just now</div>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
