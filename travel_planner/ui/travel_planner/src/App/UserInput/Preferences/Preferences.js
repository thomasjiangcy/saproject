import React from "react";

const preferences = props => (
  <div className="input-group input-group-lg">
    <textarea
      className="form-control"
      value={props.value}
      onChange={props.preferencesHandler}
      required
      placeholder="Tell us what you would like to do in Singapore :)"
    />
  </div>
);

export default preferences;
