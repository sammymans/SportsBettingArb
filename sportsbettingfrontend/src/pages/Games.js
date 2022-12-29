import '../App.css';

// Need Acios and useState/useEffect to call from FastAPI and display 
import axios from 'axios';
import {useState, useEffect} from 'react';

import Card from 'react-bootstrap/Card'


function Games() {

  const [opportunity, setOpportunity] = useState([]);

  useEffect(()=> {
    axios.get('/api').then(res => setOpportunity(res.data));
  }, []);
  // Mapping the list of opportunities that was called, each in its own Card
  return opportunity.map((o, index) => {
    return <Card 
    key={index}
    border= "primary"
    > 
    <Card.Body>
      On {o.bookkeeper1} bet ${o.amount1} for {o.team1} and
      on {o.bookkeeper2} bet ${o.amount2} for {o.team2}
    </Card.Body>
    </Card>
  }) 

}

export default Games;