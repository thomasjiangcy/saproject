import React, { Component } from 'react';

class ResultsTable extends Component {
  constructor (props) {
    super(props);
    this.state = {
      topics : {
        0 : 'Bar & Grill',
        1 : 'Seafood',
        2 : 'Nightlife',
        3 : 'Local Delights',
        4 : 'Tourist Attractions',
        5 : 'Dessert',
        6 : 'Quick Bites',
        7 : 'Shopping',
        8 : 'Muslim Cuisine',
        9 : 'Chinese Cuisine'
      }
    };
    
    this.getTopicName = this.getTopicName.bind(this);
  }

  getTopicName (topic) {
    return this.state.topics[ topic ];
  }

  render () {
    let results = (
      <span>No results</span>
    );
    if (this.props.results.data) {
      results = this.props.results.data.map((location, i) => {
        const labels = Object.keys(location.topic_distribution).map(topic => {
          if (location.topic_distribution[topic] > 0.1) {
            return (
              <div className="label" key={topic}>
                {this.getTopicName(topic)}
              </div>
            );
          }
          return null;
        });

        return (
          <div className="row" key={location.id}>
            <div className={`location ${i === 0 ? "" : "with-top"}`}>
              <div className="name">{location.name}</div>
              <div className="labels">
                {labels}
              </div>
            </div>
          </div>
        );
      });
    }

    return (
      <div className="results-table">
        <div className="container-fluid">
          {results}
        </div>
      </div>
    );
  }
}

export default ResultsTable;
