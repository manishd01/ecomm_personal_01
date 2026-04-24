import React, { useState } from "react";
import "../../App.css";
import ShipmentStatusModal from "./ShipmentStatusModal";
import { shippingAPI, addTracking } from "../../services/api";
import CreateShipmentModal from "./CreateShipmentModal";

function ShipmentsList({ shipments, updateShipmentInUI, addShipmentToUI }) {
  const [selectedShipment, setSelectedShipment] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  const openStatusModal = (shipment) => {
    setSelectedShipment(shipment);
    setShowModal(true);
  };

  const formatStatus = (status) => status.replaceAll("_", " ");

  const handleStatusUpdate = async (id, payload) => {
    try {
      console.log("🚀 Updating shipment:", id, payload);

      // 🔥 STATUS UPDATE
      if (payload.type === "STATUS") {
        const res = await shippingAPI.updateStatus(id, {
          status: payload.data,
        });

        console.log("✅ Status updated --:", res.data);

        // updateShipmentInUI(id, { status: payload.data });
        updateShipmentInUI(id, res.data); // ✅ send full object
      }

      // 🔥 TRACKING UPDATE
      if (payload.type === "TRACKING") {
        const res = await shippingAPI.addTracking(id, payload.data);

        const updated = await shippingAPI.getShipmentById(id);

        console.log("✅ Fresh shipment:", updated.data);
        console.log("📍 Tracking added:", res.data);

        // For now (simple approach)
        // window.location.reload();
        updateShipmentInUI(id, {
          tracking_updates: [res.data],
        });
      }

      // ✅ ALWAYS CLOSE MODAL
      setShowModal(false);
    } catch (err) {
      console.error("❌ API ERROR:", err);

      alert(err?.response?.data?.detail || "Something went wrong");
    }
  };

  // const STATUS_ACTIONS = {
  //   CREATED: [{ type: "STATUS", value: "SHIPPED", label: "🚚 Ship Order" }],

  //   SHIPPED: [{ type: "TRACKING", label: "📍 Add Tracking Update" }],

  //   IN_TRANSIT: [
  //     {
  //       type: "STATUS",
  //       value: "OUT_FOR_DELIVERY",
  //       label: "📦 Out for Delivery",
  //     },
  //   ],

  //   OUT_FOR_DELIVERY: [
  //     { type: "STATUS", value: "DELIVERED", label: "✅ Mark Delivered" },
  //   ],

  //   DELIVERED: [
  //     { type: "STATUS", value: "RETURN_REQUESTED", label: "↩️ Return" },
  //     { type: "STATUS", value: "REPLACEMENT_REQUESTED", label: "🔁 Replace" },
  //   ],

  //   RETURN_REQUESTED: [
  //     { type: "STATUS", value: "RETURNED", label: "✔ Confirm Return" },
  //   ],

  //   REPLACEMENT_REQUESTED: [
  //     { type: "STATUS", value: "REPLACED", label: "✔ Confirm Replacement" },
  //   ],
  // };

  // const getNextActions = async (shipmentId) => {
  //   const res = await shippingAPI.get(`/shipments/${shipmentId}/next-actions`);
  //   console.log(res, "Next Actions:");
  //   return res.data.allowed_actions;
  // };

  // ✅ Unified Timeline Builder
  const buildTimeline = (shipment) => {
    const timeline = [];

    // CREATED
    timeline.push({
      type: "STATUS",
      label: "Order Created",
      time: shipment.created_at,
    });

    // SHIPPED
    if (shipment.status !== "CREATED") {
      timeline.push({
        type: "STATUS",
        label: `Shipped via ${shipment.carrier || "Carrier"}`,
        time: shipment.shipped_at || shipment.created_at,
      });
    }

    // TRACKING EVENTS
    shipment.tracking_updates?.forEach((t) => {
      timeline.push({
        type: "TRACKING",
        label: t.status.replaceAll("_", " "),
        location: t.location,
        description: t.description,
        time: t.timestamp,
      });
    });

    // OUT FOR DELIVERY
    if (
      shipment.status === "OUT_FOR_DELIVERY" ||
      shipment.status === "DELIVERED"
    ) {
      timeline.push({
        type: "STATUS",
        label: "Out for Delivery",
        time: shipment.updated_at,
      });
    }

    // DELIVERED
    if (shipment.delivered_at) {
      timeline.push({
        type: "STATUS",
        label: "Delivered",
        time: shipment.delivered_at,
      });
    }
    // RETURN FLOW
    if (shipment.return_requested_at) {
      timeline.push({
        type: "STATUS",
        label: "Return Requested",
        time: shipment.return_requested_at,
      });
    }

    if (shipment.returned_at) {
      timeline.push({
        type: "STATUS",
        label: "Returned Successfully",
        time: shipment.returned_at,
      });
    }

    // REPLACEMENT FLOW
    if (shipment.replacement_requested_at) {
      timeline.push({
        type: "STATUS",
        label: "Replacement Requested",
        time: shipment.replacement_requested_at,
      });
    }

    if (shipment.replaced_at) {
      timeline.push({
        type: "STATUS",
        label: "Product Replaced",
        time: shipment.replaced_at,
      });
    }
    console.log("timelines: ", timeline);
    return timeline.sort((a, b) => new Date(a.time) - new Date(b.time));
  };

  return (
    <section className="section-modal">
      <h2>📦 Shipping Dashboard</h2>

      <button className="create-btn" onClick={() => setShowCreateModal(true)}>
        ➕ Create Shipment
      </button>

      <h3>All Shipments ({shipments.length})</h3>

      {shipments.length > 0 ? (
        <div className="shipments-container">
          {shipments.map((shipment) => {
            const timeline = buildTimeline(shipment);

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

                  <button onClick={() => openStatusModal(shipment)}>
                    ✏️ Change Status
                  </button>
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

                {/* 🔥 TIMELINE */}
                <div className="timeline">
                  {timeline.map((item, index) => (
                    <div key={index} className="timeline-item">
                      <div className="timeline-dot"></div>

                      <div className="timeline-content">
                        <div className="timeline-title">
                          {item.type === "STATUS"
                            ? `📦 ${item.label}`
                            : `📍 ${item.label} - ${item.location}`}
                        </div>

                        {item.description && (
                          <div className="timeline-desc">
                            {item.description}
                          </div>
                        )}

                        <div className="timeline-time">
                          🕒 {new Date(item.time).toLocaleString()}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p>No shipments found</p>
      )}
      {showModal && (
        <ShipmentStatusModal
          shipment={selectedShipment}
          onClose={() => setShowModal(false)}
          onConfirm={handleStatusUpdate}
        />
      )}

      {showCreateModal && (
        <CreateShipmentModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={(newShipment) => addShipmentToUI(newShipment)}
        />
      )}
    </section>
  );
}

export default ShipmentsList;
