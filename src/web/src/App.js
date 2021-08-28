import React from 'react';
import { Card, Button, Row, Col, Tabs, Tab } from 'react-bootstrap';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import About from './components/About';
import CourseModal from './components/CourseModal';
import CourseTable2 from './components/CourseTable2';
import { ForceGraph } from './components/graph/forceGraph';
import { SunburstGraph } from './components/graph/sunburstGraph';
import Header from './components/Header';
import Help from './components/Help';
import Search from './components/Search';
import CourseTree from './components/CourseTree';

function addDarkmodeWidget() {
    const options = {
        saveInCookies: true,
        label: '🌓',
    };
    // eslint-disable-next-line no-undef
    const darkMode = new Darkmode(options);
    darkMode.showWidget();
}

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            courses: [],
            prereqs: [],
            downloadEnabled: false,
        };

        this.updateCourses = this.updateCourses.bind(this);

        this.courseModal = React.createRef();
    }

    updateCourses = (courses, prereqs) => {
        this.setState({
            courses: courses,
            prereqs: prereqs,
            downloadEnabled: courses && courses.length,
        });
    };

    nodeHoverTooltip = (node) => {
        return `<div>
            <b>${node.name}</b>
        </div>`;
    };

    componentDidMount() {
        window.addEventListener('load', addDarkmodeWidget);
    }

    componentWillUnmount() {
        window.removeEventListener('load', addDarkmodeWidget);
    }

    render() {
        return (
            <Router>
                <div className='App bg-light'>
                    <Header />
                    <section className='px-5 pb-5'>
                        <Switch>
                            <Route path='/about' component={About} />
                            <Route path='/help' component={Help} />
                            <Route path='/courseTree' component={CourseTree} />
                            <Route
                                path='/'
                                render={() => (
                                    <section className='px-5 pb-5'>
                                        <Card body className='my-5'>
                                            <Card.Title>Course Search</Card.Title>
                                            <Search updateCourses={this.updateCourses} />
                                        </Card>
                                        <Tabs defaultActiveKey='table' id='results-tab'>
                                            <Tab eventKey='table' title='Table'>
                                                <Card body>
                                                    <Card.Title>Results</Card.Title>
                                                    <CourseTable2 courseModal={this.courseModal} courses={this.state.courses} />
                                                </Card>
                                            </Tab>
                                            <Tab eventKey='node' title='Prerequisites Graph'>
                                                <Card body>
                                                    <section className='Main'>
                                                        <Row className='justify-content-between mb-4'>
                                                            <Col xs='auto' className='my-auto'>
                                                                <h5>Prerequisite Node Graph</h5>
                                                            </Col>
                                                            <Col xs='auto'>
                                                                <Button
                                                                    id='download-node-graph'
                                                                    variant='primary'
                                                                    disabled={!this.state.downloadEnabled}>
                                                                    Download Graph
                                                                </Button>
                                                            </Col>
                                                        </Row>
                                                        <ForceGraph
                                                            courseModal={this.courseModal}
                                                            coursesData={this.state.courses}
                                                            prereqsData={this.state.prereqs}
                                                            nodeHoverTooltip={this.nodeHoverTooltip}
                                                        />
                                                    </section>
                                                </Card>
                                            </Tab>
                                            <Tab eventKey='sunburst' title='Capacity Graph'>
                                                <Card body>
                                                    <section>
                                                        <Row className='justify-content-between mb-4'>
                                                            <Col xs='auto' className='my-auto'>
                                                                <h5>Max Capacity Sunburst Graph</h5>
                                                            </Col>
                                                            <Col xs='auto'>
                                                                <Button
                                                                    id='download-sunburst-graph'
                                                                    variant='primary'
                                                                    disabled={!this.state.downloadEnabled}>
                                                                    Download Graph
                                                                </Button>
                                                            </Col>
                                                        </Row>
                                                        <SunburstGraph coursesData={this.state.courses} />
                                                    </section>
                                                </Card>
                                            </Tab>
                                        </Tabs>
                                        <CourseModal ref={this.courseModal} />
                                    </section>
                                )}
                            />
                        </Switch>
                    </section>
                </div>
            </Router>
        );
    }
}
