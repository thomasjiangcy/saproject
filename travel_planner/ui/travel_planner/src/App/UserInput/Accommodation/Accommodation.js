import React, { Component } from "react";

import './Accommodation.css';
import PlacesAutocomplete, {
  geocodeByAddress,
  getLatLng
} from "react-places-autocomplete";

class Accommodation extends Component {
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
      .then(latLng => this.props.accommodationHandler(latLng.lat, latLng.lng))
      .catch(error => console.error("Error", error));
    this.setState({ address });
  }

  render() {
    const inputProps = {
      value: this.state.address,
      onChange: this.changeHandler,
      debounce: 1500,
      placeholder: 'Accommodation Address'
    };

    const renderSuggestion = ({ suggestion }) => (
      <div className="suggestion-item">
        <i className="fa fa-map-marker" style={{ marginRight: '15px' }}/>{suggestion}
      </div>
    );

    return (
      <PlacesAutocomplete
        inputProps={inputProps}
        styles={{
          root: {
            width: '100%',
          }
        }}
        classNames={{
          root: 'input-group input-group-lg',
          input: 'form-control'
        }}
        renderSuggestion={renderSuggestion}
      />
    );
  }
}

export default Accommodation;
