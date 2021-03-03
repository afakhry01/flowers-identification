import React, { Fragment } from 'react';


const Result = ({classification}) => {
  return (
    <div>
      <span>This image contains:</span>
      <span>{classification}</span>
    </div>
  );
}
 
export default Result;