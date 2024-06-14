import './App.css';
import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState('');

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    alert(`Submitted: ${input}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        Fitness Ai App
      </header>
      <main className="App-main">
        <div className="App-container">
          <h2>Input Food Here:</h2>
          <form onSubmit={handleSubmit}>
            <textarea
              value={input}
              onChange={handleInputChange}
              className="App-textarea"
            />
            <button type="submit" className="App-button">Submit</button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;
