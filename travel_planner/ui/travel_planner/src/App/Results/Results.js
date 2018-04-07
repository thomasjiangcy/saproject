/*global google*/
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Gmaps, Marker } from 'react-gmaps';

const coords = {lat: 1.352083, lng: 103.81983600000001};
const params = {v: '3.exp', key: 'AIzaSyC-id3XdWbVyQBoe3_e2-T5fAGdVdkPxZg'};

class Results extends Component {
  constructor (props) {
    super(props);
    this.state = {
      directionsDisplay : null,
      directionsService : null,
      map               : null,
      directions        : null,
      data              : props.results.data
    };

    this.onMapCreated = this.onMapCreated.bind(this);
  }

  componentWillReceiveProps (nextProps) {
    this.setState({
      data : nextProps.results.data
    });
  }

  componentDidUpdate () {
    const { directionsService, directionsDisplay, map } = this.state;
    if (directionsService && directionsDisplay && map && this.state.data) {
      const origin = new google.maps.LatLng(this.props.accommodation.lat, this.props.accommodation.lng);
      const destination = this.state.data[ this.props.results.data.length -1 ];
      const waypoints = [];
      this.state.data.forEach((location, index) => {
        if (index !== this.state.data.length - 1 ) {
          waypoints.push({
            location: {
              lat: location.lat,
              lng: location.lng
            },
            stopover: true
          });
        }
      });
      directionsService.route({
        origin: origin,
        destination: destination,
        waypoints: waypoints,
        travelMode: 'DRIVING',
      }, (result, status) => {
        if (status === 'OK') {
          this.setState({
            directions: result,
          });
          directionsDisplay.setDirections(result);
        } else {
          console.log(status);
        }
      });
    }
  }

  onMapCreated (map) {
    const directionsDisplay = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    this.setState({ directionsDisplay, directionsService, map });
    directionsDisplay.setMap(map);
  }

  render () {
    const markers = this.props.results.data ? this.props.results.data.map(location => (
      <Marker
        key={location.id}
        lat={location.lat}
        lng={location.lng}
      />
    )) : null;
  
    return (
      <Gmaps
        width={'800px'}
        height={'600px'}
        zoom={11}
        lat={coords.lat}
        lng={coords.lng}
        params={params}
        onMapCreated={this.onMapCreated}
      >
        {markers}
      </Gmaps>
    );
  }
}

export default Results;
