# H1B Web Application Deployment
This repository shows the detailed instuction on how to deploy a Bokeh Server on Amazon Web Services EC2.


## Original Data Source
H-1B data (FY15 to FY17) is obtained directly from [United States Department of Labor](https://www.foreignlaborcert.doleta.gov/performancedata.cfm). Then 3 years of data is combined to a single file and some unrelated columns are removed, more details are documented at [data source.txt](https://github.com/sxl5507/H1B-Web-Application.git).


## Download Trimmed Data
Trimmed [data](https://github.com/sxl5507/H1B-Web-Application.git) that is uploaded to AWS:
1. top 100 employer.csv
2. top 100 job title.csv
3. H-1B_Data_FY15to17.zip

## Python File
The main python file [H1B_bokeh_server.py]( https://github.com/sxl5507/H1B-Web-Application-Deployment.git) is built during previous project [H1B-Web-Application]( https://github.com/sxl5507/H1B-Web-Application.git), but we will focus on deployment in this repository.

## Deployment on AWS EC2
Simplified instruction is recorded in [Bokeh Server on AWS EC2.txt] (https://github.com/sxl5507/H1B-Web-Application-Deployment.git).
