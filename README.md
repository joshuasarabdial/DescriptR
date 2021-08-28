# UoG Course Descriptr.ly

![Pipeline](https://gitlab.socs.uoguelph.ca/cis4250_team3/uog-course-descriptions/badges/develop/pipeline.svg?style=flat-square) ![Coverage](https://gitlab.socs.uoguelph.ca/cis4250_team3/uog-course-descriptions/badges/develop/coverage.svg?style=flat-square)

[[_TOC_]]

## Installation

1. Add the following to the `host` file.
    ```
    127.0.0.1       dev.cis4250-03.socs.uoguelph.ca
    ```

2. Generate and trust an ssl certificate for the app:

    ```
    $ cd <project_root>
    $ openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
        -keyout docker/nginx_load_balancer/nginx/ssl/dev.key.pem -out docker/nginx_load_balancer/nginx/ssl/dev.full.pem \
        -subj "/CN=*.cis4250-03.socs.uoguelph.ca" -addext "subjectAltName=DNS:cis4250-03.socs.uoguelph.ca,DNS:*.cis4250-03.socs.uoguelph.ca,IP:10.0.0.1"
    ```

    **IMPORTANT**: Add the file docker/nginx_load_balancer/nginx/ssl/dev.full.pem as a trusted certificate authority in your browser.

    Chrome: Go to the url chrome://settings/certificates > Click "Authorities" > Click "Import" > Select the file > Check all the boxes.

    Firefox: Go to the url about:preferences#privacy > Go down to "Certificates" > Click "View Certificates" > Click "Authorities" > Click "Import" > Select the file

3. Initialize a local docker swarm:

    ```
    $ eval "$(docker-machine env -u)"
    $ sudo docker swarm init
    ```

4. Start up a docker registry:
    ```
    $ sudo docker service create --name registry --mount type=volume,source=registry-data,destination=/var/lib/registry --publish published=6000,target=5000 registry:2
    ```

## Testing

#### Running Tests

Navigate to the `src/api` directory from the parent `descriptr` directory.

##### To run all unit tests
`python3 -m unittest`

##### To run specific test files
`python3 -m unittest test/<test-file>` where `<test-file>` is the test file you want to run.

#### Generating Test Coverage

Navigate to the parent `descriptr` directory.
Run `pytest --cov=src/api/classes/ --cov=src/api/functions/ src/api/test/`

## Running

To run [Descriptr.ly](https://dev.cis4250-03.socs.uoguelph.ca/) (API + WEB + NGINX):

1. Build and push the docker images:

    ```
    $ sudo docker-compose --verbose -f docker-compose-swarm.dev.yml build
    $ sudo docker-compose --verbose -f docker-compose-swarm.dev.yml push
    ```

2. Deploy the swarm:
    ```
    $ sudo docker stack deploy --compose-file=docker-compose-swarm.dev.yml descriptr_stack
    ```

Once running:
* The web server will be available at <https://dev.cis4250-03.socs.uoguelph.ca/>
* The API will be available at <https://dev.cis4250-03.socs.uoguelph.ca/api>

3. Redeploy swarm after updates:
    ```
    $ docker stack rm descriptr_stack; docker-compose -f docker-compose-swarm.dev.yml build; docker stack deploy --compose-file=docker-compose-swarm.dev.yml descriptr_stack
    ```

    If the command fails from `failed to create service descriptr_stack_descriptr_api: Error response from daemon: network descriptr_stack_descriptr-network not found`, run it again and it should work.

## Deploying To Production

For simple deployment to production just merge code into master and our git lab script will auto deploy for you.

If you want to do things the hard manual way follow the instructions in : docs/deployments/production/README.md

## Using Electron

### Downloading a Ready Built Executable

If you are on windows or linux you can download a pre-built executable from the production website cis4250-03.socs.uoguelph.ca

For linux you will need to make the downloaded file executable by your operating system with `chmod 755 Descriptrly.AppImage`

### Building Electron Executable Yourself

1. Edit the variable ENV in the `.env` file

    ```
    ENV=PROD
    ```

    When set to `PROD`, it will use assets from the React `build/` folder.

2. Ensure you have all node packages installed:

    ```
    npm --prefix src/web install  # This may not be required as docker could've already installed packages locally.
    ```

3. Next, type the commands:

    ```
    npm --prefix src/web run build
    ```

    Now that the executable is built, you can run `src/web/dist/descriptrly-0.1.0(.exe or .AppImage)`

### Running Electron Locally for Development:

1. Edit the variable ENV in the `.env` file

    ```
    ENV=DEV
    ```

    When set to `DEV`, the Electron app will use assets from the React server. When set to `PROD`, it will use assets from the React `build/` folder.

    You can optionally set the `DEV_URL` environment variable if you wish to use a React dev server running outside of the Docker Swarm.

2. Ensure you have all node packages installed:

    ```
    npm --prefix src/web install  # This may not be required as docker could've already installed packages locally.
    ```

3. In a second terminal, run the following command to start the Electron app:

    ```
    npm --prefix src/web run electron
    ```