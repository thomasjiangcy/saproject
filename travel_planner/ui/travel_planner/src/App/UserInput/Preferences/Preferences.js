import React from "react";

const preferences = props => (
  <div>
    <textarea
      placeholder="Preferences"
      value={props.value}
      onChange={props.preferencesHandler}
    />
  </div>
);

export default preferences;
