import React from "react";
import CreateOrderModal from "../../functionalities/CreateOrderModal";
import PaymentModal from "../../functionalities/PaymentModal";

function CreateOrderButton({ onOrderCreated, onRefreshData }) {
  const [showModal, setShowModal] = React.useState(false);
  const [selectedOrder, setSelectedOrder] = React.useState(null);
  const [showPaymentModal, setShowPaymentModal] = React.useState(false);

  return (
    <>
      <section>
        <button onClick={() => setShowModal(true)}>+ Add Order</button>

        {showModal && (
          <CreateOrderModal
            onClose={() => setShowModal(false)}
            onSuccess={(newOrder) => {
              console.log(newOrder, "order came");
              setShowModal(false);
              setSelectedOrder(newOrder); // ✅ store order
              setShowPaymentModal(true); // ✅ open payment modal
              onRefreshData();
            }}
          />
        )}

        {/* ✅ ADD THIS HERE (STEP 3) */}
        {showPaymentModal && selectedOrder && (
          <PaymentModal
            order={selectedOrder}
            onClose={() => setShowPaymentModal(false)}
            onSuccess={onRefreshData}
          />
        )}
      </section>
    </>
  );
}

export default CreateOrderButton;
