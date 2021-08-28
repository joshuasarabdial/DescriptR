import React from 'react';
import { Card, CardColumns } from 'react-bootstrap';

import l_flask from '../img/l_flask.png';
import l_nginx from '../img/l_nginx.svg';
import l_react from '../img/l_react.svg';
import l_gitlab from '../img/l_gitlab.svg';
import l_docker from '../img/l_docker.png';
import l_electron from '../img/l_electron.png';

export default class Help extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            techs: [
                {
                    id: 0,
                    image: l_flask,
                    title: "Flask API",
                    text: `At the beginning of the project, when our goal was a command-line tool
                    that generated graphs of interconnected courses at the University of Guelph, we
                    settled on Python as the primary language for development. We designed a parser,
                    course search functions, and CSV export functionality for those first stages of
                    the project. As the project evolved to become web-based, we converted our existing
                    code into a fast API built in Flask to serve our frontend website and Electron app.`
                }, {
                    id: 1,
                    image: l_nginx,
                    title: "NGINX Reverse Proxy",
                    text: `We're using NGINX as a reverse proxy to handle incoming requests and forward
                    them to our Flask backend servers. This can eventually evolve into a load-balancer
                    if we choose to deploy more backend servers. We support HTTPS thanks to Let's Encrypt.`
                }, {
                    id: 2,
                    image: l_react,
                    title: "React Frontend",
                    text: `We've chosen to use the React framework for our user interfaces, both the
                    website and the Electron App. React is supported by various styling and component
                    libraries, such as react-table, react-bootstrap, Bootstrap,
                    D3.js, and the Open Iconic icon library.`
                }, {
                    id: 3,
                    image: l_docker,
                    title: "Docker Containerization",
                    text: `The Flask API, React frontend, and the NGINX reverse proxy all operate in
                    Docker containers in a Docker Swarm. This swarm can be deployed locally for quick
                    development, or deployed on our designated production resources with docker-machine.
                    Docker allows us to develop on whichever platform we would like, and still see a
                    unified product.`
                }, {
                    id: 4,
                    image: l_electron,
                    title: "Electron Desktop Application",
                    text: `The course mandates using Electron to build a cross-platform desktop application
                    as an alternative to the website. Our electron app wraps our React frontend and
                    communicates with our production API to deliver the same experience with our application
                    as with our website.`
                }, {
                    id: 5,
                    image: l_gitlab,
                    title: "GitLab CI",
                    text: `Descriptr uses GitLab CI for automated testing, automated Electron builds
                    and automatic deployment to our production resources upon release.`
                }
            ]
        }
    }

    render() {
        return (
            <div className="bg-light py-5">
                <h1>About</h1>
                <p>
                    Descriptr was made by Andrew D'Agostino, Maksymilian Mastalerz, Joshua Sarabdial,
                    Nicholas Skoretz, and Ryan White for the CIS*4250 - Software Design V course. This
                    website is being built over 9 one-week sprints, culminating in a final website,
                    an Electron cross-platform application, and a backend service that supports both.
                </p>
                <h1>Technology Stack</h1>
                <CardColumns>
                    {this.state.techs.map((item) =>(
                        <Card body className="my-5" key={item.id}>
                            <Card.Title>{item.title}</Card.Title>
                            <Card.Img id={"about-us-icon-"+item.id} variant="top" src={item.image} className="logo p-5"/>
                            <Card.Text>{item.text}</Card.Text>
                        </Card>
                    ))}
                </CardColumns>
            </div>
        );
    }
}
