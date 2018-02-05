TODO:
1) write report 

QUESTIONS:
1)  when splitting my data 10 ways, I cannot split 1004 examples 10 ways. currently, I am doing 10 folds of 100 each.
     what should I do?

2) for the visualisation of a the 6 trees, we want to visualise 6 trees trained on the complete clean dataset, correct?

3) In cross-validation, for each fold x:
           a) train 6 trees on the other 9 folds
           b) get predictions by testing these 6 trees on the fold x,
           c) compute the error rate
           d) keep track of the predictions correctly and incorrectly
    at the end, compute one confusion matrix using all the predictions and their corresponding labels.
    
   Furthermore, when we talk about the average error rate, we talk about the average of the error rates for each of the k folds, correct?
   Am I understanding this correctly?

 4) when referring to the average recall & precision rates, we are talking about the the recall & precision rates of the aforementioned single confusion matrix?
     not the recall & precision rate of a confusion matrix computed for each fold? 
  
 5) the average classification rate is simply 1 - the average error rate? or is it the average of each fold's classification rate?
 





TODO:
should i randomize if multiple attributes introduce minimal avg entropy
