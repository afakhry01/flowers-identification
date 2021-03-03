import React, { useState, useEffect } from 'react';


const styling = {
  placeholder: {
    width: '300px'
  },
  image: {
    width: '100%',
    maxWidth: '300px', 
    height: 'auto' 
  }
}

const ImageUpload = ({image, setImage}) => {
  const [selectedFile, setSelectedFile] = useState()

  useEffect(() => {
    if (!selectedFile) {
      setImage(undefined)
      return
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      setImage(btoa(e.target.result))
    };
    reader.readAsBinaryString(selectedFile)
  }, [selectedFile])

  const onSelectFile = e => {
    if (!e.target.files || e.target.files.length === 0) {
      setSelectedFile(undefined)
      return
    }

    setSelectedFile(e.target.files[0])
  }

  return (
    <div>
      {selectedFile ? (
        <img src={"data:image/png;base64,"+image} style={styling.image}/>
      ) : (
        <div style={styling.placeholder}>
          No image selected
        </div>
      )}
      <input type='file' onChange={onSelectFile} />
    </div>
  )
}

export default ImageUpload;
