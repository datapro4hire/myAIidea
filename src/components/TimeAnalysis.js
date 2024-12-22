import React from 'react';

function TimeAnalysis({ data }) {
  return (
    <div>
      <h1>Time Analysis</h1>
      {data ? (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Task Type</th>
              <th>Quantity</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row.date}</td>
                <td>{row.task_type}</td>
                <td>{row.quantity}</td>
                <td>{row.start_time}</td>
                <td>{row.end_time}</td>
                <td>{row.notes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No data available. Please upload a log file.</p>
      )}
    </div>
  );
}

export default TimeAnalysis;