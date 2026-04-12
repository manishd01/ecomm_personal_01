import React from "react";
import { SWAGGER_URLS } from "../../config/apiConfig";

const renderStatus = (isHealthy) => (
  <span className={`status ${isHealthy ? "healthy" : "unhealthy"}`}>
    {isHealthy ? "✓ Online" : "✗ Offline"}
  </span>
);

function ServicesStatus({ servicesHealth }) {
  return (
    <section className="services-status">
      <h2>🔧 Services Status</h2>
      <div className="status-grid">
        <div className="service-card">
          <h3>Order Service (8000)</h3>
          {renderStatus(servicesHealth.order)}
          <a
            href={SWAGGER_URLS.order}
            target="_blank"
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 API Docs
          </a>
        </div>
        <div className="service-card">
          <h3>Inventory Service (8001)</h3>
          {renderStatus(servicesHealth.inventory)}
          <a
            href={SWAGGER_URLS.inventory}
            target="_blank"
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 API Docs
          </a>
        </div>
        <div className="service-card">
          <h3>Customer Service (8002)</h3>
          {renderStatus(servicesHealth.customer)}
          <a
            href={SWAGGER_URLS.customer}
            target="_blank"
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 API Docs
          </a>
        </div>
        <div className="service-card">
          <h3>Payment Service (8003)</h3>
          {renderStatus(servicesHealth.payment)}
          <a
            href={SWAGGER_URLS.payment}
            target="_blank"
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 API Docs
          </a>
        </div>
        <div className="service-card">
          <h3>Notification Service (8004)</h3>
          {renderStatus(servicesHealth.notification)}
          <a
            href={SWAGGER_URLS.notification}
            target="_blank"
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 API Docs
          </a>
        </div>
        <div className="service-card">
          <h3>Shipping Service (8005)</h3>
          {renderStatus(servicesHealth.shipping)}
          <a
            href={SWAGGER_URLS.shipping}
            target="_blank"
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 API Docs
          </a>
        </div>
      </div>
    </section>
  );
}

export default ServicesStatus;
