// Типы для API

export interface UploadResponse {
  success: boolean;
  documentId: string;
  filename: string;
  message: string;
}

export interface AskRequest {
  question: string;
  documentId: string;
}

export interface AskResponse {
  success: boolean;
  answer: string;
  sources: string[];
}

export interface DocumentHistory {
  id: string;
  filename: string;
  uploadDate: string;
  summary: string;
  status: "processed" | "processing" | "error";
}

export interface HistoryResponse {
  success: boolean;
  documents: DocumentHistory[];
}

export interface ApiError {
  message: string;
  status: number;
}
