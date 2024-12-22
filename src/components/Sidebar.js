import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar({ onFileUpload }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <aside className="sidebar">
      <h2>Warehouse Workflow Analysis</h2>
      <input
        type="file"
        accept=".txt"
        onChange={handleFileChange}
      />
      <nav>
        <ul>
          <li><Link to="/">Overview</Link></li>
          <li><Link to="/bottlenecks">Bottlenecks</Link></li>
          <li><Link to="/zone-analysis">Zone Analysis</Link></li>
          <li><Link to="/time-analysis">Time Analysis</Link></li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;