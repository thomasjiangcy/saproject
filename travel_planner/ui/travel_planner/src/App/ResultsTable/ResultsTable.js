import React, { Component } from 'react';

class ResultsTable extends Component {
  constructor (props) {
    super(props);
    this.state = {
      topics : {
        0 : 'Shopping & Food',
        1 : 'Western Food',
        2 : 'Waffles & Coffee',
        3 : 'Local Delights',
        4 : 'Fine Dining & Living',
        5 : 'South-East Asian Cuisine',
        6 : 'Dessert',
        7 : 'Dessert',
        8 : 'Coffee',
        9 : 'Seafood'
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
          if (location.topic_distribution[topic] > 0) {
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
