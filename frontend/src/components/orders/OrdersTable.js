import React from "react";

function OrdersTable({ orders }) {
  return (
    <section className="section">
      <h2>📦 Orders ({orders.length})</h2>
      {orders.length > 0 ? (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.customer_id}</td>
                  <td>{order.product_id}</td>
                  <td>{order.quantity}</td>
                  <td>${order.price}</td>
                  <td>${order.total_price}</td>
                  <td>
                    <span className={`badge ${order.status}`}>
                      {order.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No orders found</p>
      )}
    </section>
  );
}

export default OrdersTable;
