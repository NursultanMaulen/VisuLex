// API клиент для подключения к бэкенду

import {
  UploadResponse,
  AskRequest,
  AskResponse,
  HistoryResponse,
  ApiError,
} from "./types";
import {
  mockUploadResponse,
  mockAskResponse,
  mockHistoryResponse,
  simulateNetworkDelay,
} from "./mockData";

// Конфигурация API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === "true" || false; // По умолчанию используем реальный API

// Утилита для обработки ошибок
const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const error: ApiError = {
      message: `HTTP error! status: ${response.status}`,
      status: response.status,
    };
    throw error;
  }
  return response.json();
};

// Утилита для создания заголовков
const createHeaders = (): HeadersInit => ({
  "Content-Type": "application/json",
});

// API клиент
export class ApiClient {
  // Загрузка файла
  static async uploadFile(file: File): Promise<UploadResponse> {
    if (USE_MOCK) {
      await simulateNetworkDelay();
      return mockUploadResponse;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    return handleResponse<UploadResponse>(response);
  }

  // Отправка вопроса
  static async askQuestion(request: AskRequest): Promise<AskResponse> {
    if (USE_MOCK) {
      await simulateNetworkDelay();
      return {
        ...mockAskResponse,
        doc_id: request.doc_id,
        question: request.question,
      };
    }

    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: createHeaders(),
      body: JSON.stringify(request),
    });

    return handleResponse<AskResponse>(response);
  }

  // Получение истории документов
  static async getHistory(): Promise<HistoryResponse> {
    if (USE_MOCK) {
      await simulateNetworkDelay();
      return mockHistoryResponse;
    }

    const response = await fetch(`${API_BASE_URL}/history`, {
      method: "GET",
      headers: createHeaders(),
    });

    return handleResponse<HistoryResponse>(response);
  }

  // Проверка состояния API
  static async healthCheck(): Promise<boolean> {
    if (USE_MOCK) {
      return true;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: "GET",
      });
      return response.ok;
    } catch {
      return false;
    }
  }
}

// Экспорт для удобства использования
export default ApiClient;
