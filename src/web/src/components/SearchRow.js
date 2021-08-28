/**
 * SearchRow.js
 */

import React from 'react';
import { Col, Form, Row, Button } from 'react-bootstrap';

// Fields that will make use of >, <, and = comparisons
const numericalFields = ['lecture', 'lab', 'capacity', 'level', 'number'];

/**
 * SearchTypeDropdown
 *
 * Dropdown containing types of filters that can be used
 */
function SearchTypeDropdown(props) {
    const handleChange = (e) => {
        if (props.value) {
            props.addOption(props.value);
        }
        if (e.target.value) {
            props.removeOption(e.target.value);
        }
        props.setType(e.target.value);
    };

    let options = [
        ["code","Code"],
        ["subject","Subject"],
        ["department","Department"],
        ["keyword","Keyword"],
        ["level","Level"],
        ["number","Number"],
        ["semester","Semester"],
        ["weight","Weight"],
        ["capacity","Available Capacity"],
        ["lecture","Lecture Hours"],
        ["lab","Lab Hours"],
        ["offered","Currently Offered"]
    ];

    options = options.filter(([val, name], i) => {
        if(props.filtersAvailable.includes(val) || val === props.value) {
            return true;
        } else {
            return false;
        }
    });

    return (
        <Form.Control as='select' value={props.value} onChange={handleChange}>
            {options.map(([val, name]) => (
                <option value={val}>{name}</option>
            ))}
        </Form.Control>
    );
}

/**
 * SearchComparatorDropdown
 *
 * Dropdown containing ways to compare courses to the query
 *
 * Will change available options based on filter type passed through props
 */
function SearchComparatorDropdown(props) {
    const handleChange = (e) => props.setComparator(e.target.value);

    if (numericalFields.includes(props.type)) {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='>'>greater than</option>
                <option value='>='>greater or equal to</option>
                <option value='='>equal to</option>
                <option value='<='>less or equal to</option>
                <option value='<'>less than</option>
            </Form.Control>
        );
    } else if (props.type === 'weight' || props.type === 'offered' || props.type === 'semester') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='='>is (exactly)</option>
            </Form.Control>
        );
    } else if (props.type === 'keyword') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='~'>contains</option>
            </Form.Control>
        );
    } else {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='~'>contains</option>
                <option value='='>is (exactly)</option>
            </Form.Control>
        );
    }
}

/**
 * SearchQueryInput
 *
 * Input for the query section of a filter.
 *
 * Will change between a text input, number input, or select based on filter type passed
 * through the props.
 */
function SearchQueryInput(props) {
    const handleChange = (e) => props.setQuery(e.target.value);

    if (props.type === 'weight') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='0.0'>0.0</option>
                <option value='0.25'>0.25</option>
                <option value='0.50'>0.50</option>
                <option value='0.75'>0.75</option>
                <option value='1.00'>1.00</option>
                <option value='1.75'>1.75</option>
                <option value='2.00'>2.00</option>
                <option value='2.50'>2.50</option>
                <option value='2.75'>2.75</option>
                <option value='7.50'>7.50</option>
            </Form.Control>
        );
    } else if (props.type === 'offered') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='Y'>Yes</option>
                <option value='N'>No</option>
            </Form.Control>
        );
    } else if (props.type === 'semester') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='W'>Winter</option>
                <option value='F'>Fall</option>
                <option value='S'>Summer</option>
            </Form.Control>
        );
    } else if (props.type === 'level') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='1'>1000</option>
                <option value='2'>2000</option>
                <option value='3'>3000</option>
                <option value='4'>4000</option>
                <option value='5'>5000</option>
            </Form.Control>
        );
    } else if (numericalFields.includes(props.type)) {
        return <Form.Control type='number' value={props.value} placeholder='Enter a search term' onChange={handleChange} min={0} />;
    } else {
        return <Form.Control type='text' value={props.value} placeholder='Enter a search term' onChange={handleChange} />;
    }
}

/**
 * SearchRow
 *
 * Represents a single filter in the search. Manages the state of its
 * three child components and updates itself in the parent's state
 */
export default class SearchRow extends React.Component {
    constructor(props) {
        super(props);

        // Temporary state, real state is managed in parent
        this.state = { ...this.props.filter };
    }

    // Update individual values in child state, then update full filter in parent state
    setType = (type) => this.setState({ searchType: type, searchComparator: '=', searchQuery: '' }, this.updateParent); // Reset on type change
    setComparator = (comparator) => this.setState({ searchComparator: comparator }, this.updateParent);
    setQuery = (query) => this.setState({ searchQuery: query }, this.updateParent);

    // Update full filter in parent state
    updateParent = () => this.props.updateFilter(this.props.index, this.state);

    render() {
        return (
            <Row className='my-3'>
                <Col xs='12' sm='6' md='3' xl='2' className='my-1'>
                    <SearchTypeDropdown
                        value={this.props.filter.searchType}
                        filtersAvailable={this.props.filtersAvailable}
                        setType={this.setType}
                        removeOption={this.props.removeOption}
                        addOption={this.props.addOption}
                    />
                </Col>
                <Col xs='12' sm='6' md='3' xl='2' className='my-1'>
                    <SearchComparatorDropdown
                        value={this.props.filter.searchComparator}
                        setComparator={this.setComparator}
                        type={this.state.searchType}
                    />
                </Col>
                <Col xs='12' sm='6' md='3' xl='2' className='my-1'>
                    <SearchQueryInput value={this.props.filter.searchQuery} setQuery={this.setQuery} type={this.state.searchType} />
                </Col>
                <Col xs='auto' className='my-1'>
                    <Button variant='danger' type='button' onClick={() => this.props.removeRow(this.props.index)}>
                        <i class="fa fa-trash"></i>
                    </Button>
                </Col>
            </Row>
        );
    }
}
