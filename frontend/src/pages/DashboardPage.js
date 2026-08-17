import React, { useState } from "react";

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
import AIAssistantPage from "./AIAssistantPage";

function DashboardPage() {
  const [activeTab, setActiveTab] = useState("orders");

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

  const renderContent = () => {
    switch (activeTab) {
      case "services":
        return <ServicesStatus servicesHealth={servicesHealth} />;

      case "orders":
        return (
          <>
            <CreateOrderButton onRefreshData={fetchData} />

            <OrdersTable orders={orders} />
          </>
        );

      case "inventory":
        return <InventoryTable inventory={inventory} />;

      case "customers":
        return <CustomersTable customers={customers} />;

      case "payments":
        return <PaymentsTable payments={payments} />;

      case "notifications":
        return <NotificationsList notifications={notifications} />;

      case "shipments":
        return (
          <ShipmentsList
            shipments={shipments}
            updateShipmentInUI={updateShipmentInUI}
            addShipmentToUI={addShipmentToUI}
          />
        );

      case "ai":
        return <AIAssistantPage />;

      default:
        return <OrdersTable orders={orders} />;
    }
  };

  return (
    <div className="App">
      <Header />

      <div className="dashboard-container">
        {/* Sidebar */}
        <aside className="sidebar">
          <h2 className="sidebar-title">Dashboard</h2>

          <button
            className={activeTab === "services" ? "active" : ""}
            onClick={() => setActiveTab("services")}
          >
            Service Status
          </button>

          <button
            className={activeTab === "orders" ? "active" : ""}
            onClick={() => setActiveTab("orders")}
          >
            Orders
          </button>

          <button
            className={activeTab === "inventory" ? "active" : ""}
            onClick={() => setActiveTab("inventory")}
          >
            Inventory
          </button>

          <button
            className={activeTab === "customers" ? "active" : ""}
            onClick={() => setActiveTab("customers")}
          >
            Customers
          </button>

          <button
            className={activeTab === "payments" ? "active" : ""}
            onClick={() => setActiveTab("payments")}
          >
            Payments
          </button>

          <button
            className={activeTab === "notifications" ? "active" : ""}
            onClick={() => setActiveTab("notifications")}
          >
            Notifications
          </button>

          <button
            className={activeTab === "shipments" ? "active" : ""}
            onClick={() => setActiveTab("shipments")}
          >
            Shipments
          </button>
          <button
            className={activeTab === "ai" ? "active" : ""}
            onClick={() => setActiveTab("ai")}
          >
            🤖 AI Assistant
          </button>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {loading ? (
            <div className="loading">
              <p>⏳ Loading data from all microservices...</p>
            </div>
          ) : error ? (
            <div className="error-section">
              <p className="error">❌ Error: {error}</p>
            </div>
          ) : (
            renderContent()
          )}
        </main>
      </div>

      <Footer />
    </div>
  );
}

export default DashboardPage;

//

// import React from "react";
// import { useDashboardData } from "../hooks/useDashboardData";
// import Header from "../components/layout/Header";
// import Footer from "../components/layout/Footer";
// import ServicesStatus from "../components/layout/ServicesStatus";
// import CreateOrderButton from "../components/orders/CreateOrderButton";
// import OrdersTable from "../components/orders/OrdersTable";
// import InventoryTable from "../components/inventory/InventoryTable";
// import CustomersTable from "../components/customers/CustomersTable";
// import PaymentsTable from "../components/payments/PaymentsTable";
// import NotificationsList from "../components/notifications/NotificationsList";
// import ShipmentsList from "../components/shipping/ShipmentsList";

// function DashboardPage() {
//   const {
//     orders,
//     inventory,
//     customers,
//     payments,
//     notifications,
//     shipments,
//     loading,
//     error,
//     servicesHealth,
//     updateShipmentInUI,
//     addShipmentToUI,
//     fetchData,
//   } = useDashboardData();

//   return (
//     <div className="App">
//       <Header />

//       <main className="App-main">
//         {/* Services Status */}
//         <ServicesStatus servicesHealth={servicesHealth} />

//         {/* Data Display Sections */}
//         {loading ? (
//           <div className="loading">
//             <p>⏳ Loading data from all microservices...</p>
//           </div>
//         ) : error ? (
//           <div className="error-section">
//             <p className="error">❌ Error: {error}</p>
//           </div>
//         ) : (
//           <>
//             {/* Create Order Section */}
//             <CreateOrderButton onRefreshData={fetchData} />

//             {/* Orders Section */}
//             <OrdersTable orders={orders} />

//             {/* Inventory Section */}
//             <InventoryTable inventory={inventory} />

//             {/* Customers Section */}
//             <CustomersTable customers={customers} />

//             {/* Payments Section */}
//             <PaymentsTable payments={payments} />

//             {/* Notifications Section */}
//             <NotificationsList notifications={notifications} />

//             {/* Shipping Section */}

//             <ShipmentsList
//               shipments={shipments}
//               updateShipmentInUI={updateShipmentInUI}
//               addShipmentToUI={addShipmentToUI}
//             />
//           </>
//         )}
//       </main>

//       <Footer />
//     </div>
//   );
// }

// export default DashboardPage;
