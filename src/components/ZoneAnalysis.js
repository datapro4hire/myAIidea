import React, { useState, useEffect } from 'react';

function ZoneAnalysis() {
  const [zone, setZone] = useState('Zone A');
  const [zoneData, setZoneData] = useState(null);

  useEffect(() => {
    fetch(`/api/zone?zone=${zone}`)
      .then(response => response.json())
      .then(data => setZoneData(data))
      .catch(error => console.error('Error:', error));
  }, [zone]);

  return (
    <div>
      <h1>Zone Performance</h1>
      <select value={zone} onChange={(e) => setZone(e.target.value)}>
        <option value="Zone A">Zone A</option>
        <option value="Zone B">Zone B</option>
        <option value="Zone C">Zone C</option>
        <option value="Zone F">Zone F</option>
      </select>
      {zoneData && (
        <div>
          {zoneData.metrics.map((metric, index) => (
            <div key={index}>
              <h3>{metric.label}</h3>
              <p>{metric.value}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ZoneAnalysis;