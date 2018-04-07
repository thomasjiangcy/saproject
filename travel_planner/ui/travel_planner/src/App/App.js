import React, { Component } from "react";
import axios from "axios";

import "./App.css";
import Header from "./Header/Header";
import Loader from "./Loader/Loader";
import Results from "./Results/Results";
import UserInput from "./UserInput/UserInput";

const request = axios.create({
  baseURL: "http://localhost"
});

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hours: "",
      preferences: "",
      accommodation: {
        lat: "",
        lng: ""
      },
      loading: false,
      results: []
    };

    this.hoursHandler = this.hoursHandler.bind(this);
    this.preferencesHandler = this.preferencesHandler.bind(this);
    this.accommodationHandler = this.accommodationHandler.bind(this);
    this.submitHandler = this.submitHandler.bind(this);
  }

  hoursHandler(event) {
    this.setState({ hours: event.target.value });
  }

  preferencesHandler(event) {
    this.setState({ preferences: event.target.value });
  }

  accommodationHandler(lat, lng) {
    const accommodation = {
      lat,
      lng
    };
    this.setState({ accommodation });
  }

  submitHandler(event) {
    event.preventDefault();
    this.setState({ loading: true, results: [] });
    request
      .post("/api/plan/", {
        hours: this.state.hours,
        accommodation: this.state.accommodation,
        preferences: this.state.preferences
      })
      .then(res => {
        console.log(res.data);
        this.setState({ loading: false, results: res.data });
      })
      .catch(err => {
        this.setState({ loading: false });
      });
  }

  render() {
    let button;
    let results;

    if (this.state.loading) {
      button = <Loader />;
    } else {
      button = (
        <button
          type="button"
          className="btn btn-primary"
          onClick={this.submitHandler}
        >
          Submit
        </button>
      );
    }

    if (this.state.results) {
      results = (
        <Results
          results={this.state.results}
          accommodation={this.state.accommodation}
        />
      );
    }

    return (
      <div className="App">
        <div className="container">
          <div className="row">
            <Header />
          </div>
          <div className="user-input">
            <div className="row">
              <UserInput
                hours={this.state.hours}
                hoursHandler={this.hoursHandler}
                preferences={this.state.preferences}
                preferencesHandler={this.preferencesHandler}
                accommodationHandler={this.accommodationHandler}
              />
            </div>
            <div className="row">{button}</div>
          </div>
          <div className="row">{results}</div>
        </div>
      </div>
    );
  }
}

export default App;
