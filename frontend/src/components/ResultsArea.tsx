"use client";

import { useUploads } from "../app/UploadsContext";

export default function ResultsArea() {
  const { uploads } = useUploads();
  const done = uploads.filter((u) => u.status === "done");
  const processing = uploads.filter((u) => u.status === "processing");

  return (
    <section className="rounded-lg border border-black/10 dark:border-white/10 bg-white/60 dark:bg-black/30 p-4 h-full">
      <div className="mb-3">
        <h2 className="text-base font-semibold">Results</h2>
        <p className="text-sm opacity-70">
          Summaries, highlights, and risk classifications.
        </p>
      </div>

      {uploads.length === 0 && <EmptyState />}

      {processing.length > 0 && (
        <div className="rounded-md border border-black/10 dark:border-white/10 p-3 mb-3">
          <div className="text-sm font-medium">Processing</div>
          <ul className="mt-2 text-sm list-disc pl-5 opacity-80">
            {processing.map((u) => (
              <li key={u.id}>{u.file.name} — analyzing…</li>
            ))}
          </ul>
        </div>
      )}

      {done.length > 0 && (
        <div className="grid gap-3">
          {done.map((u) => (
            <div
              key={u.id}
              className="rounded-md border border-black/10 dark:border-white/10 p-3"
            >
              <div className="text-sm font-medium truncate">{u.file.name}</div>
              <div className="text-xs opacity-60 mb-2">
                {u.result?.risk} risk
              </div>

              <div className="text-sm font-medium">Summary</div>
              <p className="text-sm opacity-80 mt-1">{u.result?.summary}</p>

              <div className="text-sm font-medium mt-3">Highlights</div>
              <ul className="list-disc pl-5 text-sm opacity-80">
                {u.result?.highlights.map((h, idx) => (
                  <li key={idx}>{h}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function EmptyState() {
  return (
    <div className="grid gap-3">
      <div className="rounded-md border border-black/10 dark:border-white/10 p-3">
        <div className="text-sm font-medium">Summary</div>
        <p className="text-sm opacity-80 mt-1">
          Upload files to generate summaries here.
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
  );
}
