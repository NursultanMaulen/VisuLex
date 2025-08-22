// Типы для API

export interface UploadResponse {
  doc_id: string;
  summary: string;
}

export interface AskRequest {
  doc_id: string;
  question: string;
}

export interface AskResponse {
  doc_id: string;
  question: string;
  answer: string;
}

export interface DocumentHistory {
  filename: string;
  summary: string;
}

export interface HistoryResponse {
  [doc_id: string]: DocumentHistory;
}

export interface ApiError {
  message: string;
  status: number;
}
