import React from "react";
import { useDashboardData } from "../hooks/useDashboardData";
import Header from "../components/layout/Header";
import Footer from "../components/layout/Footer";
import ServicesStatus from "../components/layout/ServicesStatus";
import CreateOrderButton from "../components/orders/CreateOrderButton";
import OrdersTable from "../components/orders/OrdersTable";
import InventoryTable from "../components/inventory/InventoryTable";
import CustomersTable from "../components/customers/CustomersTable";
import PaymentsTable from "../components/payments/PaymentsTable";
import NotificationsList from "../components/notifications/NotificationsList";
import ShipmentsList from "../components/shipping/ShipmentsList";

function DashboardPage() {
  const {
    orders,
    inventory,
    customers,
    payments,
    notifications,
    shipments,
    loading,
    error,
    servicesHealth,
    updateShipmentInUI,
    addShipmentToUI,
    fetchData,
  } = useDashboardData();

  return (
    <div className="App">
      <Header />

      <main className="App-main">
        {/* Services Status */}
        <ServicesStatus servicesHealth={servicesHealth} />

        {/* Data Display Sections */}
        {loading ? (
          <div className="loading">
            <p>⏳ Loading data from all microservices...</p>
          </div>
        ) : error ? (
          <div className="error-section">
            <p className="error">❌ Error: {error}</p>
          </div>
        ) : (
          <>
            {/* Create Order Section */}
            <CreateOrderButton onRefreshData={fetchData} />

            {/* Orders Section */}
            <OrdersTable orders={orders} />

            {/* Inventory Section */}
            <InventoryTable inventory={inventory} />

            {/* Customers Section */}
            <CustomersTable customers={customers} />

            {/* Payments Section */}
            <PaymentsTable payments={payments} />

            {/* Notifications Section */}
            <NotificationsList notifications={notifications} />

            {/* Shipping Section */}

            <ShipmentsList
              shipments={shipments}
              updateShipmentInUI={updateShipmentInUI}
              addShipmentToUI={addShipmentToUI}
            />
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default DashboardPage;
