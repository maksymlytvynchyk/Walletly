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
    const detail = Array.isArray(body?.detail)
      ? body.detail.map((item) => item.msg).join(", ")
      : body?.detail;

    throw new Error(detail || "Не вдалося виконати запит.");
  }
  return body;
}

export const money = (value, currency = "uah") =>
  new Intl.NumberFormat("uk-UA", {
    style: "currency",
    currency: currency.toUpperCase(),
    maximumFractionDigits: 2,
  }).format(Number(value));
