import React, {Component} from 'react';
import Jumbo from "./Jumbo";
import TopNav from "./Nav";
import Loader from "./Loader";

class App extends Component {
    render() {
        return (
            <div>
                <header>
                    <TopNav/>
                </header>
                <Jumbo/>
                <Loader/>
            </div>
        );
    }
}

export default App;
