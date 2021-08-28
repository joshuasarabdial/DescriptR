import React from 'react';
import { Dropdown, DropdownButton } from 'react-bootstrap';
const FileDownload = require('js-file-download');

function DownloadButton(props) {

    function getPackage(key, e) {
        let url = new URL('/api/pkg', window.location.href);
        url.search = new URLSearchParams({ type: key }).toString()

        // Fetch the file at GET /api/pkg?type=windows|linux and download
        fetch(url)
            .then(res => res.blob())
            .then(blob => {
                if(key === "windows") {
                    FileDownload(blob, 'Descriptrly.exe');
                } else if(key === "linux") {
                    FileDownload(blob, 'Descriptrly.AppImage');
                }
            });
    }

    return (
        <DropdownButton
            id="dl-dropdown"
            onSelect={getPackage}
            title="Download Desktop App"
        >
            <Dropdown.Item eventKey="windows">Windows</Dropdown.Item>
            <Dropdown.Item eventKey="linux">Linux</Dropdown.Item>
        </DropdownButton>
    );
}

export default DownloadButton;
