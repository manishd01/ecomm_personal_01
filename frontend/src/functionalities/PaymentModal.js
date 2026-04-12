import { useState } from "react";
import { paymentAPI } from "../services/api";
import "./style_func.css";

const PaymentModal = ({ order, onClose, onSuccess }) => {
  const [method, setMethod] = useState("COD");

  const handlePayment = async () => {
    const confirm = window.confirm("Confirm Payment?");

    const payload = {
      order_id: order.id,
      customer_id: order.customer_id,
      amount: order.total_price,
      payment_method: method,
      status: confirm ? "success" : "failed",
    };

    await paymentAPI.create(payload);

    onSuccess();
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h2>💳 Payment</h2>

        <p>
          <b>Order ID:</b> {order.id}
        </p>
        <p>
          <b>Amount:</b> ₹{order.total_price}
        </p>

        <label>Payment Method:</label>
        <select value={method} onChange={(e) => setMethod(e.target.value)}>
          <option>COD</option>
          <option>UPI</option>
          <option>CARD</option>
          <option>NET_BANKING</option>
        </select>

        <div>
          <button onClick={handlePayment}>Confirm Payment</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default PaymentModal;
