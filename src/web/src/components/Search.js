/**
 * Search.js
 */

import React from 'react';
import { Alert, Button, Col, Row } from 'react-bootstrap';
import SearchRow from '../components/SearchRow.js';

// Fields that will make use of >, <, and = comparisons
const numericalFields = ['lecture', 'lab', 'capacity'];
const isProd = /^file/.test(window.location) || /^https:\/\/cis4250-03\.socs\.uoguelph\.ca/.test(window.location); // Check if executable or prod web server

export default class Search extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            counter: 0,
            rows: [this.createEmptyRow()],
            startingFilter: "code",
            filtersAvailable: ["subject","department","keyword","level","number","semester","weight","capacity","lecture","lab","offered"],
            error: null,
        };
    }

    // Since we don't have hooks in a React class, these three functions set up a listener for
    // <Enter> and fire the submit function.
    componentDidMount() {
        document.addEventListener("keydown", this.listener);
        this.setAddSearchTermButtonState();
    };

    componentDidUpdate() {
        this.setAddSearchTermButtonState();
    };

    compomentWillUnmount() {
        document.removeEventListener("keydown", this.listener);
        this.setAddSearchTermButtonState();
    };

    listener(event) {
        if (event.code === "Enter" || event.code === "NumpadEnter") {
            this.onSubmit();
        }
    };

    // Creates a new filter, with default values where necessary
    createEmptyRow(id, filtersAvailable) {
        var searchType = filtersAvailable != null ? filtersAvailable[0] : 'code';
        return {
            _id: id,
            searchType: searchType, // If changing this to something else, add "code" to the filtersAvailable array above and change "startingFilter".
            searchComparator: '=',
            searchQuery: ''
        };
    };

    // Appends a new, base filter
    addFilter = () => {
        if (this.state.filtersAvailable.length > 0) {
            var filterToAdd = this.createEmptyRow(this.state.counter + 1, this.state.filtersAvailable);
            this.removeOption(filterToAdd.searchType);
            this.setState({
                rows: this.state.rows.concat([filterToAdd]),
                counter: this.state.counter + 1,
            });
        }
    };

    // Updates an individual filter by index
    updateFilter = (index, filter) => {
        let temp = this.state.rows;
        temp[index] = filter;
        this.setState({ rows: temp });
    };

    // Removes row if remove button clicked
    removeRow = (index) => {
        //Add the filter category being removed to the available filters
        const filterCategoryBeingRemoved = this.state.rows[index].searchType;
        // eslint-disable-next-line eqeqeq
        if (!this.state.filtersAvailable.includes(filterCategoryBeingRemoved) && filterCategoryBeingRemoved != undefined) {
            this.setState({
                filtersAvailable: this.state.filtersAvailable.concat([filterCategoryBeingRemoved])
            });
        }
        
        let tempRows = [...this.state.rows];
        tempRows.splice(index, 1);
        this.setState({ rows: tempRows });
    };

    clearSearch = () => {
        //Add back in the filters that were cleared.
        let filtersCleared = [];
        this.state.rows.forEach((row, i) => {
            if (!this.state.filtersAvailable.includes(row.searchType) && !filtersCleared.includes(row.searchType) && this.state.startingFilter !== row.searchType) {
                filtersCleared.push(row.searchType);
            }
        });
        this.setState({
            filtersAvailable: this.state.filtersAvailable.concat(filtersCleared)
        });

        var filter = this.createEmptyRow();
        this.setState({
            rows: [filter],
        })
        this.removeOption(filter.searchType);
        this.props.updateCourses([]);
    }

    removeOption = (val) => {
        var index = this.state.filtersAvailable.indexOf(val);
        if (index !== -1) {
            this.state.filtersAvailable.splice(index, 1);
        }
    }

    addOption = (val) => {
        if (!this.state.filtersAvailable.includes(val)) {
            this.state.filtersAvailable.push(val);
        }
    }

    setAddSearchTermButtonState = () => {
        var disabledState = this.state.filtersAvailable.length === 0;
        document.getElementById("add-search-term-button").disabled = disabledState;
    }

    // Converts the array of filters from the state to a request body the API server can understand
    convertToRequestBody = () => {
        let request = {};
        let incomplete = 0;

        for (let filter of this.state.rows) {
            if (filter.searchType && filter.searchComparator && filter.searchQuery) {
                if (numericalFields.includes(filter.searchType)) {
                    if (filter.searchType === 'capacity') {
                        request[filter.searchType] = {
                            capacity: filter.searchQuery,
                            comparison: filter.searchComparator,
                        };
                    } else {
                        request[filter.searchType] = {
                            hours: filter.searchQuery,
                            comparison: filter.searchComparator,
                        };
                    }
                } else {
                    request[filter.searchType] = {
                        query: filter.searchQuery,
                        comparison: filter.searchComparator,
                    };
                }
            } else {
                incomplete++;
            }
        }

        if (incomplete > 0) {
            alert(`${incomplete} filter(s) were not fully filled out and were not sent`);
        }

        return request;
    };

    // Send filters as a POST to API server
    onSubmit = () => {
        fetch(isProd ? 'https://cis4250-03.socs.uoguelph.ca/api/search' : '/api/search', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.convertToRequestBody()),
        })
            .then((response) => response.json())
            .then((data) => {
                let courses = data.error ? [] : data.courses;
                let prereqs = data.error ? [] : data.prereqs;
                this.props.updateCourses(
                    courses.map((course) => JSON.parse(course)),
                    prereqs.map((p) => JSON.parse(p))
                );
                this.setState({ error: data.error });
            });
    };

    render() {
        return (
            <>
                {this.state.error ? <Alert variant='danger'>{this.state.error}</Alert> : null}
                {this.state.rows.map((row, id) => {
                    return <SearchRow   key={row._id}
                        index={id}
                        filter={row}
                        filtersAvailable={this.state.filtersAvailable}
                        removeOption={this.removeOption}
                        addOption={this.addOption}
                        updateFilter={this.updateFilter}
                        removeRow={this.removeRow} />;
                })}
                <hr />
                <Row className='mt-3'>
                    <Col xs='12' sm='6' md='3' xl='2'>
                        <Button variant='danger' type='button' className='btn-block my-1' onClick={this.clearSearch}>
                            Clear Search
                        </Button>
                    </Col>
                    <Col xs='12' sm='6' md='3' xl='2'>
                        <Button id='add-search-term-button' variant='secondary' type='button' className='btn-block my-1' onClick={this.addFilter}>
                            Add Filter
                        </Button>
                    </Col>
                    <Col xs='12' sm='6' md='3' xl='2'>
                        <Button type='button' variant='primary' className='btn-block my-1' onClick={this.onSubmit}>
                            Search
                        </Button>
                    </Col>
                </Row>
            </>
        );
    }
}
