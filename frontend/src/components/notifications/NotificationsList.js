import React from "react";

function NotificationsList({ notifications }) {
  return (
    <section className="section">
      <h2>🔔 Notifications ({notifications.length})</h2>
      {notifications.length > 0 ? (
        <div className="notifications-container">
          {notifications.map((notification) => (
            <div key={notification.id} className="notification-card">
              <div className="notification-header">
                <h4>{notification.subject}</h4>
                <span
                  className={`read-status ${
                    notification.is_read ? "read" : "unread"
                  }`}
                >
                  {notification.is_read ? "✓ Read" : "⚪ Unread"}
                </span>
              </div>
              <p>{notification.message}</p>
              <div className="notification-meta">
                <span className="badge">{notification.notification_type}</span>
                <span>Customer: {notification.customer_id}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>No notifications found</p>
      )}
    </section>
  );
}

export default NotificationsList;
