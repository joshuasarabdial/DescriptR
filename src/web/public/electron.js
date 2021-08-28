require('dotenv').config();

const electron = require('electron');
// Modules to control application life and native browser window
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

const path = require('path');
const url = require('url');

// Global reference of the window object.
let mainWindow;

function createWindow() {
    // Create browser window
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 720,
        autoHideMenuBar: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: true,
        },
    });
    mainWindow.maximize();
    mainWindow.setTitle('Descriptr.ly');

    // loads the index.html of the app
    if (process.env.ENV === 'DEV') {
        mainWindow.loadURL(process.env.DEV_URL ? process.env.DEV_URL : 'https://dev.cis4250-03.socs.uoguelph.ca');
    } else {
        mainWindow.loadURL(`file://${path.join(__dirname, '../build/index.html')}`);
    }

    // Opens the dev tools. Comment out to get rid of them.
    //mainWindow.webContents.openDevTools();

    // Dereference window object on closure
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

// Create browser window after initialization
app.whenReady().then(createWindow);

// Quit app when all windows are closed except on macOS
// (It is common that apps stay open until user explitly quits)
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('certificate-error', (event, webContents, url, error, certificate, callback) => {
    if (process.env.ENV === 'DEV') {
        //Allow self signed certificate in DEV mode
        event.preventDefault();
        callback(true);
    }
});

// Recreates the window on macOS when user clicks on dock icon
app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});
