import { useState, useEffect } from "react";
import {
  orderAPI,
  inventoryAPI,
  customerAPI,
  paymentAPI,
  notificationAPI,
  shippingAPI,
} from "../services/api";
import { checkAllServicesHealth } from "../services/healthCheck";

export const useDashboardData = () => {
  const [orders, setOrders] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [payments, setPayments] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [servicesHealth, setServicesHealth] = useState({});

  const fetchData = async () => {
    try {
      setLoading(true);

      const [
        ordersRes,
        inventoryRes,
        customersRes,
        paymentsRes,
        notificationsRes,
        shippingRes,
        healthRes,
      ] = await Promise.all([
        orderAPI.getAll(),
        inventoryAPI.getAll(),
        customerAPI.getAll(),
        paymentAPI.getAll(),
        notificationAPI.getAll(),
        shippingAPI.getAll(),
        checkAllServicesHealth(),
      ]);

      if (ordersRes.success) {
        setOrders(Array.isArray(ordersRes.data) ? ordersRes.data : []);
      }

      if (inventoryRes.success) {
        setInventory(Array.isArray(inventoryRes.data) ? inventoryRes.data : []);
      }

      if (customersRes.success) {
        setCustomers(Array.isArray(customersRes.data) ? customersRes.data : []);
      }

      if (paymentsRes.success) {
        setPayments(Array.isArray(paymentsRes.data) ? paymentsRes.data : []);
      }

      if (notificationsRes.success) {
        setNotifications(
          Array.isArray(notificationsRes.data) ? notificationsRes.data : [],
        );
      }
      if (shippingRes.success) {
        console.log(shippingRes.success, "statusin shipping");
        setShipments(Array.isArray(shippingRes.data) ? shippingRes.data : []);
      }
      console.log("all res:", {
        orders: ordersRes,
        inventory: inventoryRes,
        customers: customersRes,
        payments: paymentsRes,
        notifications: notificationsRes,
        shipping: shippingRes,
        health: healthRes,
      });
      setServicesHealth(healthRes);
    } catch (err) {
      console.log(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const addShipmentToUI = (newShipment) => {
    setShipments((prev) => [newShipment, ...prev]);
  };
  const updateShipmentInUI = (id, updatedShipment) => {
    setShipments((prev) =>
      prev.map((s) => {
        if (s.id !== id) return s;

        return {
          ...updatedShipment,
          allowed_actions:
            updatedShipment.allowed_actions ?? s.allowed_actions ?? [],
        };
      }),
    );
  };

  return {
    orders,
    inventory,
    customers,
    payments,
    notifications,
    shipments,
    loading,
    error,
    servicesHealth,
    updateShipmentInUI,
    addShipmentToUI,
    fetchData,
  };
};
