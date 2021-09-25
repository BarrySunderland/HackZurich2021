import React from "react";
import NotificationItem from "./NotificationItem";

export default function TopBar({
  predictedFailures,
  actualFailures,
  onZoom,
  onChartOpen,
}) {
  return (
    <div
      className="d-flex flex-column"
      style={{ width: "50%", minHeight: 800, backgroundColor: "#eee" }}
    >
      <h4 style={{ color: "grey", marginLeft: 140, paddingTop: 20 }}>
        Notifications
      </h4>
      {actualFailures.map((failure, i) => (
        <NotificationItem
          key={i}
          title={failure.name}
          onChartOpen={onChartOpen}
          onZoom={() => {
            onZoom(failure.Latitude, failure.Longitude);
          }}
        />
      ))}
      {predictedFailures.map((failure, i) => (
        <NotificationItem
          key={i}
          title={failure.name}
          onZoom={() => {
            onZoom(failure.Latitude, failure.Longitude);
          }}
          onChartOpen={onChartOpen}
        />
      ))}
    </div>
  );
}
