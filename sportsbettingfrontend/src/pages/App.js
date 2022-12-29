import '../App.css';
import './Games.js'
import Button from '../Button';

// Home page prompting user to click a button that will take them to opportunities
function App() {

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Clicking the button below will show multiple Arbitrage Opportunities
        </p>
        <Button/>
      </header>
    </div>
  );
}

export default App;
