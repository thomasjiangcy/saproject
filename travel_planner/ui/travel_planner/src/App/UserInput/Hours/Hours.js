import React from "react";

const hours = props => (
  <div className="input-group input-group-lg">
    <input
      className="form-control"
      type="text"
      value={props.value}
      onChange={props.hoursHandler}
      placeholder="Time in Singapore"
      required
    />
    <div className="input-group-append">
      <span className="input-group-text" id="basic-addon2">hours</span>
    </div>
  </div>
);

export default hours;
