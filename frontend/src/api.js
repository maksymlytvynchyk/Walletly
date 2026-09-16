const API_ROOT = "/api/v1";
const storageKey = "finance-token";

export const savedToken = () => localStorage.getItem(storageKey);
export const saveToken = (token) => localStorage.setItem(storageKey, token);
export const clearToken = () => localStorage.removeItem(storageKey);

export async function api(path, options = {}) {
  const headers = new Headers(options.headers);
  const token = savedToken();

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  if (options.body) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_ROOT}${path}`, {
    ...options,
    headers,
  });

  const body = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = body?.detail;

    let message = "Не вдалося виконати запит.";

    if (Array.isArray(detail)) {
      message = detail.map((item) => item.msg).join(", ");
    } else if (typeof detail === "object" && detail !== null) {
      message = detail.message || message;
    } else if (typeof detail === "string") {
      message = detail;
    }

    const error = new Error(message);

    error.details = Array.isArray(detail) ? detail : [];
    error.field =
      typeof detail === "object" && detail !== null ? detail.field : null;
    error.code =
      typeof detail === "object" && detail !== null ? detail.code : null;

    throw error;
  }
  return body;
}

export const money = (value, currency = "uah") =>
  new Intl.NumberFormat("uk-UA", {
    style: "currency",
    currency: currency.toUpperCase(),
    maximumFractionDigits: 2,
  }).format(Number(value));
