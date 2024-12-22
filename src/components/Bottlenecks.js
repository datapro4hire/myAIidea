import React, { useState, useEffect } from 'react';

function Bottlenecks() {
  const [bottleneckType, setBottleneckType] = useState('Equipment');
  const [bottleneckData, setBottleneckData] = useState(null);

  useEffect(() => {
    fetch(`/api/bottlenecks?type=${bottleneckType}`)
      .then(response => response.json())
      .then(data => setBottleneckData(data))
      .catch(error => console.error('Error:', error));
  }, [bottleneckType]);

  return (
    <div>
      <h1>Bottleneck Analysis</h1>
      <select value={bottleneckType} onChange={(e) => setBottleneckType(e.target.value)}>
        <option value="Equipment">Equipment</option>
        <option value="Traffic">Traffic</option>
        <option value="Processing">Processing</option>
        <option value="Temperature Control">Temperature Control</option>
      </select>
      {bottleneckData && (
        <div>
          <h2>{bottleneckData.title}</h2>
          {bottleneckData.metrics.map((metric, index) => (
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

export default Bottlenecks;