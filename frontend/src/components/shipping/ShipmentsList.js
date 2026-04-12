import React, { useState } from "react";
import "../../App.css";
import ShipmentStatusModal from "./ShipmentStatusModal";
import { shippingAPI } from "../../services/api";
import CreateShipmentModal from "./CreateShipmentModal";

function ShipmentsList({ shipments, updateShipmentInUI }) {
  const [selectedShipment, setSelectedShipment] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [orderId, setOrderId] = useState("");

  const openStatusModal = (shipment) => {
    setSelectedShipment(shipment);
    setShowModal(true);
  };

  const STATUS_FLOW = [
    "CREATED",
    "SHIPPED",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "RETURNED",
  ];

  const getNextStatus = (current) => {
    const index = STATUS_FLOW.indexOf(current);

    if (index === -1 || index === STATUS_FLOW.length - 1) {
      return null;
    }

    return STATUS_FLOW[index + 1];
  };

  const formatStatus = (status) => status.replaceAll("_", " ");

  const handleStatusUpdate = async (id, status) => {
    try {
      await shippingAPI.updateStatus(id, { status });
      updateShipmentInUI(id, { status });
      setShowModal(false);
    } catch (err) {
      console.error(err);
    }
  };

  // 🔥 KPI CALCULATIONS
  const total = shipments.length;
  const created = shipments.filter((s) => s.status === "CREATED").length;
  const shipped = shipments.filter((s) => s.status === "SHIPPED").length;
  const outForDelivery = shipments.filter(
    (s) => s.status === "OUT_FOR_DELIVERY",
  ).length;
  const delivered = shipments.filter((s) => s.status === "DELIVERED").length;
  const returned = shipments.filter((s) => s.status === "RETURNED").length;
  const replaced = shipments.filter((s) => s.status === "REPLACED").length;

  return (
    <section className="section">
      <h2>📦 Shipping Dashboard</h2>
      <button className="create-btn" onClick={() => setShowCreateModal(true)}>
        ➕ Create Shipment
      </button>

      {/* KPI CARDS */}
      <div className="kpi-container">
        <div className="kpi-card total">
          📦 Total <br /> {total}
        </div>

        <div className="kpi-card created">
          🆕 Created <br /> {created}
        </div>

        <div className="kpi-card shipped">
          🚚 Shipped <br /> {shipped}
        </div>

        <div className="kpi-card out">
          📍 Out for Delivery <br /> {outForDelivery}
        </div>

        <div className="kpi-card delivered">
          ✅ Delivered <br /> {delivered}
        </div>

        <div className="kpi-card returned">
          ↩️ Returned <br /> {returned}
        </div>

        <div className="kpi-card replaced">
          🔁 Replaced <br /> {replaced}
        </div>
      </div>

      {/* LIST */}
      <h3>All Shipments ({shipments.length})</h3>

      {shipments.length > 0 ? (
        <div className="shipments-container">
          {shipments.map((shipment) => {
            const nextStatus = getNextStatus(shipment.status);

            return (
              <div key={shipment.id} className="shipment-card">
                {/* HEADER */}
                <div className="shipment-header">
                  <h4>Shipment #{shipment.id}</h4>
                  <span
                    className={`status-badge ${shipment.status?.toLowerCase()}`}
                  >
                    {formatStatus(shipment.status)}
                  </span>
                </div>

                {/* BODY */}
                <div className="shipment-body">
                  <p>
                    <strong>Order:</strong> {shipment.order_id}
                  </p>
                  <p>
                    <strong>Tracking:</strong>{" "}
                    {shipment.tracking_number || "N/A"}
                  </p>
                  <p>
                    <strong>Carrier:</strong> {shipment.carrier || "N/A"}
                  </p>

                  {/* ACTION */}
                  <div className="shipment-actions">
                    {/* {nextStatus && (
                      <button
                        onClick={() =>
                          handleStatusUpdate(shipment.id, nextStatus)
                        }
                      >
                        🔄 Move to {formatStatus(nextStatus)}
                      </button>
                    )} */}

                    <button onClick={() => openStatusModal(shipment)}>
                      ✏️ Change Status
                    </button>
                  </div>
                </div>

                {/* META */}
                <div className="shipment-meta">
                  <span>
                    📅 {new Date(shipment.created_at).toLocaleString()}
                  </span>

                  {shipment.estimated_delivery && (
                    <span>
                      🚚 ETA:{" "}
                      {new Date(
                        shipment.estimated_delivery,
                      ).toLocaleDateString()}
                    </span>
                  )}

                  {shipment.delivered_at && (
                    <span>
                      ✅ Delivered:{" "}
                      {new Date(shipment.delivered_at).toLocaleDateString()}
                    </span>
                  )}
                </div>

                {/* TIMELINE */}
                <div className="shipment-timeline">
                  {STATUS_FLOW.map((status, index) => {
                    const currentIndex = STATUS_FLOW.indexOf(shipment.status);

                    return (
                      <span
                        key={status}
                        className={index <= currentIndex ? "done" : ""}
                      >
                        {formatStatus(status)}
                      </span>
                    );
                  })}
                </div>
              </div>
            );
          })}

          {showModal && (
            <ShipmentStatusModal
              shipment={selectedShipment}
              onClose={() => setShowModal(false)}
              onConfirm={handleStatusUpdate}
              getNextStatus={getNextStatus}
            />
          )}
          {showCreateModal && (
            <CreateShipmentModal
              onClose={() => setShowCreateModal(false)}
              onSuccess={() => {
                // 🔥 refresh data
                window.location.reload(); // quick fix
                // OR call fetchData() if available
              }}
            />
          )}
        </div>
      ) : (
        <p>No shipments found</p>
      )}
    </section>
  );
}

export default ShipmentsList;
