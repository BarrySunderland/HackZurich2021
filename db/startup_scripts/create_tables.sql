CREATE TABLE IF NOT EXISTS rssi (
  "ID" BIGINT PRIMARY KEY,
  "created_at" timestamp without time zone default now(), 
  "DateTime" TIMESTAMP without time zone,
  "AreaNumber" SMALLINT,
  "Track" SMALLINT,
  "Position" INTEGER,
  "PositionNoLeap" INTEGER,
  "Latitude" DOUBLE PRECISION,
  "Longitude" DOUBLE PRECISION,
  "A1_TotalTel" DOUBLE PRECISION,
  "A1_ValidTel" DOUBLE PRECISION,
  "A2_RSSI" DOUBLE PRECISION,
  "A2_TotalTel" DOUBLE PRECISION,
  "A2_ValidTel" DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS "rssi_mean" (
  "ID" BIGINT PRIMARY KEY,
  "created_at" TIMESTAMP without time zone default now(), 
  "Date" TIMESTAMP without time zone,
  "PositionNoLeap" INTEGER,
  "Latitude" DOUBLE PRECISION,
  "Longitude" DOUBLE PRECISION,
  "A1_TotalTel" DOUBLE PRECISION,
  "A1_ValidTel" DOUBLE PRECISION,
  "A2_RSSI" DOUBLE PRECISION,
  "A2_TotalTel" DOUBLE PRECISION,
  "A2_ValidTel" DOUBLE PRECISION
);

