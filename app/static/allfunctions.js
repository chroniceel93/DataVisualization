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
function exportsavedata(charttype, dbin, xin, yin, ytype){
    var sentdata = charttype + " " + dbin + " " + xin + " " + yin + " " + ytype;
    var a = document.createElement('a');
    a.href = 'data:attachment/text,' + encodeURI(sentdata);
    a.target = '_blank';
    a.download = 'GraphData.txt';
    a.click();
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

    // this used to be .getJSON, but now have syncronous option
    $.ajax({
        url: $SCRIPT_ROOT + '/db_all',
        dataType: 'json',
        async: false,
        success: function(JSON) {
            // loop through JSON object and create array with unique table names
            // ASSUMES: first element of 2d array is table name, second is column name
            for (var i = 0, len = JSON.length; i < len; i++) {
                currentTable = JSON[i][0];
                var inTables = (tableChoices.indexOf(currentTable) > -1); // is current table already in tableChoices?

                // if currentTable is not already in tables,
                if (!inTables)
                    tableChoices.push(currentTable); // add it to tables
            }
        }
    });
}

// displays elements of tableChoices in tableDropdown element
// CLEAN: figure out how generalize this function by passing in a parameter
function displayTables() {
    for (var i = 0; i < tableChoices.length; i++) {
        var optn = tableChoices[i];
        var el = document.createElement("option");
        el.textContent = optn;
        el.value = optn;

        tableDropdown.appendChild(el);
    }
}




// when user chooses table:
function chooseTable(tempTable) {
    // update global variables
    table = tempTable;
    setColumns(table, columnChoices); // sets columnChoices according to current table

    // set html used for debugging
    document.getElementById('table').innerHTML = "Current table - " + table;

    // display new dropdowns
    displayColumns();
}

// when user chooses x-axis
function chooseX(tempX) {
    xColumn = tempX; // update global variable
    document.getElementById('columnX').innerHTML = "Current x-axis - " + xColumn; // update html
}

// when user chooses y-axis
function chooseY(tempY) {
    // update global variables
    yColumn = tempY; 
    setType(yColumn);

    // update html
    document.getElementById('columnY').innerHTML = "Current y-axis - " + yColumn; 
    document.getElementById('columnYType').innerHTML = "Current y type - " + yType;
}

// when user chooses operation,
function chooseOperation(value) {
    operation = value;
}




// returns list of columns associated with given table name
// CLEAN: eliminate passing in global variable
function setColumns(tableName, columnChoices) {
    // clear existing columns
    columnChoices.length = 0;

    $.ajax({
        url: $SCRIPT_ROOT + '/db_all',
        dataType: 'json',
        async: false,
        success: function(JSON) {
            var currentTable;
            var currentColumn;

            // loop through JSON object and grab column names associated with given table name
            // ASSUMES: first element of 2d array is table name, second is column name
            for (var i = 0, len = JSON.length; i < len; i++) {
                currentTable = JSON[i][0];
                currentColumn = JSON[i][1];

                // if table name matches
                if (tableName == currentTable) {
                columnChoices.push(currentColumn);
                }
            }
        }
    });
}

// displays column dropdown
function displayColumns() {
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
function setType(yColumn) {
    $.ajax({
        url: $SCRIPT_ROOT + '/db_all',
        dataType: 'json',
        async: false,
        success: function(JSON) {
            var currentColumn;
            var currentType;

            // loop through JSON object and grab column type associated with chosen column
            // ASSUMES: third element of 2d array is column type
            for (var i = 0, len = JSON.length; i < len; i++) {
                currentColumn = JSON[i][1];
                currentType = JSON[i][2];

                // if column name matches
                if (yColumn == currentColumn)
                    yType = currentType;
            }
        }
    });
}


// type: -1 for no operation (disables step), 0 for avg, 1 for sum
function getGraph(table, xColumn, yColumn, yType, operation) {

    // construct strings for sql queries
    var A = table + "," + xColumn;
    var B = table + "," + yColumn + "," + yType;

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
}


function dropToggleColumn() {
    document.getElementById("setColumn").classList.toggle("show");
}

function updateGraph() {
    myChart.update();
}

