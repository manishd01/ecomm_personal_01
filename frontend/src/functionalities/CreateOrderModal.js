import { useEffect, useState } from "react";
import { orderAPI, customerAPI, inventoryAPI } from "../services/api";
import "./style_func.css";

const CreateOrderModal = ({ onClose, onSuccess }) => {
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);

  const [form, setForm] = useState({
    customer_id: "",
    product_id: "",
    quantity: 1,
    price: 0,
  });

  // Load dropdown data
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const custRes = await customerAPI.getAll();
      const prodRes = await inventoryAPI.getAll();

      if (custRes.success) setCustomers(custRes.data || []);
      if (prodRes.success) setProducts(prodRes.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  // Product selection
  const handleProductChange = (productId) => {
    const product = products.find((p) => p.id == productId);

    if (!product) return;

    setForm((prev) => ({
      ...prev,
      product_id: productId,
      price: product.price,
    }));
  };

  // Quantity change
  const handleQuantityChange = (qty) => {
    const product = products.find((p) => p.id == form.product_id);

    if (product && qty > product.quantity) {
      alert("Quantity exceeds available stock");
      return;
    }

    setForm((prev) => ({ ...prev, quantity: qty }));
  };

  const totalPrice = form.price * form.quantity;

  // Submit
  //   const handleSubmit = async () => {
  //     try {
  //       const res = await orderAPI.create({
  //         ...form,
  //         price: totalPrice,
  //       });
  const handleSubmit = async () => {
    try {
      const response = await orderAPI.create({
        ...form,
        price: form.price, // backend expects price
      });

      console.log("Order API response:", response); // DEBUG

      if (response.success) {
        console.log("Order created successfully:", response.data);
        onSuccess(response.data); // ✅ PASS ORDER BACK
      } else {
        alert("Failed to create order");
      }
    } catch (err) {
      console.error(err);
      alert("Error creating order");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h2>Create Order</h2>

        {/* Customer */}
        <select
          onChange={(e) =>
            setForm((prev) => ({ ...prev, customer_id: e.target.value }))
          }
        >
          <option value="">Select Customer</option>
          {customers.map((c) => (
            <option key={c.id} value={c.id}>
              {c.first_name} {c.last_name}
            </option>
          ))}
        </select>

        {/* Product */}
        <select onChange={(e) => handleProductChange(e.target.value)}>
          <option value="">Select Product</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.product_name} (Stock: {p.quantity})
            </option>
          ))}
        </select>

        {/* Quantity */}
        <input
          type="number"
          min="1"
          value={form.quantity}
          onChange={(e) => handleQuantityChange(Number(e.target.value))}
        />

        {/* Price */}
        <p>Total Price: ₹{totalPrice}</p>

        <div style={{ marginTop: "10px" }}>
          <button onClick={handleSubmit}>Submit</button>
          <button onClick={onClose} style={{ marginLeft: "10px" }}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateOrderModal;
