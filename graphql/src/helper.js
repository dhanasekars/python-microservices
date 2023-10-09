import fs from 'fs';

function loadJson(filePath) {
    try {
        // Read the JSON file synchronously
        const jsonData = fs.readFileSync(filePath, 'utf8');

        // Parse the JSON data into a JavaScript object and assign it to a constant
        const jsonDataObject = JSON.parse(jsonData);
        return jsonDataObject;
        
    } catch (error) {
        console.error('Error reading JSON file:', error);
        return null;
    }
}


function saveJson(filePath, jsonDataObject) {
    try{
        const jsonData = JSON.stringify(jsonDataObject, null, 2);
        fs.writeFileSync(filePath, jsonData, 'utf8');
        console.log('JSON data is saved.');
    }
    catch(error){
        console.error('Error writing JSON file:', error);
    }
}

export { loadJson, saveJson };

