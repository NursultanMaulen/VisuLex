"use client";

import { useMemo, useRef } from "react";
import { useUploads, formatFileSize } from "../app/UploadsContext";

export default function UploadArea() {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { uploads, addFiles, removeUpload, clearUploads } = useUploads();
  const hasUploads = uploads.length > 0;
  const totalSize = useMemo(
    () => uploads.reduce((acc, u) => acc + u.sizeBytes, 0),
    [uploads]
  );

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
        onDragOver={(e) => {
          e.preventDefault();
          e.dataTransfer.dropEffect = "copy";
        }}
        onDrop={(e) => {
          e.preventDefault();
          addFiles(e.dataTransfer.files);
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.mp4,.mov"
          className="hidden"
          multiple
          onChange={(e) => addFiles(e.target.files)}
        />
        <div className="text-sm">
          Drag & drop files here, or
          <span className="mx-1 px-2 py-1 rounded bg-black/90 text-white text-xs">
            Browse
          </span>
        </div>
        <div className="text-[11px] opacity-60 mt-1">Max 50MB per file</div>
      </div>

      {hasUploads && (
        <div className="mt-4">
          <div className="text-xs uppercase tracking-wide opacity-60 mb-2">
            Selected ({uploads.length}) • Total {formatFileSize(totalSize)}
          </div>
          <ul className="space-y-2">
            {uploads.map((u) => (
              <li
                key={u.id}
                className="text-sm px-2 py-2 rounded border border-black/10 dark:border-white/10 flex items-center gap-3"
              >
                <Thumbnail itemId={u.id} />
                <div className="min-w-0 flex-1">
                  <div className="truncate">{u.file.name}</div>
                  <div className="text-[11px] opacity-60">
                    {formatFileSize(u.sizeBytes)} • {u.kind.toUpperCase()} •{" "}
                    {u.status === "processing"
                      ? "Processing…"
                      : u.status === "done"
                      ? "Processed"
                      : u.status}
                  </div>
                </div>
                <button
                  className="text-xs px-2 py-1 rounded border border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/10"
                  onClick={() => removeUpload(u.id)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <div className="mt-2 flex gap-2">
            <button
              className="text-xs px-2 py-1 rounded border border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/10"
              onClick={() => inputRef.current?.click()}
            >
              Add more
            </button>
            <button
              className="text-xs px-2 py-1 rounded border border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/10"
              onClick={clearUploads}
            >
              Clear all
            </button>
          </div>
        </div>
      )}
    </section>
  );
}

function Thumbnail({ itemId }: { itemId: string }) {
  const { uploads } = useUploads();
  const item = uploads.find((u) => u.id === itemId);
  if (!item) return null;
  const base =
    "w-10 h-10 rounded border border-black/10 dark:border-white/10 flex items-center justify-center text-[10px] overflow-hidden bg-white/50 dark:bg-black/20";
  if (item.kind === "image" && item.objectUrl) {
    return (
      <div className={base}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={item.objectUrl}
          alt="preview"
          className="w-full h-full object-cover"
        />
      </div>
    );
  }
  if (item.kind === "video" && item.objectUrl) {
    return (
      <div className={base}>
        <video
          src={item.objectUrl}
          className="w-full h-full object-cover"
          muted
          playsInline
        />
      </div>
    );
  }
  if (item.kind === "pdf") {
    return <div className={base}>PDF</div>;
  }
  return <div className={base}>FILE</div>;
}
