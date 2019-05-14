import React from 'react';
import {Button, Col, Container, Form, FormGroup, FormText, Input, Row} from 'reactstrap';

class Loader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeButton: null,
            file: null,
            loading: true,
            classification: undefined
        };

        this.handleTypeChange = this.handleTypeChange.bind(this);
        this.submitImage = this.submitImage.bind(this);
        this.resetLoader = this.resetLoader.bind(this);
    }

    handleTypeChange(activeButton) {
        this.setState({activeButton: activeButton})
    }

    fileChanged(e) {
        this.setState({file: e.target.files[0]});
    }

    static handleErrors(response) {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response;
    }

    // Submit the image uploaded to the server. Then call getClassification()
    submitImage() {
        const imageData = new FormData();
        imageData.append('file', this.state.file);

        if (this.state.activeButton) {
            fetch(`http://127.0.0.1:5000/upload`, {
                mode: 'cors',
                method: 'POST',
                body: imageData,
            })
                .then((response) => Loader.handleErrors(response))
                .then((response) => {
                    response.json().then((fileName) => {
                        this.setState({
                            fileGetter: fileName,
                        });
                        this.getClassification(fileName);
                    })
                })
                .catch(() => alert('An error occurred, are you sure your image is a .JPG or .JPEG?'));
        } else {
            alert('Classification must be chosen before submitting.')
        }
    }

    // Get the classification back and display it on the web page
    getClassification(fileName) {
        const requestObject = {
            fileName: fileName,
            classification: this.state.activeButton
        };
        const query = Object.keys(requestObject).map(key => key + '=' + requestObject[key]).join('&');
        fetch('http://127.0.0.1:5000/classification?' + query, {
            mode: 'cors',
            method: 'GET',
        })
            .then((response) => Loader.handleErrors(response))
            .then((response) => {
                response.json().then((classification) => {
                    console.log(classification);
                    this.setState({
                        loading: false,
                        classification: classification,
                    });
                })
            })
            .catch((error) => console.log(error));
    }

    resetLoader() {
        this.setState({
            loading: 'true',
        })
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
                                        block onClick={() => this.handleTypeChange('decade')}
                                        disabled={!this.state.loading}>
                                    Decade
                                </Button>
                            </Row>
                            <Row style={{marginBottom: '25px'}}>
                                <Button color={this.state.activeButton === 'bodystyle' ? 'primary' : 'secondary'}
                                        size={'lg'}
                                        block onClick={() => this.handleTypeChange('bodystyle')}
                                        disabled={!this.state.loading}>
                                    Body Style
                                </Button>
                            </Row>
                            <Row style={{marginBottom: '25px'}}>
                                <Button color={this.state.activeButton === 'make' ? 'primary' : 'secondary'}
                                        size={'lg'}
                                        block onClick={() => this.handleTypeChange('make')}
                                        disabled={!this.state.loading}>
                                    Make
                                </Button>
                            </Row>
                        </Col>
                        {this.state.loading ?
                            <Col>
                                <Row>
                                    <Form>
                                        <FormGroup row>
                                            <Input type="file" name="image" id="classifyImage"
                                                   onChange={(event) => this.fileChanged(event)}/>
                                            <FormText color="muted">
                                                Select a .JPG or .JPEG to classify!
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
                            : <Col style={{textAlign: 'center'}}>
                                <h4>{this.state.activeButton.charAt(0).toUpperCase() + this.state.activeButton.slice(1)}</h4>
                                <br/>
                                <p className='display-3'>{this.state.classification}</p>
                                <Button color='danger' onClick={this.resetLoader}>Reset</Button>
                            </Col>
                        }
                        {this.state.file ?
                            <Col>
                                <img style={{maxWidth: '75%'}}
                                     src={URL.createObjectURL(this.state.file)}
                                     alt='Hopefully a car'/>
                            </Col>
                            : undefined
                        }
                    </Row>
                </Container>
            </div>
        )
    }
    ;
}

export default Loader;