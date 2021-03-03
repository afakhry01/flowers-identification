import 'semantic-ui-css/semantic.min.css';
import './App.css';
import { Segment } from 'semantic-ui-react';
import Classifier from './components/classifier/Classifier';

function App() {
  return (
    <div className="App-header">
      <Segment className="App-segment">
        <Classifier />
      </Segment>
    </div>
  );
}

export default App;
