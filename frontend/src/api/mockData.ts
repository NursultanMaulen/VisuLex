// Мок-данные для API

import { UploadResponse, AskResponse, HistoryResponse } from "./types";

export const mockUploadResponse: UploadResponse = {
  doc_id: "doc_123",
  summary: "Документ успешно загружен и обработан",
};

export const mockAskResponse: AskResponse = {
  doc_id: "doc_123",
  question: "Что содержится в документе?",
  answer:
    "Это мок-ответ на ваш вопрос. В реальном приложении здесь будет ответ от Hugging Face модели.",
};

export const mockHistoryResponse: HistoryResponse = {
  doc_123: {
    filename: "sample_document.pdf",
    summary: "Документ содержит информацию о...",
  },
  doc_124: {
    filename: "another_document.docx",
    summary: "Документ описывает процесс...",
  },
  doc_125: {
    filename: "large_file.pdf",
    summary: "Документ в процессе обработки...",
  },
};

// Функция для имитации задержки сети
export const simulateNetworkDelay = (ms: number = 1000): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
