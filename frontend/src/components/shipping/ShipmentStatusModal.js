import React from "react";
import "../../App.css";
function ShipmentStatusModal({
  shipment,
  onClose,
  onConfirm,
  getNextStatus,
  updateShipmentInUI,
}) {
  if (!shipment) return null;

  const nextStatus = getNextStatus(shipment.status);

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>Update Shipment Status</h3>

        <p>
          <strong>Shipment ID:</strong> {shipment.id}
        </p>

        <p>
          <strong>Current Status:</strong> {shipment.status}
        </p>

        <p>
          <strong>Next Status:</strong> {nextStatus || "No further updates"}
        </p>

        {nextStatus && (
          <button
            className="confirm-btn"
            onClick={() => onConfirm(shipment.id, nextStatus)}
          >
            ✅ Confirm Update
          </button>
        )}

        <button className="cancel-btn" onClick={onClose}>
          ❌ Cancel
        </button>
      </div>
    </div>
  );
}

export default ShipmentStatusModal;
