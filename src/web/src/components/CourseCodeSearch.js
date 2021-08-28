import React from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';

const isProd = /^file/.test(window.location) || /^https:\/\/cis4250-03\.socs\.uoguelph\.ca/.test(window.location); // Check if executable or prod web server

export default class CourseCodeSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            code: '',
            number: 0,
        };

        this.onClear = this.onClear.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onClear = () => {
        this.state.code = '';
        this.state.number = 0;
        this.props.updateCourses({});
    };

    onSubmit = () => {
        let courseID = this.state.code + '-' + String(this.state.number);
        fetch(isProd ? 'https://cis4250-03.socs.uoguelph.ca/api/prerequisite/' + courseID : 'api/prerequisite/' + courseID, {
            method: 'GET',
        })
            .then((response) => response.json())
            .then((data) => {
                if (!Array.isArray(data)) {
                    this.props.updateCourses(data);
                } else {
                    this.props.updateCourses({});
                }
            })
            .catch((err) => console.log(err));
    };

    render() {
        return (
            <div>
                <Row className='my-3'>
                    <Col sm='5' md='3' xl='2' className='my-1'>
                        <Form.Control
                            type='text'
                            placeholder='Enter course code'
                            value={this.state.code}
                            onChange={(e) => this.setState({ code: e.target.value })}
                        />
                    </Col>
                    <h3 className='my-1 d-sm-block d-none'>*</h3>
                    <Col sm='5' md='3' xl='2' className='my-1'>
                        <Form.Control
                            type='number'
                            placeholder='Enter course number'
                            value={this.state.number}
                            onChange={(e) => this.setState({ number: e.target.value })}
                        />
                    </Col>
                </Row>
                <p>e.g. CIS*4250</p>
                <Row className='mt-3'>
                    <Col xs='12' sm='5' md='3' xl='2'>
                        <Button variant='danger' type='button' className='btn-block my-1' onClick={this.onClear}>
                            Clear Search
                        </Button>
                    </Col>
                    <h3 className='my-1 d-sm-block d-none'>&nbsp;</h3>
                    <Col xs='12' sm='5' md='3' xl='2'>
                        <Button type='button' variant='primary' className='btn-block my-1' onClick={this.onSubmit}>
                            Search
                        </Button>
                    </Col>
                </Row>
            </div>
        );
    }
}
