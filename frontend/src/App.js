import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import TopBar from "./components/TopBar";
import Map from "./components/Map";
import RightBar from "./components/RightBar";
import Chart from "./components/Chart";
import {
  getActualFailures,
  getPredictedFailures,
  getPlugin,
} from "./utils/apis";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
const DEFAULT_CENTER = {
  lat: 47.30471,
  lng: 8.05152,
};
const DEFAULT_DATE = new Date();

function App() {
  const [actualFailures, setActualFailures] = useState([]);
  const [predictedFailures, setPredictedFailures] = useState([]);
  const [startDate, setStartDate] = useState(DEFAULT_DATE);
  const [zoom, setZoom] = useState(10);
  const [chart, setChart] = useState(true);
  const [center, setCenter] = useState(DEFAULT_CENTER);
  let i = 0;

  React.useEffect(() => {
    (async () => {
      const predictedFailures = await getPredictedFailures(startDate);
      if (predictedFailures) {
        setPredictedFailures(predictedFailures);
      }
      const actualFailures = await getActualFailures(startDate);
      console.log("my acc", actualFailures);
      if (actualFailures) {
        setActualFailures(actualFailures);
      }
    })();
  }, [startDate]); // Pass in empty array to run useEffect only on mount.

  const onChartShow = async () => {
    const myPlugin = await getPlugin();
    console.log("my plug", myPlugin);
    window.Bokeh.embed.embed_item(myPlugin, "mychart");
    setChart(true);
  };

  const onZoom = (lat, lng) => {
    setZoom(1);
    setCenter({
      lat,
      lng,
    });
  };
  return (
    <div
      style={{ backgroundColor: "#eee", minHeight: "100vh", paddingLeft: 50 }}
    >
      <TopBar
        actualFailures={actualFailures}
        predictedFailures={predictedFailures}
        startDate={startDate}
        onStartDateChange={(date) => setStartDate(date)}
      />
      <div className="d-flex flex-row">
        {chart ? (
          <Chart visible={chart} />
        ) : (
          <Map
            actualFailures={actualFailures}
            predictedFailures={predictedFailures}
            zoom={zoom}
            center={center}
            key={center}
          />
        )}
        <RightBar
          actualFailures={actualFailures}
          predictedFailures={predictedFailures}
          onZoom={onZoom}
          onChartOpen={onChartShow}
        />
      </div>
    </div>
  );
}

export default App;
