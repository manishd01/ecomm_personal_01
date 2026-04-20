import React, { useEffect, useState } from "react";
import "../../App.css";
import { shippingAPI, orderAPI } from "../../services/api";

function CreateShipmentModal({ onClose, onSuccess }) {
  const [orders, setOrders] = useState([]);
  const [shipments, setShipments] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState("");
  const [loading, setLoading] = useState(false);

  // 🔥 Fetch data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const ordersRes = await orderAPI.getAll();
        const shipmentsRes = await shippingAPI.getAll();

        const ordersData = ordersRes.data || [];
        const shipmentsData = shipmentsRes.data || [];

        setOrders(ordersData);
        setShipments(shipmentsData);

        // 🔥 Filter orders without shipment
        const shippedOrderIds = shipmentsData.map((s) => s.order_id);

        const availableOrders = ordersData.filter(
          (o) => !shippedOrderIds.includes(o.id),
        );

        setFilteredOrders(availableOrders);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, []);

  // 🔥 Create shipment
  const handleCreate = async () => {
    if (!selectedOrder) {
      alert("Please select an order");
      return;
    }

    try {
      setLoading(true);

      const res = await shippingAPI.create({
        order_id: Number(selectedOrder),
      });

      const newShipment = res.data;
      onClose();

      if (onSuccess) onSuccess(newShipment);
    } catch (err) {
      console.error(err);
      alert("Failed to create shipment");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>➕ Create Shipment</h3>

        {/* 🔥 DROPDOWN */}
        {filteredOrders.length > 0 ? (
          <select
            className="input-field"
            value={selectedOrder}
            onChange={(e) => setSelectedOrder(e.target.value)}
          >
            <option value="">Select Order</option>
            {filteredOrders.map((order) => (
              <option key={order.id} value={order.id}>
                Order #{order.id}
              </option>
            ))}
          </select>
        ) : (
          <p>⚠️ No orders available for shipment</p>
        )}

        {/* ACTIONS */}
        <div className="modal-actions">
          <button
            className="confirm-btn"
            onClick={handleCreate}
            disabled={loading || filteredOrders.length === 0}
          >
            {loading ? "Creating..." : "✅ Create"}
          </button>

          <button className="cancel-btn" onClick={onClose}>
            ❌ Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default CreateShipmentModal;
