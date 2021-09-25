import axios from "axios";
import { actual, data, predicted } from "../fakeData";

const HOSTNAME = "http://localhost:5000";

export const getPlugin = async () => {
  const response = await axios.get(`${HOSTNAME}/plot/sensor`, {
    headers: { "Access-Control-Allow-Origin": "*" },
  });
  console.log("AMM", response);
  return response.data;
};

export const getPredictedFailures = async (time) => {
  try {
    return predicted;
    const response = await axios.get(
      `${HOSTNAME}/api/failures/predicted/${time}`,
      {
        headers: { "Access-Control-Allow-Origin": "*" },
      }
    );
    return [];
    return response.status === 200 ? response.data : null;
  } catch (err) {
    console.error(err);
    return null;
  }
};

export const getActualFailures = async (id) => {
  try {
    return actual;

    const response = await axios.get(`${HOSTNAME}/api/coordinates/${id}`, {
      headers: { "Access-Control-Allow-Origin": "*" },
    });
    return actual;
    return [];
    return response.status === 200 ? response.data : null;
  } catch (err) {
    console.error(err);
    return null;
  }
  ///
};
