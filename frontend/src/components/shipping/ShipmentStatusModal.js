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

  // ✅ NEW: helper to check if location is required
  const requiresLocation = (action) =>
    action.type === "TRACKING" ||
    (action.type === "STATUS" && action.value === "SHIPPED");

  const handleActionClick = async (action) => {
    try {
      // ✅ validation (important)
      if (requiresLocation(action) && !location) {
        alert("Location is required");
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
        meta: requiresLocation(action) ? { location } : null, // ✅ send location for shipped also
      });

      onClose();
    } catch (err) {
      console.error(err);
      alert("Error updating shipment");
    } finally {
      setLoading(false);
    }
  };
  const hasTrackingAction = actions.some((a) => a.type === "TRACKING");
  const hasShipAction = actions.some(
    (a) => a.type === "STATUS" && a.value === "SHIPPED",
  );

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
                disabled={loading || (requiresLocation(action) && !location)}
                onClick={() => handleActionClick(action)}
              >
                {action.label}
              </button>
            ))}
          </div>
        )}

        {/* 🔥 TRACKING + SHIPPED INPUTS */}
        {/* {actions.some(
        //   (a) =>
        //     a.type === "TRACKING" ||
        //     (a.type === "STATUS" && a.value === "SHIPPED"),
        // ) && ( */}
        {/* ✅ SHIPPED → ONLY LOCATION */}
        {hasShipAction && (
          <div className="input-group">
            <label>📍 Location</label>
            <input
              className="input-field"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Ludhiana Hub"
            />
          </div>
        )}

        {/* ✅ TRACKING → FULL FIELDS */}
        {hasTrackingAction && (
          <div className="input-group">
            <label>📍 Location</label>
            <input
              className="input-field"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Delhi Hub"
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
