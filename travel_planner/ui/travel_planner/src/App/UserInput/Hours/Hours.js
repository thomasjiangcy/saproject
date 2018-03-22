import React from "react";

const hours = props => (
  <div>
    <input
      type="number"
      placeholder="Hours"
      value={props.value}
      onChange={props.hoursHandler}
    />
  </div>
);

export default hours;
