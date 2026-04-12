function ShipmentStats({ shipments }) {
  const total = shipments.length;
  const inTransit = shipments.filter((s) => s.status === "SHIPPED").length;
  const delivered = shipments.filter((s) => s.status === "DELIVERED").length;

  const deliveredToday = shipments.filter((s) => {
    return (
      s.delivered_at &&
      new Date(s.delivered_at).toDateString() === new Date().toDateString()
    );
  }).length;

  return (
    <div className="stats-container">
      <div>📦 Total: {total}</div>
      <div>🚚 In Transit: {inTransit}</div>
      <div>✅ Delivered: {delivered}</div>
      <div>📅 Delivered Today: {deliveredToday}</div>
    </div>
  );
}
