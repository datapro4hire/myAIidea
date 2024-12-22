import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Overview from './components/Overview';
import Bottlenecks from './components/Bottlenecks';
import ZoneAnalysis from './components/ZoneAnalysis';
import TimeAnalysis from './components/TimeAnalysis';
import './App.css';

function App() {
  const [data, setData] = useState(null);

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('File upload failed');
      }

      const result = await response.json();
      setData(result.data);
      alert(result.message);
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while uploading the file.');
    }
  };

  return (
    <Router>
      <div className="App">
        <Sidebar onFileUpload={handleFileUpload} />
        <main>
          <Switch>
            <Route exact path="/" component={Overview} />
            <Route path="/bottlenecks" render={() => <Bottlenecks data={data} />} />
            <Route path="/zone-analysis" render={() => <ZoneAnalysis data={data} />} />
            <Route path="/time-analysis" render={() => <TimeAnalysis data={data} />} />
          </Switch>
        </main>
      </div>
    </Router>
  );
}

export default App;