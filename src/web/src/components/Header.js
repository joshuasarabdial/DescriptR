import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

import DownloadButton from './DownloadButton';

export default class Header extends React.Component {
    constructor(props) {
        super(props);

        // Check if executable or prod web server
        const isProd = /^file/.test(window.location)
        this.state = {
            links: [
                { link: '/', text: 'Home' },
                { link: '/courseTree', text: 'Course Tree' },
                { link: '/help', text: 'Help' },
                { link: '/about', text: 'About' },
            ],
            downloadVisible: isProd,
        };
    }
    render() {
        return (
            <Navbar className='justify-content-between bg-secondary' expand='md'>
                <Navbar.Brand href='/' className='text-white'>
                    Descriptr
                </Navbar.Brand>
                <Navbar.Toggle />
                <Navbar.Collapse>
                    <Nav variant='pills' defaultActiveKey='/' className='mr-auto my-1'>
                        {this.state.links.map((item) => (
                            <Nav.Item key={item.text} className='mx-2'>
                                <Nav.Link to={item.link} eventKey={item.link} className='text-white px-2' as={Link}>
                                    {item.text}
                                </Nav.Link>
                            </Nav.Item>
                        ))}
                    </Nav>
                    {!this.state.downloadVisible && <DownloadButton />}
                </Navbar.Collapse>
            </Navbar>
        );
    }
}
