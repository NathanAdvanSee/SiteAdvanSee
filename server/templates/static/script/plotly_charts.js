// server/templates/static/script/plotly_charts.js
function renderPlotlyChart(elementId, graphJson) {
    const graphData = JSON.parse(graphJson);
    Plotly.newPlot(elementId, graphData.data, graphData.layout);
}