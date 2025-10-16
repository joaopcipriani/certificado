document.getElementById('csrForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get form values
    const env = document.getElementById('env').value;
    const keyName = document.getElementById('keyName').value;
    const csrName = document.getElementById('csrName').value;
    const country = document.getElementById('country').value;
    const organization = document.getElementById('organization').value;
    const commonName = document.getElementById('commonName').value;
    const state = document.getElementById('state').value;
    const locality = document.getElementById('locality').value;
    const serialNumber = document.getElementById('serialNumber').value;

    // Construct OpenSSL command
    const command = `"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe" req -newkey rsa:2048 -keyout ${env}_${keyName}.key -sha256 -out ${env}_${csrName}.csr -subj '/C=${country}/O=${organization}/CN=${commonName}/ST=${state}/L=${locality}/businessCategory=Private Organization/serialNumber=${serialNumber}/jurisdictionCountryName=${country}'`;

    // Display command
    const outputDiv = document.getElementById('commandOutput');
    outputDiv.textContent = `Generated Command:\n${command}`;

    // Create downloadable file
    const blob = new Blob([command], { type: 'text/plain' });
    const downloadLink = document.getElementById('downloadLink');
    downloadLink.href = URL.createObjectURL(blob);
    downloadLink.download = `${env}_openssl_command.bat`;
    downloadLink.style.display = 'block';
    downloadLink.textContent = `Download ${env}_openssl_command.bat`;
});
