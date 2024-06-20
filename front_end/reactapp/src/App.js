import './App.css';
import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [foodData, setFoodData] = useState({ foodList: [], calorieList: [], proteinList: [] });

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      const response = await fetch('http://localhost:8001/aifitnessapp/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: input }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      console.log(responseData)
      setFoodData((prevFoodData) => ({
        foodList: [...prevFoodData.foodList, ...responseData.foodList],
        calorieList: [...prevFoodData.calorieList, ...responseData.calorieList],
        proteinList: [...prevFoodData.proteinList, ...responseData.proteinList],
      }));
      // alert(`Response: ${JSON.stringify(responseData)}`);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  };

  const totalCalories = foodData.calorieList.reduce((total, calories) => total + parseFloat(calories), 0);
  const totalProtein = foodData.proteinList.reduce((total, protein) => total + parseFloat(protein), 0);

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
          <div className="Summary">
            <h3>Total Calories: {totalCalories}</h3>
            <h3>Total Protein: {totalProtein}g</h3>
          </div>
          <div className="Food-cards">
            {foodData.foodList?.map((food, index) => (
              <div key={index} className="Food-card">
                <h3>{food}</h3>
                <p>Calories: {foodData.calorieList[index]}</p>
                <p>Protein: {foodData.proteinList[index]}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
