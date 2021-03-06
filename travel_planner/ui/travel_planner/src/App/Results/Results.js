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

    this.isEqual = this.isEqual.bind(this);
    this.onMapCreated = this.onMapCreated.bind(this);
  }

  shouldComponentUpdate (nextProps) {
    const thisData = this.props.results.data;
    const nextData = nextProps.results.data;
    return !this.isEqual(thisData, nextData);
  }

  componentWillReceiveProps (nextProps) {
    this.setState({
      data : nextProps.results.data
    });
  }

  componentDidUpdate () {
    const { directionsService, directionsDisplay, map } = this.state;
    if (directionsService && directionsDisplay && map && this.state.data) {
      const origin = { lat: this.props.accommodation.lat, lng: this.props.accommodation.lng};
      const destinationData = this.state.data[ this.props.results.data.length -1 ];
      const destination = { lat: destinationData.lat, lng: destinationData.lng };
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
      console.log('[Origin] ', origin);
      console.log(waypoints);
      console.log('[Destination] ', destination);
      directionsService.route({
        origin: origin,
        destination: destination,
        waypoints: waypoints,
        travelMode: 'DRIVING'
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

  isEqual(arr1, arr2) {
    if (arr1 && arr2) {
      for (let i = 0; i < arr1.length; i++) {
        if (arr1[ i ].id !== arr2[ i ].id) {
          return false;
        }
      }
      return true;
    }
    return false;
  }

  onMapCreated (map) {
    const directionsDisplay = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    this.setState({ directionsDisplay, directionsService, map });
    directionsDisplay.setMap(map);
  }

  render () {
    const markers = null;
  
    return (
      <Gmaps
        width={'50%'}
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
