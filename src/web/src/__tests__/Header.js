import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
} from '@testing-library/react';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from '../components/Header.js'

afterEach(cleanup);

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<Router><Header/></Router>, div);
});

it('renders header links', () => {
    render(
        <Router>
            <Header/>
        </Router>
    );

    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Course Tree')).toBeInTheDocument();
    expect(screen.getByText('Help')).toBeInTheDocument();
    expect(screen.getByText('About')).toBeInTheDocument();
});

it('selecting changes class', async () => {
    render(
        <Router>
            <Header/>
        </Router>
    );
    fireEvent.click(screen.getByText('About'));

    await waitFor(() => screen.getByText('About'))
    expect(screen.getByText('About')).toHaveClass('active');

});
