import React from "react";

import Accomodation from "./Accomodation/Accomodation";
import Hours from "./Hours/Hours";
import Preferences from "./Preferences/Preferences";

const userInput = props => (
  <React.Fragment>
    <Hours value={props.hours} hoursHandler={props.hoursHandler} />
    <Preferences
      value={props.preferences}
      preferencesHandler={props.preferencesHandler}
    />
    <Accomodation accomodationHandler={props.accomodationHandler} />
  </React.Fragment>
);

export default userInput;
