import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
} from '@testing-library/react';
import React from 'react';
import ReactDOM from 'react-dom';
import DownloadButton from '../components/DownloadButton.js'

afterEach(cleanup);

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<DownloadButton/>, div);
});

it('renders the dropdown menu', async () => {
    render(<DownloadButton />);
    fireEvent.click(screen.getByText('Download Desktop App'));

    await waitFor(() => screen.getByText('Download Desktop App'))
    expect(screen.getByText('Windows')).toBeInTheDocument();
    expect(screen.getByText('Linux')).toBeInTheDocument();
});
