export default function ResultsArea() {
  return (
    <section className="rounded-lg border border-black/10 dark:border-white/10 bg-white/60 dark:bg-black/30 p-4 h-full">
      <div className="mb-3">
        <h2 className="text-base font-semibold">Results</h2>
        <p className="text-sm opacity-70">
          Summaries, highlights, and risk classifications.
        </p>
      </div>

      <div className="grid gap-3">
        <div className="rounded-md border border-black/10 dark:border-white/10 p-3">
          <div className="text-sm font-medium">Summary</div>
          <p className="text-sm opacity-80 mt-1">
            Ask a question to see the summarized insights here.
          </p>
        </div>

        <div className="rounded-md border border-black/10 dark:border-white/10 p-3">
          <div className="text-sm font-medium">Highlights</div>
          <ul className="list-disc pl-5 text-sm opacity-80">
            <li>Key clauses and extracted entities will show here.</li>
          </ul>
        </div>

        <div className="rounded-md border border-black/10 dark:border-white/10 p-3">
          <div className="text-sm font-medium">Risk classification</div>
          <div className="mt-1 flex flex-wrap gap-1">
            {["Low", "Medium", "High"].map((risk) => (
              <span
                key={risk}
                className="px-2 py-0.5 rounded-full text-xs border border-black/10 dark:border-white/10"
              >
                {risk}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
