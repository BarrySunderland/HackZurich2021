import React from "react";

export default function Chart({ visible }) {
  return (
    <div
      style={{
        width: "100%",
        height: 800,
        marginLeft: 10,
      }}
    >
      <h4
        style={{
          color: "grey",
          marginLeft: 10,
          marginTop: 20,
          marginBottom: 25,
        }}
      >
        Graph
      </h4>
      <div style={{ width: 800 }}>
        <div id="mychart" key={visible} />
      </div>
    </div>
  );
}
