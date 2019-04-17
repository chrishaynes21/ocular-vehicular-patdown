import React from 'react';
import { Jumbotron } from 'reactstrap';

const Jumbo = (props) => {
  return (
    <div>
      <Jumbotron style={{textAlign: 'center'}}>
        <h1 className="display-3">Ocular Vehicular Patdown</h1>
        <p className='lead'>This simple web application will accept an image and attempt to classify the vehicle features.</p>
      </Jumbotron>
    </div>
  );
};

export default Jumbo;