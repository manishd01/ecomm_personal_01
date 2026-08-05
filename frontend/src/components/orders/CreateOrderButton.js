import React from "react";
import { useEffect } from "react";
import CreateOrderModal from "../../functionalities/CreateOrderModal";
import PaymentModal from "../../functionalities/PaymentModal";

function CreateOrderButton({ onOrderCreated, onRefreshData }) {
  const [showModal, setShowModal] = React.useState(false);
  const [selectedOrder, setSelectedOrder] = React.useState(null);
  const [showPaymentModal, setShowPaymentModal] = React.useState(false);
  useEffect(() => {
    console.log("selectedOrder changed:", selectedOrder);

    if (selectedOrder) {
      console.log("OPENING PAYMENT MODAL");

      setShowPaymentModal(true);
    }
  }, [selectedOrder]);
  console.log("showPaymentModal:", showPaymentModal);
  return (
    <>
      <section>
        <button onClick={() => setShowModal(true)}>+ Add Order</button>

        {showModal && (
          <CreateOrderModal
            onClose={() => setShowModal(false)}
            onSuccess={(newOrder) => {
              console.log("NEW ORDER RECEIVED:", newOrder);

              setSelectedOrder(newOrder);
              console.log("selectedOrder:", selectedOrder);
              setShowModal(false);

              // setTimeout(() => {
              //   setShowPaymentModal(true);
              // }, 100);

              // onRefreshData();
            }}
          />
        )}

        {/* ✅ ADD THIS HERE (STEP 3) */}
        {showPaymentModal && selectedOrder && (
          <PaymentModal
            order={selectedOrder}
            onClose={() => setShowPaymentModal(false)}
            onSuccess={() => {
              onRefreshData();

              setShowPaymentModal(false);
            }}
          />
        )}
      </section>
    </>
  );
}

export default CreateOrderButton;
