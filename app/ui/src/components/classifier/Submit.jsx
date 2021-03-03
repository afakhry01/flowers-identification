import React from 'react';
import { Button } from 'semantic-ui-react';
import axios from 'axios';

const Submit = ({image, setClassification}) => {
  const handleSubmit = () => {
    axios.post('/api/flowers/classify/', {image: image})
    .then(res => {
      setClassification(res.data.classification)
    })
    .catch(err => {
      console.log(err)
    })
  }

  return (
    <Button
      content='Submit'
      onClick={() => handleSubmit()}
    />
  );
}
 
export default Submit;