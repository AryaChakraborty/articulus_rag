async function checkFact() {
    const text = document.getElementById('inputText').value;
    const response = await fetch('http://127.0.0.1:5000/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
    });
    const result = await response.json();
    displayResults(result);
}

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    result.results.forEach((res, index) => {
        const claimDiv = document.createElement('div');
        claimDiv.innerHTML = `<strong>Claim ${index + 1}:</strong> ${res.claim}<br>`;
        res.results.forEach((resText) => {
            const resDiv = document.createElement('div');
            resDiv.innerHTML = `- ${resText}`;
            claimDiv.appendChild(resDiv);
        });
        resultsDiv.appendChild(claimDiv);
    });
}
