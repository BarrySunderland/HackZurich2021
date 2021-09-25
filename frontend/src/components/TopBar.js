import React from "react";
import BoxItem from "./BoxItem";
import TimeSlider from "./TimePicker";
export default function TopBar({
  predictedFailures,
  actualFailures,
  startDate,
  onStartDateChange,
}) {
  return (
    <>
      <h4 style={{ color: "grey", marginLeft: 20, paddingTop: 20 }}>
        General Status
      </h4>
      <div
        className="d-flex flex-row  align-items-center"
        style={{ marginBottom: 20 }}
      >
        <BoxItem
          title="predicted failures: "
          value={predictedFailures.length}
        />
        <BoxItem title="actual failures: " value={actualFailures.length} />
        <TimeSlider
          startDate={startDate}
          onStartDateChange={onStartDateChange}
        />
      </div>
    </>
  );
}
