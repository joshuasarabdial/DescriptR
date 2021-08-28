import React from 'react';
import { Card } from 'react-bootstrap';

export default class Help extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            filterDocs : [
                {
                    filter: 'Code',
                    text: `Search by course code, e.g. "CIS". This filter supports the "contains"
                            and "is (exactly)" operators which allow for partial-text and exact
                            text search respectively.`
                }, {
                    filter: 'Subject',
                    text: `Search by subject, e.g. "Accounting", a more natural language grouping
                    that is present in the Course Calendar. This filter supports the "contains" and
                    "is (exactly)" operators which allow for partial-text and exact text search
                    respectively.`
                }, {
                    filter: 'Department',
                    text: `Search by course department, e.g. "Department of Clinical Studies". This
                    filter supports the "contains" and "is (exactly)" operators which allow for
                    partial-text and exact text search respectively.`
                }, {
                    filter: 'Keyword',
                    text: `Search by keyword, e.g. "biology". This
                    filter supports the "contains" and "is (exactly)" operators which allow for
                    partial-text and exact text search respectively.`
                }, {
                    filter: 'Level',
                    text: `Search by course level, e.g. "4" for a fourth-level course, a course with
                    the course code NNN-4XXX. This filter supports the "contains" and "is (exactly)"
                    operators which allow for partial-text and exact text search respectively.`
                }, {
                    filter: 'Number',
                    text: `Search by course number, e.g. "4250". This filter supports the "contains"
                    and "is (exactly)" operators which allow for partial-text and exact text search
                    respectively.`
                }, {
                    filter: 'Semester',
                    text: `Search by semester, [Summer, Winter, Fall].`
                }, {
                    filter: 'Weight',
                    text: `Search by a course's credit weight, [0.0, 0.25, 0.50, 0.75, 1.00, 1.75,
                    2.00, 2.50, 2.75, 7.50].`
                }, {
                    filter: 'Available Capacity',
                    text: `Search by a course's available capacity, e.g. "8". This filter supports
                    the "is (exactly)", "greater than", and "less than" operators for finer
                    filtering.`
                }, {
                    filter: 'Lecture Hours',
                    text: `Search by the amount of lecture hours per week a course demands, e.g.
                    "6". This filter supports the "is (exactly)", "greater than", and "less than"
                    operators for finer filtering.`
                }, {
                    filter: 'Lab Hours',
                    text: `Search by the amount of lab hours per week a course demands, e.g. "6".
                    This filter supports the "is (exactly)", "greater than", and "less than"
                    operators for finer filtering.`
                }, {
                    filter: 'Currently Offered',
                    text: `Filter courses by whether or not they're offered in the current semester.`
                },
            ],
        };
    }
    render() {
        return (
            <div className="bg-light py-5">
                <h1>Search Help</h1>
                <p>
                    Descriptr supports various search filters that you can use to refine your
                    search. The search bar is dynamic, as you add filters they refine the set of
                    matching courses with a logical AND.
                </p>
                {this.state.filterDocs.map((item) => (
                    <Card key={item.filter} body className="my-5">
                        <Card.Title>{item.filter}</Card.Title>
                        <Card.Text>{item.text}</Card.Text>
                    </Card>
                ))}
            </div>
        );
    }
}
