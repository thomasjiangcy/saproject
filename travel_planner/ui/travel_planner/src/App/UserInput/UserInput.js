import React from "react";

import './UserInput.css';
import Accommodation from './Accommodation/Accommodation';
import Hours from "./Hours/Hours";
import Preferences from "./Preferences/Preferences";

const userInput = props => (
  <div className="container-fluid">
    <div className="row">
      <Hours value={props.hours} hoursHandler={props.hoursHandler} />
    </div>
    <div className="row">
      <Accommodation accommodationHandler={props.accommodationHandler} />
    </div>
    <div className="row">
      <Preferences
        value={props.preferences}
        preferencesHandler={props.preferencesHandler}
      />
    </div>
  </div>
);

export default userInput;
