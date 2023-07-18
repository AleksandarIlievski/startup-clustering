# bda-analytics-challenge

## Task Description
The start-up ecosystem is always changing and evolving. Getting an overview of existing start-ups and categorizing them into sectors is hard to do. The founding of new start-ups (with often low visibility), the abandonment of others, and new business ideas that do not fit in conventional business fields make this task even harder.

So your task is to use natural language processing (NLP), and unsupervised learning to categorize a list of start-ups based on the text that is found on the landing page of their website.

## Group Members: 
- Forename: Yuanchen
- Surname: Zhong
- Matriculation Number: 1950498

- Forename: Katharina
- Surname: Mitterer
- Matriculation Number: 2106230

- Forename: Aleksandar
- Surname: Ilievski
- Matriculation Number: 1954763

- Forename: Fabian
- Surname: Röckel
- Matriculation Number: 1970907

- Forename: Meriton
- Surname: Duraki
- Matriculation Number: 2506665

- Forename: Philipp
- Surname: Jäger
- Matriculation Number: 2112323

- Forename: Patrick
- Surname: Müller
- Matriculation Number: 2421690

- Forename: Franz   
- Surname: Muszarsky
- Matriculation Number: 2111400


**Operating System**: Windows

**Python Version**: 3.10.9

**Environment Setup**: 
````
conda create –n bda python=3.10.9
conda activate bda
pip install –r requirements.txt
````

**Unittest & docstring coverage**:
````
pytest --cov-report term --cov=src tests/
docstr-coverage src -i -f
````  


## Project Organization
------------
```
    ├── README.md 							
    ├── .gitignore 						    
    │   ├── preprocessed 					
    │   └── raw								
    ├── models								
    ├── presentation                        
    ├── notebooks							
    ├── requirements.txt 					
    ├── src
    │   ├── Clustering 			
    │   |   ├── HierachicalCluster.py 						
    │   |   └── LDA.py      
    │   ├── DataPreprocessing						
    │   |   └── Preprocessing_en.py 						
    │   └── Web_Scraping 				
    │       ├── basic_functions.py 						
    │       └── ScrapingMain.py                       
    └── tests
         ├── test_preprocessing_en.py                  
         └── test_scraping.py                               
	
```
## Code evaluation

To evaluate your code, we will run the following commands:

````
pytest --cov-report term --cov=src tests/
docstr-coverage src -i -f
````
