// // In static/js/script.js
// document.addEventListener('DOMContentLoaded', () => {
//     const form = document.getElementById('prediction-form');
//     const fileInput = document.getElementById('file-input');
//     const fileNameDisplay = document.getElementById('file-name-display');
//     const dataPreviewContainer = document.getElementById('data-preview');
//     const previewContainer = document.getElementById('preview-container');
//     const resultsContainer = document.getElementById('results-container');
//     const predictionResultsContainer = document.getElementById('prediction-results');
//     const downloadBtn = document.getElementById('download-btn');
//     const loader = document.getElementById('loader');

//     let uploadedFile = null;
//     let tableData = null; // To store parsed CSV data

//     // Feature 3: Show file name and preview on file selection
//     fileInput.addEventListener('change', (event) => {
//         uploadedFile = event.target.files[0];
//         if (uploadedFile) {
//             fileNameDisplay.textContent = `Selected file: ${uploadedFile.name}`;
            
//             // Use Papa Parse to read and display the CSV
//             Papa.parse(uploadedFile, {
//                 header: true,
//                 dynamicTyping: true,
//                 complete: (results) => {
//                     tableData = results.data;
//                     displayTable(tableData, dataPreviewContainer, true); // true for editable
//                     previewContainer.style.display = 'block';
//                 }
//             });
//         }
//     });

//     // Main submit logic
//     form.addEventListener('submit', async (event) => {
//         event.preventDefault();

//         // Feature 1: Inline error handling
//         if (!uploadedFile) {
//             alert('Please select a CSV file first.');
//             return;
//         }

//         loader.style.display = 'block'; // Show loader
//         resultsContainer.style.display = 'none'; // Hide previous results

//         const formData = new FormData();
//         formData.append('file', uploadedFile);

//         try {
//             const response = await fetch('/predict', {
//                 method: 'POST',
//                 body: formData
//             });

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
//             }

//             // The data from the backend is already in the perfect format
//             const predictionData = await response.json();
            
//             console.log('Received prediction data:', predictionData);
//             // logging.info('Received prediction data:', predictionData);
//             // Now we can use it directly
//             displayTable(predictionData, predictionResultsContainer, false);
//             resultsContainer.style.display = 'block';

//         } catch (error) {
//             console.error('Error:', error);
//             alert(`An error occurred: ${error.message}`);
//         } finally {
//             loader.style.display = 'none'; // Hide loader
//         }
//     });

//     // Helper function to display data as a table
//     function displayTable(data, container, isEditable) {
//         container.innerHTML = ''; // Clear previous table
//         if (!data || data.length === 0) return; // Don't create a table if there's no data

//         const table = document.createElement('table');
//         const thead = document.createElement('thead');
//         const tbody = document.createElement('tbody');
        
//         // --- FIX: Get headers and sort them numerically ---
//         const headers = Object.keys(data[0]);

//         headers.sort((a, b) => {
//             // Keep 'prediction' column at the very end
//             if (a === 'prediction') return 1;
//             if (b === 'prediction') return -1;

//             // Extract numbers from "Sensor-X" and compare
//             const numA = parseInt(a.split('-')[1] || 0);
//             const numB = parseInt(b.split('-')[1] || 0);
//             return numA - numB;
//         });
//         // --- END OF FIX ---

//         // Create header row using the sorted headers
//         const headerRow = document.createElement('tr');
//         headers.forEach(key => {
//             const th = document.createElement('th');
//             th.textContent = key;
//             headerRow.appendChild(th);
//         });
//         thead.appendChild(headerRow);

//         // Create data rows using the sorted headers to maintain order
//         data.forEach(row => {
//             const tr = document.createElement('tr');
//             headers.forEach(header => {
//                 const td = document.createElement('td');
//                 td.textContent = row[header];
//                 if (isEditable) {
//                     td.contentEditable = true;
//                 }
//                 tr.appendChild(td);
//             });
//             tbody.appendChild(tr);
//         });

//         table.appendChild(thead);
//         table.appendChild(tbody);
//         container.appendChild(table);
//     }
    
//     // Feature 2: Download button logic
//     downloadBtn.addEventListener('click', () => {
//         const table = predictionResultsContainer.querySelector('table');
//         if (table) {
//             const rows = Array.from(table.querySelectorAll('tr'));
//             const csvContent = rows.map(row => 
//                 Array.from(row.querySelectorAll('th, td'))
//                      .map(cell => `"${cell.textContent.replace(/"/g, '""')}"`)
//                      .join(',')
//             ).join('\n');

//             const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8,' });
//             const link = document.createElement('a');
//             link.href = URL.createObjectURL(blob);
//             link.download = 'prediction_results.csv';
//             link.style.visibility = 'hidden';
//             document.body.appendChild(link);
//             link.click();
//             document.body.removeChild(link);
//         }
//     });
// });



// Updates rendering

// In static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name-display');
    const dataPreviewContainer = document.getElementById('data-preview');
    const previewContainer = document.getElementById('preview-container');
    const resultsContainer = document.getElementById('results-container');
    const predictionResultsContainer = document.getElementById('prediction-results');
    const downloadBtn = document.getElementById('download-btn');
    const loader = document.getElementById('loader');

    let originalFileName = '';

    // Feature 3: Show file name and preview on file selection
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            originalFileName = file.name;
            fileNameDisplay.textContent = `Selected file: ${originalFileName}`;
            
            Papa.parse(file, {
                header: true,
                dynamicTyping: true,
                skipEmptyLines: true,
                complete: (results) => {
                    displayTable(results.data, dataPreviewContainer, true);
                    previewContainer.style.display = 'block';
                }
            });
        }
    });

    // Main submit logic
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        // --- FIX: Read from the table instead of using the original file ---
        const editedData = getTableDataAsArray('data-preview');

        if (editedData.length === 0) {
            alert('There is no data to predict. Please upload a file.');
            return;
        }

        loader.style.display = 'block';
        resultsContainer.style.display = 'none';

        // Convert the edited data back to a CSV string
        const csvString = Papa.unparse(editedData);
        // Create a file-like object from the string
        const editedFile = new Blob([csvString], { type: 'text/csv' });

        const formData = new FormData();
        // Append the new, in-memory file
        formData.append('file', editedFile, originalFileName || 'edited_data.csv');
        // --- END OF FIX ---

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const predictionData = await response.json();
            
            // Merge the user's edited data with the new prediction column
            const finalDisplayData = editedData.map((userRow, index) => {
                const predictionRow = predictionData[index];
                return {
                    ...userRow,
                    prediction: predictionRow ? predictionRow.prediction : 'N/A'
                };
            });

            displayTable(finalDisplayData, predictionResultsContainer, false);
            resultsContainer.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            alert(`An error occurred: ${error.message}`);
        } finally {
            loader.style.display = 'none';
        }
    });

    // New helper function to read data from an HTML table
    function getTableDataAsArray(tableContainerId) {
        const table = document.getElementById(tableContainerId)?.querySelector('table');
        if (!table) return [];

        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent);
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        
        return rows.map(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            const rowData = {};
            headers.forEach((header, index) => {
                rowData[header] = cells[index].textContent;
            });
            return rowData;
        });
    }

    // This function for displaying tables is still needed
    function displayTable(data, container, isEditable) {
        // ... (This function remains the same as before)
        container.innerHTML = '';
        if (!data || data.length === 0) return;
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        const headers = Object.keys(data[0]);
        headers.sort((a, b) => {
            if (a === 'prediction') return 1;
            if (b === 'prediction') return -1;
            const numA = parseInt(a.split('-')[1] || 0);
            const numB = parseInt(b.split('-')[1] || 0);
            return numA - numB;
        });
        const headerRow = document.createElement('tr');
        headers.forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        data.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = row[header];
                if (isEditable) {
                    td.contentEditable = true;
                }
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(thead);
        table.appendChild(tbody);
        container.appendChild(table);
    }
    
    // Download button logic remains the same
    downloadBtn.addEventListener('click', () => {
        //... (This function remains the same as before)
        const table = predictionResultsContainer.querySelector('table');
        if (table) {
            const rows = Array.from(table.querySelectorAll('tr'));
            const csvContent = rows.map(row => 
                Array.from(row.querySelectorAll('th, td'))
                     .map(cell => `"${cell.textContent.replace(/"/g, '""')}"`)
                     .join(',')
            ).join('\n');

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8,' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'prediction_results.csv';
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    });
});