document.addEventListener('DOMContentLoaded', function() {
    const codeEditor = document.getElementById('codeEditor');
    const runButton = document.getElementById('runButton');
    const clearButton = document.getElementById('clearButton');
    const outputContainer = document.getElementById('outputContainer');
    
    // Run code
    runButton.addEventListener('click', function() {
        const code = codeEditor.value.trim();
        if (!code) return;
        
        fetch('/evaluate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayOutput(data.output);
            } else {
                displayError(data.error);
            }
        })
        .catch(error => {
            displayError('An error occurred: ' + error.message);
        });
    });
    
    // Clear editor and output
    clearButton.addEventListener('click', function() {
        codeEditor.value = '';
        outputContainer.innerHTML = '';
    });
    
    function displayOutput(outputLines) {
        outputContainer.innerHTML = '';
        
        if (outputLines.length === 0) {
            outputContainer.innerHTML = '<div class="output-line">No output</div>';
            return;
        }
        
        outputLines.forEach(line => {
            const lineDiv = document.createElement('div');
            lineDiv.className = 'output-line';
            lineDiv.textContent = line;
            outputContainer.appendChild(lineDiv);
        });
    }
    
    function displayError(errorMessage) {
        outputContainer.innerHTML = `<div class="error-message">Error: ${errorMessage}</div>`;
    }
    
    // CSRF token helper function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});