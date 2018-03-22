import React, { Component } from "react";

import Header from "./Header/Header";
import Loader from './Loader/Loader';
import Results from "./Results/Results";
import UserInput from "./UserInput/UserInput";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hours: "",
      preferences: "",
      accomodation: {
        lat: "",
        lng: ""
      },
      loading: true,
      results: null
    };

    this.hoursHandler = this.hoursHandler.bind(this);
    this.preferencesHandler = this.preferencesHandler.bind(this);
    this.accomodationHandler = this.accomodationHandler.bind(this);
    this.submitHandler = this.submitHandler.bind(this);
  }

  hoursHandler(event) {
    this.setState({ hours: event.target.value });
  }

  preferencesHandler(event) {
    this.setState({ preferences: event.target.value });
  }

  accomodationHandler(lat, lng) {
    const accomodation = {
      lat,
      lng
    };
    this.setState({ accomodation });
  }

  submitHandler(event) {
    event.preventDefault();
    console.log(this.state);
  }

  render() {
    let results;
    
    if (this.state.results) {
      results = <Results results={this.state.results} />;
    } else if (this.state.loading) {
      results = <Loader />;
    }

    return (
      <div className="App">
        <Header />
        <UserInput
          hours={this.state.hours}
          hoursHandler={this.hoursHandler}
          preferences={this.state.preferences}
          preferencesHandler={this.preferencesHandler}
          accomodationHandler={this.accomodationHandler}
        />
        <button type="button" onClick={this.submitHandler}>
          Submit
        </button>
        {results}
      </div>
    );
  }
}

export default App;
