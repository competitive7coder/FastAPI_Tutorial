import React from "react";
import "./TaglineSection.css";

const TaglineSection = () => {
  return (
    <div className="tagline-card">
      <div className="tagline-content">
        <h3>Inventory Overview</h3>

        <p className="tagline-subtitle">
          Manage products, pricing, and stock levels in one place with a clean,
          fast, and reliable inventory system.
        </p>

        <ul className="tagline-points">
          <li>• Real-time product tracking</li>
          <li>• Quick add, edit, and delete actions</li>
          <li>• Clear visibility of stock quantity</li>
        </ul>
      </div>
    </div>
  );
};

export default TaglineSection;
