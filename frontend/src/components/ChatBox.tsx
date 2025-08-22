"use client";

import { useState } from "react";
import { useAskQuestion } from "../api/hooks";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [isSending, setIsSending] = useState(false);

  const ask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsSending(true);
    // TODO: wire to backend
    await new Promise((r) => setTimeout(r, 600));
    setIsSending(false);
  };

  return (
    <section className="rounded-lg border border-black/10 dark:border-white/10 bg-white/60 dark:bg-black/30 p-4">
      <div className="mb-3">
        <h2 className="text-base font-semibold">Ask about your documents</h2>
        <p className="text-sm opacity-70">
          Summaries, clauses, risks, obligations, dates, parties, etc.
        </p>
      </div>

      <form onSubmit={ask} className="flex flex-col gap-2">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Summarize key risks and payment terms across uploaded contracts"
          className="min-h-[96px] resize-y rounded-md border border-black/10 dark:border-white/10 bg-transparent px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black/20 dark:focus:ring-white/20"
        />
        <div className="flex items-center justify-between">
          <div className="text-[11px] opacity-60">
            Press Enter to send, Shift+Enter for newline
          </div>
          <button
            type="submit"
            disabled={isSending}
            className="px-3 py-1.5 rounded-md bg-black text-white text-sm disabled:opacity-50"
          >
            {isSending ? "Sending..." : "Ask"}
          </button>
        </div>
      </form>
    </section>
  );
}
