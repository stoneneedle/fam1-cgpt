// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import React, { useState, useEffect } from 'react';

const App = () => {
  const [examples, setExamples] = useState([]);

  useEffect(() => {
    const fetchExamples = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/example', {
          credentials: 'include',
        });  // Update with your Flask API endpoint
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setExamples(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchExamples();
  }, []);  // The empty dependency array ensures the effect runs once when the component mounts

  return (
    <div>
      <h1>Examples from Flask API</h1>
      <ul>
        {examples.map((example) => (
          <li key={example.id}>{example.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;