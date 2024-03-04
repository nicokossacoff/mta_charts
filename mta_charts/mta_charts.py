import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import warnings
import os
import plotly.graph_objs as go


warnings.filterwarnings("ignore")
matplotlib.rc("lines", linewidth= 1.5)
matplotlib.rc("figure", figsize= (12,6))

class Fitted:
    def __init__(self, path: str):
        files = [file for file in os.listdir(path) if ("$" not in file) and (file.endswith(".xlsx"))]
        self.d = {file[:-5]: pd.read_excel(path + file, sheet_name= "AvM") for file in files}

        dates = pd.Series(pd.date_range(start= "2023-08-01", end= "2024-01-31", freq= "D"))
        for (key, value) in self.d.items():
            value["Dates"] = dates

    def actual_vs_fitted(self, model: str, raise_errors: bool = False):
        try:
            actual = go.Scatter(x= self.d[model]["Dates"],
                                y= self.d[model]["Actual"],
                                mode= "lines",
                                line= dict(color= "#001D38"),
                                name= "actual"
                                )
            fitted = go.Scatter(x= self.d[model]["Dates"],
                                y= self.d[model]["Fitted"],
                                mode= "lines",
                                line= dict(color="#4DBAC1"),
                                name= "fitted"
                                )
            residual = go.Scatter(x= self.d[model]["Dates"],
                                  y= self.d[model]["Residual"],
                                  mode= "lines",
                                  line= dict(color= "#FF245B"),
                                  name= "residual"
                                  )
            trace = [actual, fitted, residual]

            fig = go.Figure(data= trace)
            fig.update_layout(yaxis= dict(title= "KPI",
                                          showline= True,
                                          linecolor= "black",
                                          showgrid= True,
                                          gridcolor= "lightgrey",
                                          ticks= "outside"
                                          ),
                              xaxis= dict(title= "Date",
                                          showline= True,
                                          linecolor= "black",
                                          showgrid= True,
                                          gridcolor= "lightgrey",
                                          ticks= "outside"
                                          ),
                              plot_bgcolor= "white",
                              title= "Actual vs. Fitted"
                              )
            fig.show()
        except Exception as error:
            if raise_errors == False:
                print("An error ocurred...")
                print(error)
            else:
                print("An error ocurred...")
                raise

class Correlations:
    def __init__(self, data: str, kpi: dict, start_date: str, end_date: str):
        self.df = pd.read_csv(data)
        self.kpi = kpi

        self.df.drop(columns= ["Unnamed: 0"], inplace= True)
        self.df.Date = pd.to_datetime(self.df.Date)
        self.df = self.df.loc[(self.df.Date >= pd.to_datetime(start_date)) & (self.df.Date <= pd.to_datetime(end_date))]
        self.df = self.df.pivot_table(index= "Date", columns= "Serie", values= "Value", aggfunc= "first")
        self.df.fillna(0, inplace= True)

        self.dates = pd.Series(self.df.index)
    
    def kpi_vs_media_corr(self, model: str, media_var: str, scatter: bool = False, raise_errors: bool = False):
        try:
            media = " - ".join(media_var.split("-")[-2:])

            if scatter == True:
                kpi_series = go.Scatter(x= self.dates,
                                        y= self.df[self.kpi[model]],
                                        mode= "markers",
                                        line= dict(color= "#001D38"),
                                        name= model
                                        )
                media_series = go.Scatter(x= self.dates,
                                          y= self.df[media_var],
                                          mode= "markers", 
                                          line= dict(color="#4DBAC1"),
                                          name= media_var
                                          )
                trace = [kpi_series, media_series]

                fig = go.Figure(data= trace)
                fig.update_layout(title= "Correlations",
                                  plot_bgcolor= "white",
                                  yaxis= dict(title= model,
                                              showline= True,
                                              linecolor= "black",
                                              showgrid= True,
                                              gridcolor= "lightgrey",
                                              ticks= "outside"
                                              ),
                                  yaxis2 = dict(title= media,
                                                overlaying= "y",
                                                side= "right",
                                                showline= True,
                                                linecolor= "black",
                                                ticks= "outside"
                                                ),
                                  xaxis = dict(title= "Date",
                                               showline= True,
                                               linecolor= "black",
                                               showgrid= True,
                                               gridcolor= "lightgrey",
                                               ticks= "outside"
                                               ),
                                  legend= dict(x= 0.35,
                                               y= 1.2,
                                               orientation= "v"
                                               )
                                  )

                fig.show()
            else:
                kpi_series = go.Scatter(x= self.dates,
                                        y= self.df[self.kpi[model]],
                                        mode= "lines",
                                        line= dict(color= "#001D38"), 
                                        name= model
                                        )
                media_series = go.Scatter(x= self.dates,
                                          y= self.df[media_var],
                                          mode= "lines",
                                          line= dict(color="#4DBAC1"),
                                          name= media_var,
                                          yaxis= "y2"
                                          )
                trace = [kpi_series, media_series]

                fig = go.Figure(data= trace)
                fig.update_layout(title= "Correlations",
                                  plot_bgcolor= "white",
                                  yaxis= dict(title= model,
                                              showline= True,
                                              linecolor= "black",
                                              showgrid= True,
                                              gridcolor= "lightgrey",
                                              ticks= "outside"
                                              ),
                                  yaxis2 = dict(title= media,
                                                overlaying= "y",
                                                side= "right",
                                                showline= True,
                                                linecolor= "black",
                                                ticks= "outside"
                                                ),
                                  xaxis = dict(title= "Date",
                                               showline= True,
                                               linecolor= "black",
                                               showgrid= True,
                                               gridcolor= "lightgrey",
                                               ticks= "outside"
                                               ),
                                  legend= dict(x= 0.35,
                                               y= 1.2,
                                               orientation= "v"
                                               )
                                  )

                fig.show()
        except Exception as error:
            if raise_errors == False:
                print("There was an error...")
                print(error)
            else:
                raise
    
    def media_corr(self, media_vars: list, scatter: bool = False, raise_errors: bool = False):
        try:
            media = []
            for var in media_vars:
                var = " - ".join(var.split("-")[-2:])
                media.append(var)

            if scatter == True:
                media1 = go.Scatter(x= self.dates,
                                    y= self.df[media_vars[0]],
                                    mode= "markers",
                                    line= dict(color= "#001D38"),
                                    name= media[0]
                                    )
                media2 = go.Scatter(x= self.dates,
                                    y= self.df[media_vars[1]],
                                    mode= "markers", 
                                    line= dict(color="#4DBAC1"),
                                    name= media[1],
                                    yaxis= "y2"
                                    )
                trace = [media1, media2]

                fig = go.Figure(data= trace)
                fig.update_layout(title= "Correlations",
                                  plot_bgcolor= "white",
                                  yaxis= dict(title= media[0],
                                              showline= True,
                                              linecolor= "black",
                                              showgrid= True,
                                              gridcolor= "lightgrey",
                                              ticks= "outside"
                                              ),
                                  yaxis2 = dict(title= media[1],
                                                overlaying= "y",
                                                side= "right",
                                                showline= True,
                                                linecolor= "black",
                                                ticks= "outside"
                                                ),
                                  xaxis = dict(title= "Date",
                                               showline= True,
                                               linecolor= "black",
                                               showgrid= True,
                                               gridcolor= "lightgrey",
                                               ticks= "outside"
                                               ),
                                  legend= dict(x= 0.35,
                                               y= 1.2,
                                               orientation= "v"
                                               )
                                  )

                fig.show()
            else:
                media1 = go.Scatter(x= self.dates,
                                    y= self.df[media_vars[0]],
                                    mode= "lines",
                                    line= dict(color= "#001D38"), 
                                    name= media_vars[0]
                                    )
                media2 = go.Scatter(x= self.dates,
                                    y= self.df[media_vars[1]],
                                    mode= "lines",
                                    line= dict(color="#4DBAC1"),
                                    name= media_vars[1],
                                    yaxis= "y2"
                                    )
                trace = [media1, media2]

                fig = go.Figure(data= trace)
                fig.update_layout(title= "Correlations",
                                  plot_bgcolor= "white",
                                  yaxis= dict(title= media[0],
                                              showline= True,
                                              linecolor= "black",
                                              showgrid= True,
                                              gridcolor= "lightgrey",
                                              ticks= "outside"
                                              ),
                                  yaxis2 = dict(title= media[1],
                                                overlaying= "y",
                                                side= "right",
                                                showline= True,
                                                linecolor= "black",
                                                ticks= "outside"
                                                ),
                                  xaxis = dict(title= "Date",
                                               showline= True,
                                               linecolor= "black",
                                               showgrid= True,
                                               gridcolor= "lightgrey",
                                               ticks= "outside"
                                               ),
                                  legend= dict(x= 0.35,
                                               y= 1.2,
                                               orientation= "v"
                                               )
                                  )

                fig.show()
        except Exception as error:
            if raise_errors == False:
                print("There was an error...")
                print(error)
            else:
                raise
