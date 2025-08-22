# API Клиент для VisuLex

Этот модуль предоставляет API клиент для подключения к бэкенду VisuLex.

## Структура

```
src/api/
├── types.ts          # TypeScript типы для API
├── client.ts         # Основной API клиент
├── hooks.ts          # React хуки для работы с API
├── mockData.ts       # Мок-данные для разработки
└── index.ts          # Экспорт всех модулей
```

## Использование

### 1. Импорт API клиента

```typescript
import { ApiClient } from "@/api";
// или
import ApiClient from "@/api/client";
```

### 2. Использование React хуков

```typescript
import { useFileUpload, useAskQuestion, useHistory } from "@/api";

function MyComponent() {
  const { uploadFile, loading, error, data } = useFileUpload();
  const { askQuestion, loading: askLoading } = useAskQuestion();
  const { fetchHistory, data: historyData } = useHistory();

  // Загрузка файла
  const handleFileUpload = async (file: File) => {
    try {
      const result = await uploadFile(file);
      console.log("Файл загружен:", result);
    } catch (err) {
      console.error("Ошибка загрузки:", err);
    }
  };

  // Отправка вопроса
  const handleAsk = async (question: string, documentId: string) => {
    try {
      const result = await askQuestion({ question, documentId });
      console.log("Ответ:", result);
    } catch (err) {
      console.error("Ошибка:", err);
    }
  };

  // Получение истории
  const handleGetHistory = async () => {
    try {
      await fetchHistory();
    } catch (err) {
      console.error("Ошибка получения истории:", err);
    }
  };

  return <div>{/* Ваш UI */}</div>;
}
```

### 3. Прямое использование API клиента

```typescript
import ApiClient from "@/api/client";

// Загрузка файла
const uploadResult = await ApiClient.uploadFile(file);

// Отправка вопроса
const answer = await ApiClient.askQuestion({
  question: "Что содержится в документе?",
  documentId: "doc_123",
});

// Получение истории
const history = await ApiClient.getHistory();

// Проверка состояния API
const isHealthy = await ApiClient.healthCheck();
```

## Конфигурация

Создайте файл `.env.local` на основе `env.example`:

```bash
# URL бэкенда
NEXT_PUBLIC_API_URL=http://localhost:8000

# Использовать мок-данные (true для разработки)
NEXT_PUBLIC_USE_MOCK=true
```

## Эндпоинты

### POST /upload

Загрузка файла для обработки Hugging Face моделью.

**Параметры:**

- `file`: File - загружаемый файл

**Ответ:**

```typescript
{
  success: boolean;
  documentId: string;
  filename: string;
  message: string;
}
```

### POST /ask

Отправка вопроса с ссылкой на документ.

**Параметры:**

```typescript
{
  question: string;
  documentId: string;
}
```

**Ответ:**

```typescript
{
  success: boolean;
  answer: string;
  sources: string[];
}
```

### GET /history

Получение списка ранее обработанных документов.

**Ответ:**

```typescript
{
  success: boolean;
  documents: DocumentHistory[];
}
```

### GET /health

Проверка состояния API.

**Ответ:** HTTP 200 OK или ошибка

## Мок-данные

В режиме разработки API клиент использует мок-данные для имитации работы бэкенда. Это позволяет:

- Разрабатывать фронтенд без запущенного бэкенда
- Тестировать различные сценарии
- Имитировать задержки сети

Для отключения мок-данных установите `NEXT_PUBLIC_USE_MOCK=false`.

## Обработка ошибок

API клиент автоматически обрабатывает HTTP ошибки и возвращает структурированные ошибки:

```typescript
try {
  const result = await ApiClient.uploadFile(file);
} catch (error) {
  if (error.status === 413) {
    console.error("Файл слишком большой");
  } else if (error.status === 500) {
    console.error("Ошибка сервера");
  }
}
```

## Переход на реальный бэкенд

Когда будет готов FastAPI бэкенд:

1. Установите `NEXT_PUBLIC_USE_MOCK=false`
2. Убедитесь, что `NEXT_PUBLIC_API_URL` указывает на правильный адрес
3. Проверьте, что все эндпоинты соответствуют спецификации
4. Протестируйте интеграцию

## Типы TypeScript

Все API типы экспортируются из `@/api/types`:

```typescript
import {
  UploadResponse,
  AskRequest,
  AskResponse,
  HistoryResponse,
  ApiError,
} from "@/api/types";
```
