// React хуки для работы с API

import { useState, useCallback } from "react";
import ApiClient from "./client";
import {
  UploadResponse,
  AskRequest,
  AskResponse,
  HistoryResponse,
  ApiError,
} from "./types";

// Хук для загрузки файлов
export const useFileUpload = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<UploadResponse | null>(null);

  const uploadFile = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);

    try {
      const result = await ApiClient.uploadFile(file);
      setData(result);
      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Произошла ошибка при загрузке файла";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
  }, []);

  return {
    uploadFile,
    loading,
    error,
    data,
    reset,
  };
};

// Хук для отправки вопросов
export const useAskQuestion = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<AskResponse | null>(null);

  const askQuestion = useCallback(async (request: AskRequest) => {
    setLoading(true);
    setError(null);

    try {
      const result = await ApiClient.askQuestion(request);
      setData(result);
      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Произошла ошибка при отправке вопроса";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
  }, []);

  return {
    askQuestion,
    loading,
    error,
    data,
    reset,
  };
};

// Хук для получения истории
export const useHistory = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<HistoryResponse | null>(null);

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await ApiClient.getHistory();
      setData(result);
      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Произошла ошибка при получении истории";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
  }, []);

  return {
    fetchHistory,
    loading,
    error,
    data,
    reset,
  };
};

// Хук для проверки состояния API
export const useApiHealth = () => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(false);

  const checkHealth = useCallback(async () => {
    setLoading(true);
    try {
      const healthy = await ApiClient.healthCheck();
      setIsHealthy(healthy);
      return healthy;
    } catch {
      setIsHealthy(false);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    checkHealth,
    isHealthy,
    loading,
  };
};
