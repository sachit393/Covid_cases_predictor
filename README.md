# Covid_cases_predictor
<br>
An ARIMA model to forecast COVID-19 cases(new ones) in Kerela five days in future
<br>
<br>
<ul>
  <li>The python script itself scraps the latest data of cases(for previous day) from GOK website and adds it to csv file</li>
  <br>
  <li>New ARIMA model is created and trained on updated data and forecast for 5 days in future</li>
  <br>
  <li>Forecasts are plotted by using Google charts and plot of the existing data(on which model is trained) is made using matplotlib</li>
</ul>
<br>
<h2>STEPS TO RUN</h2>
<br>
<ul>
  
  <li>Clone the repository</li>
  <li>Install pandas,numpy,matplotlib,statsmodels,beautiful soup and Django using pip</li>
  <li>CD into covidpredictor(Topmost) directory</li>
  <li>Run the command "python manage.py runserver" in the command line</li>
</ul>
