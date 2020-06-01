from django.shortcuts import render
from django.views.generic import TemplateView
from .fusioncharts import FusionCharts


class Home(TemplateView):
    template_name = 'index.html'


class BalanceCheck(TemplateView):
    template_name = 'dashboard/balance_check.html'


class BalanceView(TemplateView):
    template_name = 'dashboard/balance.html'

    def myFirstChart(self):
        dataSource = {}
        chartConfig = {}
        chartConfig["caption"] = "Countries With Most Oil Reserves [2017-18]"
        chartConfig["subCaption"] = "In MMbbl = One Million barrels"
        chartConfig["xAxisName"] = "Country"
        chartConfig["yAxisName"] = "Reserves (MMbbl)"
        chartConfig["numberSuffix"] = "K"
        chartConfig["theme"] = "fusion"
        dataSource["chart"] = chartConfig
        dataSource["data"] = []
        dataSource["data"].append({"label": 'Venezuela', "value": '290'})
        dataSource["data"].append({"label": 'Saudi', "value": '290'})
        dataSource["data"].append({"label": 'Canada', "value": '180'})
        dataSource["data"].append({"label": 'Iran', "value": '140'})
        dataSource["data"].append({"label": 'Russia', "value": '115'})
        dataSource["data"].append({"label": 'Russia', "value": '115'})
        dataSource["data"].append({"label": 'UAE', "value": '100'})
        dataSource["data"].append({"label": 'US', "value": '30'})
        dataSource["data"].append({"label": 'China', "value": '30'})
        column2D = FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)
        return column2D.render()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['output'] = self.myFirstChart()
        print(context['output'])


def myFirstChart(request):
    dataSource = {}
    chartConfig = {}
    chartConfig["caption"] = "Countries With Most Oil Reserves [2017-18]"
    chartConfig["subCaption"] = "In MMbbl = One Million barrels"
    chartConfig["xAxisName"] = "Country"
    chartConfig["yAxisName"] = "Reserves (MMbbl)"
    chartConfig["numberSuffix"] = "K"
    chartConfig["theme"] = "fusion"
    dataSource["chart"] = chartConfig
    dataSource["data"] = []
    dataSource["data"].append({"label": 'Venezuela', "value": '290'})
    dataSource["data"].append({"label": 'Saudi', "value": '290'})
    dataSource["data"].append({"label": 'Canada', "value": '180'})
    dataSource["data"].append({"label": 'Iran', "value": '140'})
    dataSource["data"].append({"label": 'Russia', "value": '115'})
    dataSource["data"].append({"label": 'Russia', "value": '115'})
    dataSource["data"].append({"label": 'UAE', "value": '100'})
    dataSource["data"].append({"label": 'US', "value": '30'})
    dataSource["data"].append({"label": 'China', "value": '30'})
    column2D = FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)
    result = render(request, 'dashboard/balance_demo.html', {'output': column2D.render()})
    print(column2D.render())
    return result


# def chart(request):
#     # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
#     dataSource = {}
#     dataSource['chart'] = {
#         "caption": "Monthly revenue for last year",
#             "subCaption": "Harry's SuperMart",
#             "xAxisName": "Month",
#             "yAxisName": "Revenues (In USD)",
#             "numberPrefix": "$",
#             "theme": "zune"
#         }
#
#     # The data for the chart should be in an array where each element of the array is a JSON object
#     # having the `label` and `value` as key value pair.
#
#     dataSource['data'] = []
#     # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
#     for key in Revenue.objects.all():
#       data = {}
#       data['label'] = key.Month
#       data['value'] = key.MonthlyRevenue
#       dataSource['data'].append(data)
#
#     # Create an object for the Column 2D chart using the FusionCharts class constructor
#     column2D = FusionCharts("column2D", "ex1" , "600", "350", "chart-1", "json", dataSource)
#     return render(request, 'index.html', {'output': column2D.render()})

