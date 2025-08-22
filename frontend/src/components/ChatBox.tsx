"use client";

import { useState } from "react";
import { useAskQuestion } from "../api/hooks";
import { useUploads } from "../app/UploadsContext";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const { uploads } = useUploads();
  const { askQuestion, loading, error } = useAskQuestion();

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Проверяем, есть ли загруженные файлы
    if (uploads.length === 0) {
      alert("Сначала загрузите документ!");
      return;
    }

    try {
      // Берем первый загруженный файл (можно улучшить логику выбора)
      const firstUpload = uploads[0];
      if (!firstUpload.id) {
        alert("Документ еще не обработан!");
        return;
      }

      const response = await askQuestion({
        doc_id: firstUpload.id,
        question: query.trim(),
      });

      console.log("Ответ от API:", response);
      setQuery(""); // Очищаем поле после успешной отправки
    } catch (err) {
      console.error("Ошибка при отправке вопроса:", err);
      alert("Ошибка при отправке вопроса. Проверьте консоль для деталей.");
    }
  };

  return (
    <section className="rounded-lg border border-black/10 dark:border-white/10 bg-white/60 dark:bg-black/30 p-4">
      <div className="mb-3">
        <h2 className="text-base font-semibold">Ask about your documents</h2>
        <p className="text-sm opacity-70">
          Summaries, clauses, risks, obligations, dates, parties, etc.
        </p>
        {uploads.length === 0 && (
          <p className="text-xs text-red-500 mt-1">
            ⚠️ Сначала загрузите документ
          </p>
        )}
      </div>

      <form onSubmit={handleAsk} className="flex flex-col gap-2">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Summarize key risks and payment terms across uploaded contracts"
          className="min-h-[96px] resize-y rounded-md border border-black/10 dark:border-white/10 bg-transparent px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black/20 dark:focus:ring-white/20"
          disabled={uploads.length === 0}
        />
        <div className="flex items-center justify-between">
          <div className="text-[11px] opacity-60">
            Press Enter to send, Shift+Enter for newline
          </div>
          <button
            type="submit"
            disabled={loading || uploads.length === 0}
            className="px-3 py-1.5 rounded-md bg-black text-white text-sm disabled:opacity-50"
          >
            {loading ? "Sending..." : "Ask"}
          </button>
        </div>
        {error && (
          <div className="text-xs text-red-500 mt-2">Ошибка: {error}</div>
        )}
      </form>
    </section>
  );
}
