import React from 'react';
import { TreeGraph } from './graph/treeGraph';
import { Card, Button, Row, Col } from 'react-bootstrap';
import CourseCodeSearch from './CourseCodeSearch';

const isProd = /^file/.test(window.location) || /^https:\/\/cis4250-03\.socs\.uoguelph\.ca/.test(window.location); // Check if executable or prod web server

export default class CourseTree extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            courses: {},
            downloadEnabled: false,
        };

        this.updateCourses = this.updateCourses.bind(this);
    }

    componentDidMount() {
        // Automatically search for a course in the querystring
        let courseQueryParam = new URLSearchParams(this.props.location.search).get('course');
        if (/^[a-zA-Z]+-\d{4}$/.test(courseQueryParam)) {
            this.handleQueryParam(courseQueryParam);
        }
    }

    updateCourses = (courses) => {
        this.setState({ 
            courses: courses, 
            downloadEnabled: (courses && Object.keys(courses).length && !courses.error)
        } 
    )};

    handleQueryParam = (courseID) => {
        fetch(isProd ? 'https://cis4250-03.socs.uoguelph.ca/api/prerequisite/' + courseID : 'api/prerequisite/' + courseID, {
            method: 'GET',
        })
            .then((response) => response.json())
            .then((data) => {
                if (!Array.isArray(data)) {
                    this.updateCourses(data);
                } else {
                    this.updateCourses({});
                }
            })
            .catch((err) => console.log(err));
    };

    render() {
        return (
            <div className='bg-light'>
                <section className='px-5 pb-5'>
                    <Card body className='my-5'>
                        <Card.Title>Course Search</Card.Title>
                        <CourseCodeSearch updateCourses={this.updateCourses} />
                    </Card>
                    <Card body>
                        <section className='Main'>
                            <Row className='justify-content-between mb-4'>
                                <Col xs='auto' className='my-auto'>
                                    <h5>Prerequisite Tree Graph</h5>
                                </Col>
                                <Col xs='auto'>
                                    <Button id='download-tree-graph' variant='primary' disabled={!this.state.downloadEnabled}>
                                        Download Graph
                                    </Button>
                                </Col>
                            </Row>
                            <Row className='my-1 mx-1'>
                                <Button id='collapse-all' variant='primary btn-sm'>
                                    Collapse All
                                </Button>
                                <Button className='mx-1' id='expand-all' variant='secondary btn-sm'>
                                    Expand All
                                </Button>
                            </Row>
                            <TreeGraph coursesData={this.state.courses} />
                        </section>
                    </Card>
                </section>
            </div>
        );
    }
}
