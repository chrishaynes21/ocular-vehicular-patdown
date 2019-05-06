import React from 'react';
import {Button, Col, Container, Form, FormGroup, FormText, Input, Row} from 'reactstrap';

class Loader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeButton: null,
            file: null,
            fileGetter: null
        };

        this.handleTypeChange = this.handleTypeChange.bind(this);
        this.submitImage = this.submitImage.bind(this);
    }

    handleTypeChange(activeButton) {
        this.setState({activeButton: activeButton})
    }

    fileChanged(e) {
        this.setState({file: e.target.files[0]});
    }

    handleErrors(response) {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response;
    }

    submitImage() {
        const imageData = new FormData();
        imageData.append('file', this.state.file);

        fetch(`http://127.0.0.1:5000/upload`, {
            mode: 'cors',
            method: 'POST',
            body: imageData,
        })
            .then((response) => this.handleErrors(response))
            .then((response) => {
                response.json().then((fileName) => {
                    this.setState({
                        fileGetter: fileName
                    });
                })
            })
            .catch((error) => console.log(error));
    }

    render() {
        return (
            <div>
                <Container>
                    <Row>
                        <Col style={{marginRight: '50px'}}>
                            <Row style={{marginBottom: '25px'}}>
                                <Button color={this.state.activeButton === 'decade' ? 'primary' : 'secondary'}
                                        size={'lg'}
                                        block onClick={() => this.handleTypeChange('decade')}>
                                    Decade
                                </Button>
                            </Row>
                            <Row style={{marginBottom: '25px'}}>
                                <Button color={this.state.activeButton === 'bodystyle' ? 'primary' : 'secondary'}
                                        size={'lg'}
                                        block onClick={() => this.handleTypeChange('bodystyle')}>
                                    Body Style
                                </Button>
                            </Row>
                            <Row style={{marginBottom: '25px'}}>
                                <Button color={this.state.activeButton === 'price' ? 'primary' : 'secondary'}
                                        size={'lg'}
                                        block onClick={() => this.handleTypeChange('price')}>
                                    Price
                                </Button>
                            </Row>
                        </Col>
                        <Col>
                            <Row>
                                <Form>
                                    <FormGroup row>
                                        <Input type="file" name="image" id="classifyImage"
                                               onChange={(event) => this.fileChanged(event)}/>
                                        <FormText color="muted">
                                            Select an image to classify!
                                        </FormText>
                                    </FormGroup>
                                </Form>
                            </Row>
                            <Row>
                                <Button className="float-left" color={this.state.file ? 'success' : 'secondary'}
                                        disabled={!this.state.file} onClick={this.submitImage}>
                                    Submit
                                </Button>
                            </Row>
                        </Col>
                        {this.state.file ? (
                            <Col>
                                <img style={{maxWidth: '75%'}}
                                     src={URL.createObjectURL(this.state.file)}
                                     alt='Hopefully a car'/>
                            </Col>
                        ) : undefined}
                    </Row>
                </Container>
            </div>
        )
    };
}

export default Loader;