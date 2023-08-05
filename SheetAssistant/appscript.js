let doc = SpreadsheetApp.openById("<sheetId>");

function doGet(request) {
  let response = { 'status': 'SUCCESS' };
  let sheet = doc.getSheetByName("Tasks");

  if (request && request.parameter && request.parameter.q && request.parameter.q == "list") {
    let result = {
      'status': 'SUCCESS',
      'tasks': []
    };
    let values = sheet.getRange('A3:A1000').getValues();
    for (let i = 0; i < values.length; i++) {
      if (values[i] == "") {
        break;
      }
      result.tasks.push(values[i][0]);
    }

    return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);
  }

  let newValue = request.parameter.text;

  let values = sheet.getRange('A3:A1000').getValues();
  let col = 'A';
  let lastEmptyRow = 3;
  for (let i = 0; i < values.length; i++) {
    if (values[i] == "") {
      lastEmptyRow = i + 3;
      break;
    }
  }
  let targetCell = sheet.getRange(col+lastEmptyRow);
  targetCell.setValue(newValue);

  return ContentService.createTextOutput(JSON.stringify(response)).setMimeType(ContentService.MimeType.JSON);
}
