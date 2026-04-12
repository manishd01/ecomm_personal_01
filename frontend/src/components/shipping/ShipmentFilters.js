function ShipmentFilters({ filters, setFilters }) {
  return (
    <div>
      <input
        placeholder="Search Tracking ID"
        onChange={(e) =>
          setFilters((prev) => ({ ...prev, search: e.target.value }))
        }
      />

      <select
        onChange={(e) =>
          setFilters((prev) => ({ ...prev, status: e.target.value }))
        }
      >
        <option value="">All</option>
        <option value="CREATED">Created</option>
        <option value="SHIPPED">Shipped</option>
        <option value="DELIVERED">Delivered</option>
      </select>
    </div>
  );
}
