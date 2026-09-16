import { computed, ref } from "vue";
import { api, clearToken, savedToken, saveToken } from "../api";

export function useFinance() {
  const user = ref(null);
  const authenticated = ref(false);
  const loading = ref(false);
  const initializing = ref(true);

  const notice = ref("");
  const error = ref("");

  const cards = ref([]);
  const operations = ref([]);

  // Balances for each currency
  const balances = computed(() => ({
    UAH: cards.value
      .filter((card) => card.currency === "uah")
      .reduce((sum, card) => sum + Number(card.balance), 0),

    USD: cards.value
      .filter((card) => card.currency === "usd")
      .reduce((sum, card) => sum + Number(card.balance), 0),

    EUR: cards.value
      .filter((card) => card.currency === "eur")
      .reduce((sum, card) => sum + Number(card.balance), 0),
  }));

  // Show message or error for 4 seconds
  function message(text, isError = false) {
    notice.value = isError ? "" : text;
    error.value = isError ? text : "";

    setTimeout(() => {
      notice.value = "";
      error.value = "";
    }, 10000);
  }

  // Load cards and operations
  async function loadDashboard() {
    loading.value = true;

    try {
      const [cardData, operationData] = await Promise.all([
        api("/cards"),
        api("/operations"),
      ]);

      cards.value = cardData;
      operations.value = operationData;
    } catch (exception) {
      message(exception.message, true);
    } finally {
      loading.value = false;
    }
  }

  function getFieldErrors(exception) {
    // 401 / 409: detail = { field, code }
    if (exception.field && exception.code) {
      return {
        [exception.field]: exception.code,
      };
    }

    // 422: detail = [{ type, loc, msg }]
    const fieldErrors = {};

    for (const error of exception.details || []) {
      const field = error.loc?.at(-1);

      if (field) {
        fieldErrors[field] = error.type;
      }
    }

    return fieldErrors;
  }

  // Authentication
  async function signIn(phone, password) {
    phone = phone.trim();

    if (!phone) {
      return {
        success: false,
        fieldErrors: {
          phone: "phone_required",
        },
      };
    }

    if (!password) {
      return {
        success: false,
        fieldErrors: {
          password: "password_required",
        },
      };
    }

    loading.value = true;

    try {
      const data = await api("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          phone,
          password,
        }),
      });

      saveToken(data.access_token);

      user.value = data.user;
      authenticated.value = true;

      await loadDashboard();

      message("Ви успішно увійшли.");

      return {
        success: true,
        fieldErrors: {},
      };
    } catch (exception) {
      clearToken();

      user.value = null;
      authenticated.value = false;

      const fieldErrors = getFieldErrors(exception);

      if (Object.keys(fieldErrors).length) {
        return {
          success: false,
          fieldErrors,
        };
      }

      message(exception.message, true);

      return {
        success: false,
        fieldErrors: {},
      };
    } finally {
      loading.value = false;
    }
  }

  // Registration
  async function register(payload) {
    loading.value = true;

    try {
      await api("/users", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      message("Користувача успішно створено.");

      // return true;
      return {
        success: true,
        fieldErrors: {},
      };
    } catch (exception) {
      const fieldErrors = getFieldErrors(exception);

      if (Object.keys(fieldErrors).length) {
        return {
          success: false,
          fieldErrors,
        };
      }

      message(exception.message, true);

      return {
        success: false,
        fieldErrors: {},
      };
    } finally {
      loading.value = false;
    }
  }

  // Restore session from saved token
  async function restoreSession() {
    const token = savedToken();

    if (!token) {
      initializing.value = false;
      return false;
    }

    loading.value = true;

    try {
      const currentUser = await api("/users/me");

      user.value = currentUser;
      authenticated.value = true;

      await loadDashboard();

      return true;
    } catch (exception) {
      clearToken();

      user.value = null;
      authenticated.value = false;

      return false;
    } finally {
      loading.value = false;
      initializing.value = false;
    }
  }

  // Create card
  async function createCard(payload) {
    try {
      await api("/cards", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      message("Картку створено.");

      await loadDashboard();

      return {
        success: true,
        fieldErrors: {},
      };
    } catch (exception) {
      const fieldErrors = getFieldErrors(exception);

      if (Object.keys(fieldErrors).length) {
        return {
          success: false,
          fieldErrors,
        };
      }

      message(exception.message, true);
      return {
        success: false,
        fieldErrors: {},
      };
    }
  }

  // Create regular operation
  async function createOperation(payload) {
    try {
      await api("/operation", {
        method: "POST",
        body: JSON.stringify({
          card_id: Number(payload.card_id),
          type: payload.type,
          amount: payload.amount,
          currency: payload.currency,
          category: payload.category || null,
          subcategory: payload.subcategory || null,
        }),
      });

      message("Операцію додано.");

      await loadDashboard();

      return {
        success: true,
        fieldErrors: {},
      };
    } catch (exception) {
      const fieldErrors = getFieldErrors(exception);

      if (Object.keys(fieldErrors).length) {
        return {
          success: false,
          fieldErrors,
        };
      }
      message(exception.message, true);

      return {
        success: false,
        fieldErrors: {},
      };
    }
  }

  // Transfer between cards
  async function transfer(payload) {
    const fromCardId = Number(payload.from_card_id);
    const toCardId = Number(payload.to_card_id);
    if (fromCardId === toCardId) {
      return message("Оберіть різні картки.", true);
    }
    try {
      await api("/operation/transfer", {
        method: "POST",
        body: JSON.stringify({
          from_card_id: fromCardId,
          to_card_id: toCardId,
          amount: payload.amount,
          currency: payload.currency,
        }),
      });

      message("Переказ виконано.");

      await loadDashboard();

      return {
        success: true,
        fieldErrors: {},
      };
    } catch (exception) {
      const fieldErrors = getFieldErrors(exception);

      if (Object.keys(fieldErrors).length) {
        return {
          success: false,
          fieldErrors,
        };
      }
      message(exception.message, true);

      return {
        success: false,
        fieldErrors: {},
      };
    }
  }

  // End session
  function logout() {
    clearToken();

    user.value = null;
    authenticated.value = false;

    cards.value = [];
    operations.value = [];
  }

  return {
    user,
    authenticated,
    loading,
    initializing,

    notice,
    error,

    cards,
    operations,
    balances,

    loadDashboard,

    signIn,
    register,
    restoreSession,

    createCard,
    createOperation,
    transfer,

    logout,
  };
}
