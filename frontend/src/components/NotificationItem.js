import React from "react";
import "../App.css";
export default function NotificationItem({
  title,
  onZoom,
  onChartOpen,
  color,
}) {
  return (
    <div
      className="item-shadow"
      style={{
        width: 400,
        height: 70,
        backgroundColor: "white",
        display: "flex",
        alignItems: "center",
        borderColor: "grey",
        borderRadius: 5,
        margin: 20,
        paddingLeft: 50,
        cursor: "pointer",
      }}
      onClick={onZoom}
    >
      <span className="dot" style={{ backgroundColor: color }}></span>
      <span style={{ fontSize: 15, marginLeft: 15 }}>{title}</span>
      <span
        style={{ fontSize: 15, marginLeft: 15, color: "grey" }}
        onClick={(e) => {
          onChartOpen();
          e.stopPropagation();
        }}
      >
        Click to show detail
      </span>
    </div>
  );
}
