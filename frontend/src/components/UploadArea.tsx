"use client";

import { useRef, useState } from "react";

export default function UploadArea() {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [files, setFiles] = useState<File[]>([]);

  const onFiles = (list: FileList | null) => {
    if (!list) return;
    const arr = Array.from(list);
    setFiles(arr);
  };

  return (
    <section className="rounded-lg border border-black/10 dark:border-white/10 bg-white/60 dark:bg-black/30 p-4">
      <div className="mb-3">
        <h2 className="text-base font-semibold">Upload documents</h2>
        <p className="text-sm opacity-70">
          Contracts, PDFs, images, or short videos.
        </p>
      </div>

      <div
        className="border-2 border-dashed rounded-lg p-6 text-center hover:bg-black/[0.02] dark:hover:bg-white/[0.04] transition"
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.mp4,.mov"
          className="hidden"
          multiple
          onChange={(e) => onFiles(e.target.files)}
        />
        <div className="text-sm">
          Drag & drop files here, or
          <span className="mx-1 px-2 py-1 rounded bg-black/90 text-white text-xs">
            Browse
          </span>
        </div>
        <div className="text-[11px] opacity-60 mt-1">Max 50MB per file</div>
      </div>

      {files.length > 0 && (
        <div className="mt-4">
          <div className="text-xs uppercase tracking-wide opacity-60 mb-2">
            Selected
          </div>
          <ul className="space-y-1">
            {files.map((f, i) => (
              <li
                key={i}
                className="text-sm px-2 py-1 rounded border border-black/10 dark:border-white/10"
              >
                {f.name}{" "}
                <span className="opacity-60 text-xs">
                  ({(f.size / (1024 * 1024)).toFixed(2)} MB)
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
