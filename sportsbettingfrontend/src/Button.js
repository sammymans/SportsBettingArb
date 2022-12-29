import { useNavigate } from 'react-router-dom';
import './App.css';



function Button() {
  // Creating variable to make it easier to navigate
    const navigate = useNavigate()
  return (
    <div className="App">
        <button style=
        {{
            fontSize: '20px',
            padding: '10px 20px'
        }}
        // Navigating to new page once clicked, sincle only one button, can have the exact Route here
        className="btn" onClick = {() => {navigate("/ArbitrageOpps")}}>  
        Show Arbitrage Opportunities </button>
    </div>
  );
}

export default Button;
