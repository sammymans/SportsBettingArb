import React from 'react';
import { Switch, Route } from 'react-router-dom';

import App from './pages/App';
import Games from './pages/Games';



// Required to have multiple Routes to different pages
const Main = () => {
  return (
    <Switch> {/* The Switch decides which component to show based on the current URL.*/}
      <Route exact path='/' component={App}></Route>
      <Route exact path='/Games' component={Games}></Route>
    </Switch>
  );
}

export default Main;