// API Configuration for all microservices
// Automatically switches between localhost and Docker service names

// API Configuration for all microservices
// API Configuration for all microservices

const API_HOST = process.env.REACT_APP_API_HOST;

const SERVICES = {
  order: `${API_HOST}:8000`,
  inventory: `${API_HOST}:8001`,
  customer: `${API_HOST}:8002`,
  payment: `${API_HOST}:8003`,
  notification: `${API_HOST}:8004`,
  shipping: `${API_HOST}:8005`,
};

export const API_BASE_URLS = {
  ORDERS: `${SERVICES.order}/api`,
  INVENTORY: `${SERVICES.inventory}/api`,
  CUSTOMERS: `${SERVICES.customer}/api`,
  PAYMENTS: `${SERVICES.payment}/api`,
  NOTIFICATIONS: `${SERVICES.notification}/api`,
  SHIPPING: `${SERVICES.shipping}/api`,
};

export const HEALTH_URLS = {
  order: `${SERVICES.order}/api/health`,
  inventory: `${SERVICES.inventory}/api/health`,
  customer: `${SERVICES.customer}/api/health`,
  payment: `${SERVICES.payment}/api/health`,
  notification: `${SERVICES.notification}/api/health`,
  shipping: `${SERVICES.shipping}/api/health`,
};

export const SWAGGER_URLS = {
  order: `${SERVICES.order}/docs`,
  inventory: `${SERVICES.inventory}/docs`,
  customer: `${SERVICES.customer}/docs`,
  payment: `${SERVICES.payment}/docs`,
  notification: `${SERVICES.notification}/docs`,
  shipping: `${SERVICES.shipping}/docs`,
};

export default API_BASE_URLS;

// import { shippingAPI } from "../services/api";

// const isDevelopment = process.env.NODE_ENV === "development";
// const isDocker = process.env.REACT_APP_ENV === "docker";

// // Service URLs
// const SERVICES = {
//   order:
//     isDevelopment && !isDocker
//       ? "http://localhost:8000"
//       : "http://order-service:8000",
//   inventory:
//     isDevelopment && !isDocker
//       ? "http://localhost:8001"
//       : "http://inventory-service:8000",
//   customer:
//     isDevelopment && !isDocker
//       ? "http://localhost:8002"
//       : "http://customer-service:8000",
//   payment:
//     isDevelopment && !isDocker
//       ? "http://localhost:8003"
//       : "http://payment-service:8000",
//   notification:
//     isDevelopment && !isDocker
//       ? "http://localhost:8004"
//       : "http://notification-service:8000",
//   shipping:
//     isDevelopment && !isDocker
//       ? "http://localhost:8005"
//       : "http://shipping-service:8000",
// };

// export const API_BASE_URLS = {
//   ORDERS: `${SERVICES.order}/api`,
//   INVENTORY: `${SERVICES.inventory}/api`,
//   CUSTOMERS: `${SERVICES.customer}/api`,
//   PAYMENTS: `${SERVICES.payment}/api`,
//   NOTIFICATIONS: `${SERVICES.notification}/api`,
//   SHIPPING: `${SERVICES.shipping}/api`,
// };

// // Service health check URLs
// export const HEALTH_URLS = {
//   order: `${SERVICES.order}/api/health`,
//   inventory: `${SERVICES.inventory}/api/health`,
//   customer: `${SERVICES.customer}/api/health`,
//   payment: `${SERVICES.payment}/api/health`,
//   notification: `${SERVICES.notification}/api/health`,
//   shipping: `${SERVICES.shipping}/api/health`,
// };

// // Swagger UI URLs for API Documentation
// export const SWAGGER_URLS = {
//   order: `${SERVICES.order}/docs`,
//   inventory: `${SERVICES.inventory}/docs`,
//   customer: `${SERVICES.customer}/docs`,
//   payment: `${SERVICES.payment}/docs`,
//   notification: `${SERVICES.notification}/docs`,
//   shipping: `${SERVICES.shipping}/docs`,
// };

// export default API_BASE_URLS;
