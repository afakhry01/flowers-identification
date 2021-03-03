import React, { Fragment, useState } from 'react';
import ImageUpload from './ImageUpload';
import Result from './Result';
import Submit from './Submit';
import Title from './Title';


const Classifier = () => {
  const [image, setImage] = useState();
  const [classification, setClassification] = useState();

  return (
    <Fragment>
      <Title />
      <ImageUpload
        image={image}
        setImage={setImage}
      />
      <Submit
        image={image}
        setClassification={setClassification}
      />
      <Result
        classification={classification}
      />
    </Fragment>
  );
}
 
export default Classifier;