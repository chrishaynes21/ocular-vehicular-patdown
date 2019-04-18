import React from 'react';
import {Button, Row, Col,Container} from 'reactstrap';

class Loader extends React.Component {
    constructor(props) {
        super(props);
        this.state = { activeButton: null}
    }

    handleDecadeChange() {
        this.setState({activeButton: 'decade'})
    }

    handleBodyChange() {
        this.setState({activeButton: 'bodystyle'})
    }

    handlePriceChange() {
        this.setState({activeButton: 'price'})
    }

    render() {
        return (
            <div>
                <Container>
                    <Row>
                        <Col>
                            <Button color={this.state.activeButton === 'decade' ? 'primary' : 'secondary'} size={'lg'}
                                    block onClick={this.handleDecadeChange.bind(this)}>
                                Decade
                            </Button>
                        </Col>
                        <Col>
                            <Button color={this.state.activeButton === 'bodystyle' ? 'primary' : 'secondary'} size={'lg'}
                                     block onClick={this.handleBodyChange.bind(this)}>
                                Body Style
                            </Button>
                        </Col>
                        <Col>
                            <Button color={this.state.activeButton === 'price' ? 'primary' : 'secondary'} size={'lg'}
                                     block onClick={this.handlePriceChange.bind(this)}>
                                Price
                            </Button>
                        </Col>
                    </Row>
                </Container>
            </div>
        )
    };
}

export default Loader;