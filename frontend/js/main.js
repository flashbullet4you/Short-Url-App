document.getElementById('shortenForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const longUrl = document.getElementById('longUrl').value;
    const resultDiv = document.getElementById('result');
    
    try {
        const response = await fetch('/short_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ long_url: longUrl })
        });
        
        if (response.ok) {
            const data = await response.json();
            const shortUrl = window.location.origin + '/' + data.short_url;
            resultDiv.className = 'success';
            resultDiv.innerHTML = `
                <p>Ссылка успешно сокращена!</p>
                <p><a href="${shortUrl}" target="_blank">${shortUrl}</a></p>
                <button onclick="copyToClipboard('${shortUrl}')">Копировать</button>
            `;
        } else {
            const error = await response.json();
            resultDiv.className = 'error';
            resultDiv.textContent = error.detail || 'Произошла ошибка';
        }
    } catch (error) {
        resultDiv.className = 'error';
        resultDiv.textContent = 'Произошла ошибка соединения';
    }
});

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Ссылка скопирована!');
    }).catch(err => {
        console.error('Ошибка копирования: ', err);
    });
}