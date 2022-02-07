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
  <font size="3">The dataset used on this project is a synthetic financial dataset generated in a simulator called PaySim and available on kaggle. The PaySim simulator uses aggregated data from private dataset to generate a synthetic dataset that resembles the normal operation of transactions and adds malicious behaviour to later evaluate the performance of fraud detection methods. The dataset used to build the solution has the following attributes:</font></li>
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
  <li><font size="3"><b>Machine learning:</b> evaluating different algorithms and compare their results based on cross-validation. For the sake of this step a good candidate algorithm should perform better than the random baseline estimator.</font></li>
<br>
  <li><font size="3"><b>Hiperparameter fine tuning:</b> randomly test different hyperparameter values in order to find some combination that improves model performance.</font></li>
<br>
  <li><font size="3"><b>Error interpretation:</b> after choosing the best performing model, in the next step model performance needs to be translated to business results.</font></li>
<br>
  <li><font size="3"><b>Model deployment:</b> deploying the machine learning model to cloud environment so predictions can be accessed via API requests.</font></li>
<br>  
</ol>







<h1>5- Main insights</h1>

<br>
<p><font size="3">- Fraud happens mostly AM. 
    <br>Answer: <b>TRUE</b>. Fraud transactions mostly happen AM.</font></p>


<a href="https://drive.google.com/uc?export=view&id=1j-R4ncXCgW_Dfx5OOT3QpZLxESL579mc"><img src="https://drive.google.com/uc?export=view&id=1j-R4ncXCgW_Dfx5OOT3QpZLxESL579mc" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />

<br>
    
<p><font size="3">Non-fraud transactions, however, happen in the opposite direction.</font></p>    
    
<a href="https://drive.google.com/uc?export=view&id=1hFy5U25SN9QPmBiGzgx2GkbaLToJe6DD"><img src="https://drive.google.com/uc?export=view&id=1hFy5U25SN9QPmBiGzgx2GkbaLToJe6DD" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />    

    
<br>    
<br>
<p><font size="3">- Fraud transactions frequencies follow the trend of non-Fraud transactions to make it dificult to track. 
    <br>Answer: <b>FALSE</b>. Fraud happens with diferent frequencies distribution when compared to non-fraud transactions.</font></p>

<p><font size="3"><i>Fraud transactions during days of week:</i></font></p>   
    
<a href="https://drive.google.com/uc?export=view&id=1oNke6PeroRo3wAfMkwOnM-Vb-Kn9m93g"><img src="https://drive.google.com/uc?export=view&id=1oNke6PeroRo3wAfMkwOnM-Vb-Kn9m93g" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />    

<p><font size="3"><i>Non-fraud transactions during days of week:</i></font></p>   
    
<a href="https://drive.google.com/uc?export=view&id=1KJNiqZ_YZia3AqMZJ0ZWUPwoBcROVLfk"><img src="https://drive.google.com/uc?export=view&id=1KJNiqZ_YZia3AqMZJ0ZWUPwoBcROVLfk" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />      
    
    
    
<br>
<p><font size="3">- Most fraud transactions happen when origin new balance is zero. 
    <br>Answer: <b>TRUE</b>.  After most fraud transactions the remaining origin balance is zero.</font></p>


<a href="https://drive.google.com/uc?export=view&id=1lZ_ZOvu67ASbxSCqTeOetgAEuHsZDcIK"><img src="https://drive.google.com/uc?export=view&id=1lZ_ZOvu67ASbxSCqTeOetgAEuHsZDcIK" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />    


    
<p><font size="3">Non-fraud transactions, however, the non-zero/zero ratio is different.</font></p>    
    
<a href="https://drive.google.com/uc?export=view&id=1o7fLYfx0oJJwvx_yEkEbddK4sO_Vr_UW"><img src="https://drive.google.com/uc?export=view&id=1o7fLYfx0oJJwvx_yEkEbddK4sO_Vr_UW" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />        
    
    
<br>    
<p><font size="3">Other hypothesis raised, as well as other insights can be checked out in the main notebook.</font></p>     
    
    
    
    
<h1>6- Machine Learning models</h1>

<br>
<p><font size="3">Models evaluated:</font></p>


<ul>
  <li><font size="3">Random model (baseline)</font></li>
  <li><font size="3">Logistic Regression</font></li>
  <li><font size="3">Random Forest</font></li>
  <li><font size="3">XGBoost</font></li>
  <li><font size="3">K-Nearest Neighbors</font></li>
</ul>






<h1>7- Machine Learning performance</h1>
    
    
<br>    
<table border="1">
   <thead>
   <tr>
       <th><font size="3">Model name</font></th>
       <th><font size="3">Accuracy CV</font></th>
       <th><font size="3">Balanced Accuracy CV</font></th>
       <th><font size="3">ROC-AUC CV</font></th>
       <th><font size="3">Precision CV</font></th>
       <th><font size="3">F1-score CV</font></th>
       <th><font size="3">Recall CV</font></th>
   </tr>
   </thead>
   <tbody>
   <tr>
       <td><font size="3">Random classifier (baseline)</font></td>
       <td><font size="3">0.997404</font></td>
       <td><font size="3">0.499523</font></td>
       <td><font size="3">0.499523</font></td>
       <td><font size="3">0.000359</font></td>
       <td><font size="3">0.000367</font></td>
       <td><font size="3">0.000375</font></td>
   </tr>
   <tr>
       <td><font size="3">Logistic Regression</font></td>
       <td><font size="3">0.998893</font></td>
       <td><font size="3">0.572757</font></td>
       <td><font size="3">0.867702</font></td>
       <td><font size="3">0.894009</font></td>
       <td><font size="3">0.250323</font></td>
       <td><font size="3">0.145536</font></td>
   </tr>
          <tr>
       <td><font size="3">Random Forest</font></td>
       <td><font size="3">0.999724</font></td>
       <td><font size="3">0.893658</font></td>
       <td><font size="3">0.966993</font></td>
       <td><font size="3">0.993845</font></td>
       <td><font size="3">0.87861</font></td>
       <td><font size="3">0.787322</font></td>
   </tr>
          <tr>
       <td><font size="3">XGBoost</font></td>
       <td><font size="3">0.999763</font></td>
       <td><font size="3">0.912596</font></td>
       <td><font size="3">0.998484</font></td>
       <td><font size="3">0.986105</font></td>
       <td><font size="3">0.898509</font></td>
       <td><font size="3">0.825206</font></td>
   </tbody>
       <td><font size="3">KNN</font></td>
       <td><font size="3">0.999649</font></td>
       <td><font size="3">0.873391</font></td>
       <td><font size="3">0.915126</font></td>
       <td><font size="3">0.9698</font></td>
       <td><font size="3">0.843823</font></td>
       <td><font size="3">0.746812</font></td>
</table>
    
    
    
<br>
<p><font size="3">K-fold (number of splits=10) cross-validation provided replicates that allowed standard deviation calculation of each metric evaluated (Accuracy, Balanced Accuracy, ROC-AUC, Precision, F1-score, Recall). Cross-validation step was applied to the best performing model in the previous step (XGBoost).</font></p><br>

    
<table border="1">
   <thead>
   <tr>
       <th><font size="3">Model name</font></th>
       <th><font size="3">Accuracy CV</font></th>
       <th><font size="3">Balanced Accuracy CV</font></th>
       <th><font size="3">ROC-AUC CV</font></th>
       <th><font size="3">Precision CV</font></th>
       <th><font size="3">F1-score CV</font></th>
       <th><font size="3">Recall CV</font></th>
   </tr>
   </thead>
   <tbody>
   <tr>
       <td><font size="3">XGBoost</font></td>
       <td><font size="3">1.0 +/-0.0</font></td>
       <td><font size="3">0.91 +/-0.01</font></td>
       <td><font size="3">1.0 +/-0.0</font></td>
       <td><font size="3">0.98 +/-0.01</font></td>
       <td><font size="3">0.9 +/-0.01</font></td>
       <td><font size="3">0.83 +/-0.02</font></td>
   </tr>         
   </tbody>
</table>    
    
    
    

<br>
    
    
    
    

<h1>8- Hyperparameter fine tuning</h1>

<br>
<p><font size="3">Model hyperparameters were adjusted via random search fine tuning in order to improve model performance.The following table shows the metrics for the XGBoost tuned model:</font></p>
<br>

<table border="1">
   <thead>
   <tr>
       <th><font size="3">Model name</font></th>
       <th><font size="3">Accuracy CV</font></th>
       <th><font size="3">Balanced Accuracy CV</font></th>
       <th><font size="3">ROC-AUC CV</font></th>
       <th><font size="3">Precision CV</font></th>
       <th><font size="3">F1-score CV</font></th>
       <th><font size="3">Recall CV</font></th>
   </tr>
   </thead>
   <tbody>
   <tr>
       <td><font size="3">XGBoost</font></td>
       <td><font size="3">1.0 +/-0.0</font></td>
       <td><font size="3">0.92 +/-0.01</font></td>
       <td><font size="3">1.0 +/-0.0</font></td>
       <td><font size="3">0.95 +/-0.01</font></td>
       <td><font size="3">0.89 +/-0.01</font></td>
       <td><font size="3">0.84 +/-0.01</font></td>
   </tr>         
   </tbody>
</table>

<br>
<p><font size="3">As expected fine tuning did not improve significantly model's performance.</font>    
<br>
    
    
    
    
 
    
    
    
    


<h1>9- Model performance to business performance</h1>

    
<br>
<p><font size="3">Transaction Tracker's forecasted revenue and profits of implementing the proposed machine learning model:</font></p>    
    
    
<br>
    <p><font size="3"><i>Revenue:</i></font></p>

<ul>
  <li><font size="3">Sum of amount of fraudulent transactions correctly detected by Transaction Tracker: 3,719,735,063.56 dollars</font></li><br>
  <li><font size="3">Transaction Tracker amount received for detecting fraudulent transactions (25%): 929,933,765.89 dollars</font></li><br>
  <li><font size="3">Sum of amount of non-fraudulent transactions detected by Transaction Tracker as fraud: 27,691,057.44 dollars</font></li><br>
  <li><font size="3">Transaction Tracker amount received for this transaction operation (5%): 1,384,552.87 dollars</font></li><br>
  <li><font size="3">Sum of amount of fraudulent transactions  wrongfully detected by Transaction Tracker as non-fraud: 85,846,430.44 dollars</font></li><br>  
  <li><font size="3">Transaction Tracker refound cashback (-100%): 85,846,430.44 dollars</font></li><br>
</ul>    
    

<p><font size="3"><i>Profit:</i></font></p>

<ul>
  <li><font size="3">(25%): 929,933,765.89</font></li><br>
  <li><font size="3">+(5%): 1,384,552.87</font></li><br>
  <li><font size="3">-(100%): 85,846,430.44</font></li><br>
    <li><font size="3"><b>Total profit: 845,471,888.32</b></font></li><br>
</ul>        


<p><font size="3">Now we are going to point out the advantages for client that hires the service provided by Transaction Tracker. Again, we will assume for this scenario that the hiring client uses the random baseline estimator.</font></p>      
<br>    
    
<p><font size="3">Baseline model:</font></p>

<ul>
  <li><font size="3">Sum of amount of fraudulent transactions correctly detected by baseline model: 1,789,207.89 dollars</font></li><br>
  <li><font size="3">Sum of amount of fraudulent transactions wrongfully detected by baseline model as non-fraud: 3,803,792,286.11 dollars.</font></li><br>
</ul>      

    
    
<p><font size="3">Expenses (loss) calculation:</font></p>

<ul>
  <li><font size="3">Without hiring Transaction Tracker services: 3,803,792,286.11 dollars</font></li><br>
  <li><font size="3">Hiring Transaction Tracker services:<br><br>
      (25%): 929,933,765.89<br><br>
      +(5%): 1,384,552.87<br><br>
      Sum: 931,318,318.76<br><br>
      <b>Total saved by hiring Transaction Tracker services: 2,875,243,073.09 dollars.</b></font></li><br>
</ul>       
    
    
<br>

<a href="https://drive.google.com/uc?export=view&id=1R2-Yb-ljCzx0NR2Wo_UtzQGAAxLvO2Tf"><img src="https://drive.google.com/uc?export=view&id=1R2-Yb-ljCzx0NR2Wo_UtzQGAAxLvO2Tf" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />

    
<br>

<br>

<a href="https://drive.google.com/uc?export=view&id=1AXr3VL3WW4_gOktXnZBoDVRct1n3gdF5"><img src="https://drive.google.com/uc?export=view&id=1AXr3VL3WW4_gOktXnZBoDVRct1n3gdF5" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />

    
<br>
    
    

<h1>10- Model deployment</h1>

<br>

<ul>
  <li><font size="3">Machine learning model was successfully deployed on Heroku cloud. Predictions can be acessed using the following endpoint: <a href="https://transaction-fraud-tracker.herokuapp.com/transactiontracker/predict">https://transaction-fraud-tracker.herokuapp.com/transactiontracker/predict</a>.</font>
      
<font size="3">To access predictions the user should make a API request (POST) sending the information about some transaction as json. The request should return the same data with the prediction included. Some model unseen data for testing purposes can be acessed here: <a href="https://drive.google.com/u/1/uc?id=1XBPpvCjOQhVDgHFeujoQ9RIDskns2-pp&export=download">https://drive.google.com/u/1/uc?id=1XBPpvCjOQhVDgHFeujoQ9RIDskns2-pp&export=download</a>  </font>
</ul>    
    

  
    
    
    
    

<h1>11- Conclusions</h1>

<br>
<p><font size="3">Althought the presented results is not the best that could be achieved and there is room for model improvements decreasing its corresponding error, the proposed solution reached satisfactory results performing better than random estimator satisfying the needs of the business. From the business standpoint, the proposed solution is capable of both generating profits for the Transaction Tracker company and reducing losses for the hiring client, therefore satisfying business needs.</font></p>
<br>

    
    
    
    
<h1>12- Next steps/Perspectives</h1>

<br>
   
    
<ul>
  <li><font size="3">Work on model improvements to reduce error metrics.</font></li>
</ul
