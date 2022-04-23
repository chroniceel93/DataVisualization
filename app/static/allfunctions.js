//all functions for the project

//change title of graph
function updatetitle(nameval){
    myChart.config.options.plugins.title.text = nameval.value;
    myChart.update();
}

//update the name of datasets
function updatedatesetname1(nameval){
    myChart.config.data.datasets[0].label = nameval.value;
    myChart.update();
}

function updatedatesetname2(nameval){
    myChart.config.data.datasets[1].label = nameval.value;
    myChart.update();
}

//update y axes
function updateymax(numval){
    myChart.config.options.scales.y.suggestedMax = numval.value;
    myChart.update()
}

function updateymin(numval){
    myChart.config.options.scales.y.suggestedMin = numval.value;
    myChart.update()
}

function updatey2max(numval){
    myChart.config.options.scales.y2.suggestedMax = numval.value;
    myChart.update()
}

function updatey2min(numval){
    myChart.config.options.scales.y2.suggestedMin = numval.value;
    myChart.update()
}

//update x axes
function updatexmax(numval){
    myChart.config.options.scales.x.suggestedMax = numval.value;
    myChart.update()
}

function updatexmin(numval){
    myChart.config.options.scales.x.suggestedMin = numval.value;
    myChart.update()
}

//change names of axes
function updatexname(nameval){
    myChart.config.options.scales.x.title.text = nameval.value;
    myChart.update()
}

function updateyname(nameval){
    myChart.config.options.scales.y.title.text = nameval.value;
    myChart.update()
}

function updatey2name(nameval){
    myChart.config.options.scales.y2.title.text = nameval.value;
    myChart.update()
}

//user download of graph
function exportimage(){
    var a = document.createElement('a');
    a.href = myChart.toBase64Image();
    a.download = 'graph.png';

    // Trigger the download
    a.click();
}


//favorite graph function
function favgraph(){
    var tmp = localStorage.getItem('myArray');
    var image = myChart.toBase64Image();
    var tmp2 = tmp + " " + image;
    localStorage.setItem('myArray', tmp2);
}

//function for adding to the graph creation history
function graphhistory(){
    var tmp = localStorage.getItem('myArray2');
    var image = myChart.toBase64Image();
    var tmp2 = tmp + " " + image;
    localStorage.setItem('myArray2', tmp2);
    window.location.href = "/viewpage"
}

//export of user settings
function exportsavedata(charttype, x1, y1, y1type, op1, x2, y2, y2type, op2){
    var sentdata = charttype + " " + x1 + " " + y1 + " " + y1type + " " + op1 + " " + x2 + " " + y2 + " " + y2type + " " + op2;
    var a = document.createElement('a');
    a.href = 'data:attachment/text,' + encodeURI(sentdata);
    a.target = '_blank';
    a.download = 'GraphData.txt';
    a.click();
}

function importsavedata(){
    getGraph(localStorage.getItem('x1chose'), localStorage.getItem('y1chose'), localStorage.getItem('y1type'), localStorage.getItem('opchose'));

    //clear localstorage of import options
    localStorage.removeItem("opchose");
    localStorage.removeItem("x1chose");
    localStorage.removeItem("y1chose");
    localStorage.removeItem("y1type");
    localStorage.removeItem("op2chose");
    localStorage.removeItem("x2chose");
    localStorage.removeItem("y2chose");
    localStorage.removeItem("y2type");

    document.getElementById("importload").style.display = "block";
    setTimeout(function() {
    myChart.update();
    document.getElementById("importload").style.display = "none";
    }, 5000);
}

//dark mode
function darkmode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
}

// Keaton's functions:
// Ordered by: 1. Called on page load
//             2. Called by user action
//             3. Called by other function

// gets tables from raw JSON data
// passing by reference with global vars, but might need to change this - Arrays are weird in JS
// CLEAN: clean this up by figuring out better way to pass value out (instead of global variable reference)
function setTables(tableChoices) {
    var currentTable;

    // get database from backend
    $.ajax({
        url: $SCRIPT_ROOT + '/db_all',
        dataType: 'json',
        async: false,
        success: function(JSON) {
            database = JSON;
        }
    });

    // loop through database object and create array with unique table names
    // ASSUMES: first element of 2d array is table name, second is column name
    for (var i = 0, len = database.length; i < len; i++) {
        currentTable = database[i][0];
        var inTables = (tableChoices.indexOf(currentTable) > -1); // is current table already in tableChoices?

        // if currentTable is not already in tables,
        if (!inTables)
            tableChoices.push(currentTable); // add it to tables
    }
}

// displays elements of tableChoices in tableDropdown element
// CLEAN: figure out how generalize this function by passing in a parameter
// CLEAN: fix this elx and ely bullshit
function displayTables() {
    for (var i = 0; i < tableChoices.length; i++) {
        var optn = tableChoices[i];
        var elx = document.createElement("option");
        elx.textContent = optn;
        elx.value = optn;

        var ely = document.createElement("option");
        ely.textContent = optn;
        ely.value = optn;

        tableDropdownX.appendChild(elx);
        tableDropdownY.appendChild(ely);
    }
}


// CALLED BY USER

//CLEAN: Combine these
// when user chooses table:
function chooseTableX(tempTable) {
    // update global variables
    xColumn['table'] = tempTable;
    setColumns(xColumn['table'], columnChoicesX); // sets columnChoicesX according to current table

    // set html used for debugging
    document.getElementById('tableX').innerHTML = "Current x-table - " + xColumn['table'];

    // display new dropdowns
    //displayColumns();
    displayXColumn(columnChoicesX);
}

function chooseTableY(tempTable) {
    // update global variables
    yColumn['table'] = tempTable;
    setColumns(yColumn['table'], columnChoicesY); // sets columnChoicesY according to current table

    // set html used for debugging
    document.getElementById('tableY').innerHTML = "Current y-table - " + yColumn['table'];

    // display new dropdowns
    //displayColumns();
    displayYColumn(columnChoicesY);
}

// when user chooses x-axis
function chooseX(tempX) {
    // update global variable
    xColumn['column'] = tempX;
    document.getElementById('columnX').innerHTML = "Current x-axis - " + xColumn['column'] + " FROM " + xColumn['table']; // update html
}

// when user chooses y-axis
function chooseY(tempY) {
    // update global variables
    yColumn['column'] = tempY; 
    setType(tempY);

    // update html
    document.getElementById('columnY').innerHTML = "Current y-axis - " + yColumn['column'] + " FROM " + yColumn['table']; 
    document.getElementById('columnYType').innerHTML = "Current y type - " + yType;
}

// when user chooses operation,
function chooseOperation(value) {
    operation = value;

    document.getElementById('operation').innerHTML = "Current operation - " + operation;
}


// CALLED BY OTHER FUNCTION

// returns list of columns associated with given table name
// CLEAN: eliminate passing in global variable
function setColumns(tableName, columnChoices) {
    // clear existing columns
    columnChoices.length = 0;

    var currentTable;
    var currentColumn;

    // loop through database object and grab column names associated with given table name
    // ASSUMES: first element of 2d array is table name, second is column name
    for (var i = 0, len = database.length; i < len; i++) {
        currentTable = database[i][0];
        currentColumn = database[i][1];

        // if table name matches
        if (tableName == currentTable) {
        columnChoices.push(currentColumn);
        }
    }
}

/*
// displays column dropdown
function displayColumns(columnChoices) {
    // delete options for old column dropdowns
    removeOptions(xDropdown);
    removeOptions(yDropdown);

    // loops over columns, adding those that correspond to table
    // CLEAN: don't know why need elx and ely separately, but it works
    for (var i = 0; i < columnChoices.length; i++) {
        var optn = columnChoices[i];

        // creates element to be added
        var elx = document.createElement("option");
        elx.textContent = optn;
        elx.value = optn;

        // creates element to be added
        var ely = document.createElement("option");
        ely.textContent = optn;
        ely.value = optn;

        // appends elements
        xDropdown.appendChild(elx);
        yDropdown.appendChild(ely);
    }
}
*/

function displayXColumn(columnChoices) {
    // delete options for old column dropdowns
    removeOptions(xDropdown);

    // loops over columns, adding those that correspond to table
    // CLEAN: don't know why need elx and ely separately, but it works
    for (var i = 0; i < columnChoices.length; i++) {
        var optn = columnChoices[i];

        // creates element to be added
        var elx = document.createElement("option");
        elx.textContent = optn;
        elx.value = optn;

        // appends elements
        xDropdown.appendChild(elx);
    }
}

function displayYColumn(columnChoices) {
    // delete options for old column dropdowns
    removeOptions(yDropdown);

    // loops over columns, adding those that correspond to table
    // CLEAN: don't know why need elx and ely separately, but it works
    for (var i = 0; i < columnChoices.length; i++) {
        var optn = columnChoices[i];

        // creates element to be added
        var ely = document.createElement("option");
        ely.textContent = optn;
        ely.value = optn;

        // appends elements
        yDropdown.appendChild(ely);
    }
}

// removes all but first element of given <select> element
function removeOptions(selectElement) {
    //var i;
    var L = selectElement.options.length - 1;
    for(var i = L; i > 0; i--) {
       selectElement.remove(i);
    }
 }
  
// returns type associated with column passed in
// CLEAN: use something other than global variable
function setType(tempY) {

    var currentColumn;
    var currentType;

    // loop through database object and grab column type associated with chosen column
    // ASSUMES: third element of 2d array is column type
    for (var i = 0, len = database.length; i < len; i++) {
        currentColumn = database[i][1];
        currentType = database[i][2];

        // if column name matches
        if (tempY == currentColumn)
            yType = currentType;
    }
}


// type: -1 for no operation (disables step), 0 for avg, 1 for sum
// CLEAN: combine error alerts into a general function (named specifed?)
function getGraph(xColumn, yColumn, yType, operation) {

    // if table is unspecified
    if (xColumn['table'] == 'unspecified') {
        alert('Please specify a table for the x-axis');
        return;
    }

    if (yColumn['table'] == 'unspecified') {
        alert('Please specify a table for the y-axis');
        return;
    }

    // if x-column is unspecified
    if (xColumn['column'] == 'unspecified') {
        alert('Please specify an x-column');
        return;
    }

    // if y-column is unspecified
    if (yColumn['column'] == 'unspecified') {
        alert('Please specify a y-column');
        return;
    }

    // if operation is unspecified
    if (operation == 'unspecified') {
        alert('Please specify an operation');
        return;
    }

    // construct strings for sql queries
    var A = xColumn['table'] + "," + xColumn['column'];
    var B = yColumn['table'] + "," + yColumn['column'] + "," + yType;

    // requests appropriate data
    $.post($SCRIPT_ROOT + '/request', { type: operation, itemA: A, itemB: B, filter: "", step: 1 }, function(JSON) {

    /* CLEAN: get this to work synchronously so no need for separate 'update' and 'getGraph' buttons
$.ajax({
    url: $SCRIPT_ROOT + '/request',
    data: { type: 0, itemA: A, itemB: B, filter: "", step: 1 },
    dataType: 'json',
    async: false,
    success: function(JSON) {
        */

        var tmp = JSON.toString();
        var allVars = tmp.split(",");

        // check if first character is '{', then it worked
        // if not, then bad response
        if (isNaN(tmp[0])) {
            alert('You cannot graph this');
            return;
        }

        // gets odd values from array, which are x-vals
        var x = allVars.filter((element, index) => {
            return index % 2 === 1;
        });

        // gets even values from array, which are y-vals
        var y = allVars.filter((element, index) => {
            return index % 2 === 0;
        });

        // sets graph x-values
        myChart.config.data.labels = x;

        // sets graph y-values
        myChart.config.data.datasets[0].data = y;
        
        //}
   // });
    }, "json")
    .fail(function() {
        alert('error');
    });

    setTimeout(function() {
        myChart.update();
    }, 5000);
}


function dropToggleColumn() {
    document.getElementById("setColumn").classList.toggle("show");
}

function updateGraph() {
    myChart.update();
}

