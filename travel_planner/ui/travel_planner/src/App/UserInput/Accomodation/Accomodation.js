import React, { Component } from "react";

import PlacesAutocomplete, {
  geocodeByAddress,
  getLatLng
} from "react-places-autocomplete";

class Accomodation extends Component {
  constructor(props) {
    super(props);
    this.state = {
      address: ""
    };

    this.changeHandler = this.changeHandler.bind(this);
  }

  changeHandler(address) {
    geocodeByAddress(this.state.address)
      .then(results => getLatLng(results[0]))
      .then(latLng => this.props.accomodationHandler(latLng.lat, latLng.lng))
      .catch(error => console.error("Error", error));
    this.setState({ address });
  }

  render() {
    const inputProps = {
      value: this.state.address,
      onChange: this.changeHandler,
      debounce: 1000,
      placeholder: 'Your Accomodation Address'
    };
    return <PlacesAutocomplete inputProps={inputProps} highlightFirstSuggestion />;
  }
}

export default Accomodation;
