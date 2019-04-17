import React from 'react';
import {Button, Row, Col,Container} from 'reactstrap';

class Loader extends React.Component {
    render() {
        return (
            <div>
                <Container>
                    <Row>
                        <Col>
                            <Button size={'lg'} block>Decade</Button>
                        </Col>
                        <Col>
                            <Button size={'lg'} block>Body Style</Button>
                        </Col>
                        <Col>
                            <Button size={'lg'} block>Price</Button>
                        </Col>
                    </Row>

                </Container>
            </div>
        )
    };
}

export default Loader;