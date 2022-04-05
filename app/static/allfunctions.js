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