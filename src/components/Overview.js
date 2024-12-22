import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

function Overview() {
  const [sankeyData, setSankeyData] = useState(null);

  useEffect(() => {
    fetch('/api/sankey')
      .then(response => response.json())
      .then(data => setSankeyData(JSON.parse(data)))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div>
      <h1>Warehouse Process Flow</h1>
      {sankeyData && (
        <Plot
          data={sankeyData.data}
          layout={sankeyData.layout}
          config={{responsive: true}}
        />
      )}
    </div>
  );
}

export default Overview;