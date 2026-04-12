import React from "react";

function CustomersTable({ customers }) {
  return (
    <section className="section">
      <h2>👥 Customers ({customers.length})</h2>
      {customers.length > 0 ? (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>IDjj</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>City</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td>{customer.id}</td>
                  <td>
                    {customer.first_name} {customer.last_name}
                  </td>
                  <td>{customer.email}</td>
                  <td>{customer.phone || "N/A"}</td>
                  <td>{customer.city || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No customers found</p>
      )}
    </section>
  );
}

export default CustomersTable;
