<h1><b><font color="#cc0000"><i>Creating a Solution for Fraud in Financial Transactions using Machine Learning</i></font></b></h1>





<h1>1- Overview, business context and challenges</h1>

<br>
<p><font size="3">Our fictious company named Transaction Tracker is a company specialized in fraud detection in financial transactions made through mobile devices. The company offers a service that guarantees the blocking of fraudulent transactions.</br>
    
And the company's business model is of the service type with monetization made by the performance of the service provided, which is, the user pays a fixed fee on the success in the detection of fraud of the customer's transactions.</br> 

</br>
However, Transaction Tracker is expanding and in order to acquire customers more quickly, it has adopted a very aggressive strategy. The strategy works as follows: 
</font></p>


</br>
<ol>
  <b><li><font size="3">The company will receive 25% of the value of each transaction that is truly detected as fraud.</font></li>
<br>
  <li><font size="3">The company will receive 5% of the value of each transaction detected as fraud, however the transaction is truly legitimate.</font></li>
<br>
  <li><font size="3">The company will refund 100% of the value to the customer, for each transaction detected as legitimate, however the transaction is truly a fraud.</font></li></b>
</ol>
</br>

<p><font size="3">With this aggressive strategy, the company assumes the risks of failing to detect fraud and is remunerated in the assertive detection of fraud.</font></p>

<p><font size="3">For the customer, it is an excellent deal to hire Transaction Tracker company. Despite the very high fee charged on success, 25%, the company reduces its costs with correctly detected fraudulent transactions and even the damage caused by an anti-fraud service error will be covered by the Blocker Fraud Company itself.</font></p>

<p><font size="3">For the company, in addition to getting many customers with this risky strategy of guaranteeing reimbursement in the event of a failure to detect customer fraud, it depends only on the precision and accuracy of the models built by its Data Scientists, that is, the more accurate the “Blocker Fraud” model, the higher the company's revenue. However, if the model has low accuracy, the company could have a huge loss.</font></p>


<p><font size="3"><b>The challenge:</b> The main goal of this project is to develop a machine learning model able to predict fraudulent transactions made through mobile devices where the corresponding predictions can be acessed via API.</font></p>


<p><font size="3">For the development of the solution, some import issues will be kept in mind:</font></p>

</br>
<ol>
  <li><font size="3">The performance of the machine learning model implemented.</font></li>
<br>
  <li><font size="3">The reliability of the implemented machine learning model in classifying transactions as legitimate or fraudulent.</font></li>
<br>
  <li><font size="3">The expected revenue by the company if we classify 100% of the transactions with the machine learning model.</font></li>
<br>
  <li><font size="3">The loss expected by the company in the event of a model failure.</font></li>
<br>  
  <li><font size="3">The expected profit by Transaction Tracker company when using the model.</font></li>
</ol>
</br>


<p><font size="3"><b>Disclaimer:</b> The business context herein presented is fictitious and was used only for the purpose of the development of this project.</font></p>


<p><font size="3">Datasets used in this project can be downloaded <a href="https://www.kaggle.com/ealaxi/paysim1">here</a>.</font></p>





<h1>2- Assumptions</h1>

<br>
<p><font size="3">For the purpose of the development, model implementation and business calculations we will be assuming the hiring client to currently control for fraud transactions using a random estimator.</font></p></br>






<h1>3- Data description</h1>

<br>
  <font size="3">The dataset used on this project is a synthetic financial dataset generated in a simulator called PaySim and available on kaggle. The PaySim simulator uses aggregated data from private dataset to generate a synthetic dataset that resembles the normal operation of transactions and adds malicious behaviour to later evaluate the performance of fraud detection methods.The dataset used to build the solution has the following attributes:</font></li>
<br>
<br>
<ul>
  <li><font size="3"><b>step - </b>maps a unit of time in the real world. In this case 1 step is 1 hour of time. Total steps 744 (30 days simulation).</font></li><br>
  <li><font size="3"><b>type - </b>CASH-IN, CASH-OUT, DEBIT, PAYMENT and TRANSFER.</font></li><br>
  <li><font size="3"><b>amount - </b>amount of the transaction in local currency.</font></li><br>
  <li><font size="3"><b>nameOrig - </b>customer who started the transaction</font></li><br>
  <li><font size="3"><b>oldbalanceOrg - </b>initial balance before the transaction</font></li><br>
  <li><font size="3"><b>newbalanceOrig - </b>new balance after the transaction</font></li><br>
  <li><font size="3"><b>nameDest - </b>customer who is the recipient of the transaction</font></li><br>
  <li><font size="3"><b>oldbalanceDest - </b>initial balance recipient before the transaction. Note that there is not information for customers that start with M (Merchants).</font></li><br>
  <li><font size="3"><b>newbalanceDest - </b>new balance recipient after the transaction. Note that there is not information for customers that start with M (Merchants).</font></li><br>
  <li><font size="3"><b>isFraud - </b>This is the transactions made by the fraudulent agents inside the simulation. In this specific dataset the fraudulent behavior of the agents aims to profit by taking control or customers accounts and try to empty the funds by transferring to another account and then cashing out of the system.</font></li><br>
  <li><font size="3"><b>isFlaggedFraud - </b>The business model aims to control massive transfers from one account to another and flags illegal attempts. An illegal attempt in this dataset is an attempt to transfer more than 200.000 in a single transaction.</font></li><br>
</ul>








<h1>4- Solution strategy</h1>

<br>
<ol>
  <li><font size="3"><b>Understanding the business and problems to be solved:</b> already described.</font></li>
<br>
  <li><font size="3"><b>Data colection:</b> downloading the corresponding .csv files from <a href="https://www.kaggle.com/ealaxi/paysim1">Kaggle</a> plattform.</font></li>
<br>
  <li><font size="3"><b>Data cleaning:</b> basic search for missing values, outliers and inconsistencies to make data suitable for further analysis. Adittionally a basic inspection including descriptive statistics (mean, standard deviation, range, skewness and kurtosis) should be also carried out.</font></li>
<br>
  <li><font size="3"><b>Feature engineering:</b> creating new features from the existing ones to assist in both exploratory data analysis (EDA) and machine learning modelling.</font></li>
<br>
  <li><font size="3"><b>Data filtering and selection:</b>  reducing the data based on business assumptions and constraints to make training set as close as possible to data in production.</font></li>
<br>
  <li><font size="3"><b>EDA:</b> exploring data to search for interesting insights and understand the impact of the features on the target variable (sales).</font></li>
<br>
  <li><font size="3"><b>Data preparation:</b> splitting the data into train/test sets and applying them scaling, encoding and transformation methods to make data suitable to machine learning.</font></li>
<br>
  <li><font size="3"><b>Feature selection:</b> selecting the most relevant attributes based on EDA results and suitable algorithm to maximize machine learning performance.</font></li>
<br>
  <li><font size="3"><b>Machine learning:</b> evaluating different algorithms and compare their results based on cross-validation. For the sake of this step a good candidate algorithm should perform better than the average-based baseline estimator.</font></li>
<br>
  <li><font size="3"><b>Hiperparameter fine tuning:</b> randomly test different hyperparameter values in order to find some combination that improves model performance.</font></li>
<br>
  <li><font size="3"><b>Error interpretation:</b> after choosing the best performing model, in the next step model performance needs to be translated to business results.</font></li>
<br>
  <li><font size="3"><b>Model deployment:</b> deploying the machine learning model to cloud environment so predictions can be accessed via API requests.</font></li>
<br>  
</ol>
