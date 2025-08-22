"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

type RiskLevel = "Low" | "Medium" | "High";
type UploadKind = "pdf" | "image" | "video" | "other";

export type UploadResult = {
  summary: string;
  highlights: string[];
  risk: RiskLevel;
  risksExtracted: string[];
};

export type UploadItem = {
  id: string;
  file: File;
  objectUrl?: string;
  kind: UploadKind;
  sizeBytes: number;
  status: "queued" | "processing" | "done" | "error";
  result?: UploadResult;
  errorMessage?: string;
};

type UploadsContextValue = {
  uploads: UploadItem[];
  addFiles: (files: File[] | FileList | null) => void;
  removeUpload: (id: string) => void;
  clearUploads: () => void;
  askOnUpload: (id: string, question: string) => void;
};

const UploadsContext = createContext<UploadsContextValue | null>(null);

export function UploadsProvider({ children }: { children: React.ReactNode }) {
  const [uploads, setUploads] = useState<UploadItem[]>([]);
  const objectUrlsRef = useRef<Map<string, string>>(new Map());

  const detectKind = (file: File): UploadKind => {
    const type = file.type;
    if (type.startsWith("image/")) return "image";
    if (type.startsWith("video/")) return "video";
    if (type === "application/pdf") return "pdf";
    return "other";
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(i === 0 ? 0 : 2)} ${sizes[i]}`;
  };

  const pickRisk = (item: UploadItem): RiskLevel => {
    const hash =
      [...item.file.name].reduce((a, c) => a + c.charCodeAt(0), 0) +
      item.sizeBytes;
    const mod = hash % 3;
    return mod === 0 ? "Low" : mod === 1 ? "Medium" : "High";
  };

  const mockGenerateResult = (
    item: UploadItem,
    question?: string
  ): UploadResult => {
    const readableSize = formatBytes(item.sizeBytes);
    if (item.kind === "pdf") {
      return {
        summary: `PDF "${item.file.name}" (${readableSize}) processed${
          question ? ` for question: "${question}"` : ""
        }. Found several key sections and dates.`,
        highlights: [
          "Parties identified",
          "Effective date detected",
          "Payment terms extracted",
        ],
        risk: pickRisk(item),
        risksExtracted: [
          "Late payment penalties",
          "Auto-renewal clause",
          "Confidentiality breach conditions",
        ],
      };
    }
    if (item.kind === "image") {
      return {
        summary: `Image "${item.file.name}" analyzed${
          question ? ` for: "${question}"` : ""
        }. Text and visual elements detected.`,
        highlights: [
          "OCR text extracted",
          "Logos found",
          "Signature-like region",
        ],
        risk: pickRisk(item),
        risksExtracted: ["Illegible signature", "Mismatch of dates"],
      };
    }
    if (item.kind === "video") {
      return {
        summary: `Video "${item.file.name}" transcribed${
          question ? ` and searched for: "${question}"` : ""
        }. Key moments detected.`,
        highlights: [
          "Speaker segments",
          "Mentions of obligations",
          "Compliance keywords",
        ],
        risk: pickRisk(item),
        risksExtracted: [
          "Compliance risk: missing disclosure",
          "Ambiguous commitment wording",
        ],
      };
    }
    return {
      summary: `"${item.file.name}" processed${
        question ? ` for: "${question}"` : ""
      }.`,
      highlights: ["Content indexed"],
      risk: pickRisk(item),
      risksExtracted: ["General risk placeholder"],
    };
  };

  const addFiles = useCallback((input: File[] | FileList | null) => {
    if (!input) return;
    const arr = Array.from(input);
    const newItems: UploadItem[] = arr.map((file) => {
      const id = cryptoRandomId();
      const objectUrl = URL.createObjectURL(file);
      objectUrlsRef.current.set(id, objectUrl);
      return {
        id,
        file,
        objectUrl,
        kind: detectKind(file),
        sizeBytes: file.size,
        status: "processing",
      };
    });
    setUploads((prev) => [...prev, ...newItems]);
    newItems.forEach((item) => {
      const delay = 800 + Math.floor(Math.random() * 1200);
      window.setTimeout(() => {
        setUploads((prev) =>
          prev.map((u) =>
            u.id === item.id
              ? { ...u, status: "done", result: mockGenerateResult(u) }
              : u
          )
        );
      }, delay);
    });
  }, []);

  const askOnUpload = useCallback((id: string, question: string) => {
    setUploads((prev) =>
      prev.map((u) => (u.id === id ? { ...u, status: "processing" } : u))
    );
    const delay = 700 + Math.floor(Math.random() * 1200);
    window.setTimeout(() => {
      setUploads((prev) =>
        prev.map((u) =>
          u.id === id
            ? { ...u, status: "done", result: mockGenerateResult(u, question) }
            : u
        )
      );
    }, delay);
  }, []);

  const removeUpload = useCallback((id: string) => {
    setUploads((prev) => prev.filter((u) => u.id !== id));
    const url = objectUrlsRef.current.get(id);
    if (url) {
      URL.revokeObjectURL(url);
      objectUrlsRef.current.delete(id);
    }
  }, []);

  const clearUploads = useCallback(() => {
    setUploads([]);
    objectUrlsRef.current.forEach((url) => URL.revokeObjectURL(url));
    objectUrlsRef.current.clear();
  }, []);

  useEffect(() => {
    return () => {
      objectUrlsRef.current.forEach((url) => URL.revokeObjectURL(url));
      objectUrlsRef.current.clear();
    };
  }, []);

  const value = useMemo(
    () => ({ uploads, addFiles, removeUpload, clearUploads, askOnUpload }),
    [uploads, addFiles, removeUpload, clearUploads, askOnUpload]
  );

  return (
    <UploadsContext.Provider value={value}>{children}</UploadsContext.Provider>
  );
}

export function useUploads() {
  const ctx = useContext(UploadsContext);
  if (!ctx) throw new Error("useUploads must be used within UploadsProvider");
  return ctx;
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(i === 0 ? 0 : 2)} ${sizes[i]}`;
}

function cryptoRandomId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return (crypto as Crypto & { randomUUID?: () => string }).randomUUID!();
  }
  return Math.random().toString(36).slice(2);
}
