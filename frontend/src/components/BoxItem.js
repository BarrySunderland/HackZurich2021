import React from "react";

export default function NotificationItem({ title, value }) {
  return (
    <div
      style={{
        width: 400,
        height: 100,
        backgroundColor: "white",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderColor: "grey",
        borderRadius: 5,
        margin: 20,
      }}
    >
      <h4 style={{ color: "grey" }}>{title}</h4>
      <h4 style={{ color: "#C0C0C0", marginLeft: 10 }}>{value}</h4>
    </div>
  );
}
