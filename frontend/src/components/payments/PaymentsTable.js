import React from "react";

function PaymentsTable({ payments }) {
  return (
    <section className="section">
      <h2>💳 Payments ({payments.length})</h2>
      {payments.length > 0 ? (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Order</th>
                <th>Customer</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((payment) => (
                <tr key={payment.id}>
                  <td>{payment.id}</td>
                  <td>{payment.order_id}</td>
                  <td>{payment.customer_id}</td>
                  <td>${payment.amount}</td>
                  <td>{payment.payment_method}</td>
                  <td>
                    <span className={`badge ${payment.status}`}>
                      {payment.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No payments found</p>
      )}
    </section>
  );
}

export default PaymentsTable;
