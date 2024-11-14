// script.js
async function getRecommendation() {
    const make = document.getElementById('make').value;
    const model = document.getElementById('model').value;
    const year = document.getElementById('year').value;
    const price = document.getElementById('price').value;
    const fuel = document.getElementById('fuel').value;
    const drive = document.getElementById('drive').value;

    const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ make, model, year, price, fuel, drive })
    });

    const data = await response.json();
    displayResults(data);
}

function displayResults(cars) {
    const results = document.getElementById('results');
    results.innerHTML = '';
    if (cars.length > 0) {
        cars.forEach(car => {
            const carElement = document.createElement('div');
            carElement.classList.add('car');
            carElement.innerHTML = `
                <strong>${car['Make Name']} ${car['Model Name']}</strong><br>
                Year: ${car['Trim Year']}<br>
                Type: ${car['Body Type']}<br>
                Fuel: ${car['Engine Fuel Type']}<br>
                Price: $${car['Trim Msrp']}<br>
            `;
            results.appendChild(carElement);
        });
    } else {
        results.innerHTML = '<p>No cars matched your preferences.</p>';
    }
}
