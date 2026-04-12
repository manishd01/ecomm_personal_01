import React from "react";

function InventoryTable({ inventory }) {
  return (
    <section className="section">
      <h2>📊 Inventory ({inventory.length})</h2>
      {inventory.length > 0 ? (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Product Name</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {inventory.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.product_name}</td>
                  <td>
                    <span
                      className={`quantity ${item.quantity > 0 ? "in-stock" : "out-of-stock"}`}
                    >
                      {item.quantity}
                    </span>
                  </td>
                  <td>${item.price}</td>
                  <td>{item.description || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No inventory items found</p>
      )}
    </section>
  );
}

export default InventoryTable;
