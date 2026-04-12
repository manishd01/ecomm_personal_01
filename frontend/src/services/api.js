// API Client utility for making requests to microservices
import { API_BASE_URLS } from "../config/apiConfig";

/**
 * Generic API request handler with error handling
 * @param {string} url - API endpoint URL
 * @param {object} options - fetch options
 * @returns {Promise} - Response data or error
 */
export const apiRequest = async (url, options = {}) => {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  };
  console.log("API Request URL:---", url);
  try {
    const response = await fetch(url, defaultOptions);

    if (!response.ok) {
      throw new Error(
        `HTTP Error: ${response.status} - ${response.statusText}`,
      );
    }

    const data = await response.json();
    console.log("data----------:", data);
    return { success: true, data };
  } catch (error) {
    console.error("API Request Error:", error);
    return { success: false, error: error.message };
  }
};

// Order Service API calls
export const orderAPI = {
  getAll: () => apiRequest(`${API_BASE_URLS.ORDERS}/orders`),
  getById: (id) => apiRequest(`${API_BASE_URLS.ORDERS}/orders/${id}`),
  create: (orderData) =>
    apiRequest(`${API_BASE_URLS.ORDERS}/orders`, {
      method: "POST",
      body: JSON.stringify(orderData),
    }),
  update: (id, orderData) =>
    apiRequest(`${API_BASE_URLS.ORDERS}/orders/${id}`, {
      method: "PUT",
      body: JSON.stringify(orderData),
    }),
  delete: (id) =>
    apiRequest(`${API_BASE_URLS.ORDERS}/orders/${id}`, {
      method: "DELETE",
    }),
};

// Inventory Service API calls
export const inventoryAPI = {
  getAll: async () => {
    const url = `${API_BASE_URLS.INVENTORY}/inventory`;
    console.log("Inventory API URL:", url); // 👈 DEBUG
    const response = await apiRequest(url); // ✅ wait
    console.log("Inventory API Response:", response);

    return response;
  },
  getById: (id) => apiRequest(`${API_BASE_URLS.INVENTORY}/inventory/${id}`),
  create: (itemData) =>
    apiRequest(`${API_BASE_URLS.INVENTORY}/inventory`, {
      method: "POST",
      body: JSON.stringify(itemData),
    }),
  update: (id, itemData) =>
    apiRequest(`${API_BASE_URLS.INVENTORY}/inventory/${id}`, {
      method: "PUT",
      body: JSON.stringify(itemData),
    }),
  delete: (id) =>
    apiRequest(`${API_BASE_URLS.INVENTORY}/inventory/${id}`, {
      method: "DELETE",
    }),
};

// Customer Service API calls
export const customerAPI = {
  getAll: () => apiRequest(`${API_BASE_URLS.CUSTOMERS}/customers`),
  getById: (id) => apiRequest(`${API_BASE_URLS.CUSTOMERS}/customers/${id}`),
  getByEmail: (email) =>
    apiRequest(`${API_BASE_URLS.CUSTOMERS}/customers/email/${email}`),
  create: (customerData) =>
    apiRequest(`${API_BASE_URLS.CUSTOMERS}/customers`, {
      method: "POST",
      body: JSON.stringify(customerData),
    }),
  update: (id, customerData) =>
    apiRequest(`${API_BASE_URLS.CUSTOMERS}/customers/${id}`, {
      method: "PUT",
      body: JSON.stringify(customerData),
    }),
  delete: (id) =>
    apiRequest(`${API_BASE_URLS.CUSTOMERS}/customers/${id}`, {
      method: "DELETE",
    }),
};

// Payment Service API calls
export const paymentAPI = {
  getAll: () => apiRequest(`${API_BASE_URLS.PAYMENTS}/payments`),
  getById: (id) => apiRequest(`${API_BASE_URLS.PAYMENTS}/payments/${id}`),
  getByOrder: (orderId) =>
    apiRequest(`${API_BASE_URLS.PAYMENTS}/payments/order/${orderId}`),
  create: (paymentData) =>
    apiRequest(`${API_BASE_URLS.PAYMENTS}/payments`, {
      method: "POST",
      body: JSON.stringify(paymentData),
    }),
  update: (id, paymentData) =>
    apiRequest(`${API_BASE_URLS.PAYMENTS}/payments/${id}`, {
      method: "PUT",
      body: JSON.stringify(paymentData),
    }),
  delete: (id) =>
    apiRequest(`${API_BASE_URLS.PAYMENTS}/payments/${id}`, {
      method: "DELETE",
    }),
};

// Notification Service API calls
export const notificationAPI = {
  getAll: () => apiRequest(`${API_BASE_URLS.NOTIFICATIONS}/notifications`),
  getById: (id) =>
    apiRequest(`${API_BASE_URLS.NOTIFICATIONS}/notifications/${id}`),
  getCustomerNotifications: (customerId) =>
    apiRequest(
      `${API_BASE_URLS.NOTIFICATIONS}/notifications/customer/${customerId}`,
    ),
  getUnreadNotifications: (customerId) =>
    apiRequest(
      `${API_BASE_URLS.NOTIFICATIONS}/notifications/customer/${customerId}/unread`,
    ),
  create: (notificationData) =>
    apiRequest(`${API_BASE_URLS.NOTIFICATIONS}/notifications`, {
      method: "POST",
      body: JSON.stringify(notificationData),
    }),
  update: (id, notificationData) =>
    apiRequest(`${API_BASE_URLS.NOTIFICATIONS}/notifications/${id}`, {
      method: "PUT",
      body: JSON.stringify(notificationData),
    }),
  delete: (id) =>
    apiRequest(`${API_BASE_URLS.NOTIFICATIONS}/notifications/${id}`, {
      method: "DELETE",
    }),
};

export const shippingAPI = {
  // 📦 Create shipment
  create: (shipmentData) =>
    apiRequest(`${API_BASE_URLS.SHIPPING}/shipments`, {
      method: "POST",
      body: JSON.stringify(shipmentData),
    }),

  // 🔍 Get shipment by ID
  getById: (shipmentId) =>
    apiRequest(`${API_BASE_URLS.SHIPPING}/shipments/${shipmentId}`),

  // 📋 List all shipments (with pagination)
  getAll: () => {
    console.log("SHIPPING BASE URL:", API_BASE_URLS.SHIPPING); // 🔥 ADD THIS
    return apiRequest(`${API_BASE_URLS.SHIPPING}/shipments`);
  },

  // 🔄 Update shipment status
  updateStatus: (shipmentId, statusData) =>
    apiRequest(`${API_BASE_URLS.SHIPPING}/shipments/${shipmentId}/status`, {
      method: "PATCH",
      body: JSON.stringify(statusData),
    }),

  // 📦 Get shipments by order
  getByOrder: (orderId) =>
    apiRequest(`${API_BASE_URLS.SHIPPING}/orders/${orderId}/shipments`),

  // ❤️ Health check
  health: () => apiRequest(`${API_BASE_URLS.SHIPPING}/health`),
};

export default {
  orderAPI,
  inventoryAPI,
  customerAPI,
  paymentAPI,
  notificationAPI,
  shippingAPI,
};
