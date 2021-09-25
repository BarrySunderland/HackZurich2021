import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
//348ceb
const ExampleCustomInput = React.forwardRef(({ value, onClick }, ref) => (
  <h1
    className="example-custom-input"
    style={{ color: "grey", marginLeft: 380 }}
    onClick={onClick}
    ref={ref}
  >
    {value}
  </h1>
));

function formatDate(date) {
  var d = new Date(date),
    month = "" + (d.getMonth() + 1),
    day = "" + d.getDate(),
    year = d.getFullYear();

  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;

  return [year, month, day].join("-");
}

export default function TimeSlider({ startDate, onStartDateChange }) {
  return (
    <div>
      <DatePicker
        popperPlacement="bottom-end"
        selected={startDate}
        onChange={onStartDateChange}
        customInput={<ExampleCustomInput />}
      />
    </div>
  );
}
