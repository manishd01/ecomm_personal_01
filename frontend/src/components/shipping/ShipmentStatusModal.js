import React, { useState } from "react";
import "../../App.css";

function ShipmentStatusModal({ shipment, onClose, onConfirm }) {
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [trackingStatus, setTrackingStatus] = useState("IN_TRANSIT");

  console.log("Shipment:", shipment);

  if (!shipment) return null;

  // 🔥 FROM BACKEND (NOT FRONTEND CONSTANT)
  const actions = shipment.allowed_actions || [];
  const isDelivered = shipment.status === "DELIVERED";

  const handleActionClick = async (action) => {
    try {
      // ✅ validation (important)
      if (action.type === "TRACKING" && !location) {
        alert("Location is required for tracking update");
        return;
      }

      setLoading(true);

      await onConfirm(shipment.id, {
        type: action.type,
        data:
          action.type === "TRACKING"
            ? {
                location,
                description,
                status: trackingStatus,
              }
            : action.value,
      });

      onClose();
    } catch (err) {
      console.error(err);
      alert("Error updating shipment");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>📦 Update Shipment</h3>

        <p>
          <strong>ID:</strong> {shipment.id}
        </p>

        <p>
          <strong>Status:</strong> {shipment.status.replaceAll("_", " ")}
        </p>

        {actions.length > 0 && (
          <div className="input-group">
            <h4>Available Actions</h4>

            {actions.map((action, index) => (
              <button
                key={index}
                className="confirm-btn"
                style={{ margin: "5px", width: "100%" }}
                disabled={loading || (action.type === "TRACKING" && !location)}
                onClick={() => handleActionClick(action)}
              >
                {action.label}
              </button>
            ))}
          </div>
        )}

        {/* 🔥 TRACKING INPUTS */}
        {actions.some((a) => a.type === "TRACKING") && (
          <div className="input-group">
            <label>📍 Location</label>
            <input
              className="input-field"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Ludhiana Hub"
            />
            <label>📦 Tracking Status</label>
            <select
              className="input-field"
              value={trackingStatus}
              onChange={(e) => setTrackingStatus(e.target.value)}
            >
              <option value="IN_TRANSIT">In Transit</option>
              <option value="ARRIVED_AT_HUB">Arrived at Hub</option>
              <option value="DEPARTED_HUB">Departed Hub</option>
              <option value="OUT_FOR_DELIVERY">Out for Delivery</option>
              <option value="DELIVERED">Delivered</option>
            </select>

            <label>📝 Description</label>
            <input
              className="input-field"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional note"
            />
          </div>
        )}

        {/* 🔥 CLOSE */}
        <div className="modal-actions">
          <button className="cancel-btn" onClick={onClose}>
            ❌ Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default ShipmentStatusModal;
