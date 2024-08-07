document.getElementById('visualize-btn').addEventListener('click', function() {
    const selectedOptions = Array.from(document.getElementById('country-codes').selectedOptions);
    if (selectedOptions.length > 3) {
        alert('You can only select up to 3 country codes.');
        return;
    }
    
    const countryCodes = selectedOptions.map(option => option.value);
    alert('Selected Country Codes: ' + countryCodes.join(', '));
    // You can add your visualization logic here
});
