// Service Status Monitor
import { HEALTH_URLS } from "../config/apiConfig";

export const checkServiceHealth = async (serviceName) => {
  try {
    const response = await fetch(HEALTH_URLS[serviceName], {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return { [serviceName]: response.ok };
  } catch (error) {
    console.error(`Health check failed for ${serviceName}:`, error);
    return { [serviceName]: false };
  }
};

export const checkAllServicesHealth = async () => {
  const services = [
    "order",
    "inventory",
    "customer",
    "payment",
    "notification",
    "shipping",
    "ai",
  ];
  const checks = await Promise.all(
    services.map((service) => checkServiceHealth(service)),
  );
  return Object.assign({}, ...checks);
};

export default {
  checkServiceHealth,
  checkAllServicesHealth,
};
