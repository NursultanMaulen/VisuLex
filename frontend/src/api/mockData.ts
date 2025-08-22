// Мок-данные для API

import { UploadResponse, AskResponse, HistoryResponse } from "./types";

export const mockUploadResponse: UploadResponse = {
  success: true,
  documentId: "doc_123",
  filename: "sample_document.pdf",
  message: "Документ успешно загружен и обработан",
};

export const mockAskResponse: AskResponse = {
  success: true,
  answer:
    "Это мок-ответ на ваш вопрос. В реальном приложении здесь будет ответ от Hugging Face модели.",
  sources: ["sample_document.pdf - стр. 1-3"],
};

export const mockHistoryResponse: HistoryResponse = {
  success: true,
  documents: [
    {
      id: "doc_123",
      filename: "sample_document.pdf",
      uploadDate: "2024-01-15T10:30:00Z",
      summary: "Документ содержит информацию о...",
      status: "processed",
    },
    {
      id: "doc_124",
      filename: "another_document.docx",
      uploadDate: "2024-01-14T15:45:00Z",
      summary: "Документ описывает процесс...",
      status: "processed",
    },
    {
      id: "doc_125",
      filename: "large_file.pdf",
      uploadDate: "2024-01-15T11:00:00Z",
      summary: "",
      status: "processing",
    },
  ],
};

// Функция для имитации задержки сети
export const simulateNetworkDelay = (ms: number = 1000): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
