# H1B Web Application Deployment
This repository shows the detailed instuction on how to deploy a Bokeh Server on Amazon Web Services EC2.

The website is: [18.219.1.116:5006](18.219.1.116:5006). Due to budget constraint, the server may be not always available.

Objective:

    Application Function:
    1. visualize top n sponsored job titles
    2. visualize top n H-1B sponsors
    3. search H-1B official data based on employer name or job title or any combination, and similar names and titles are returned

    Algorithm Design:
    this cool interactive web application is able to be distributed through internet (by using AWS)
    1. with efficient data loading process to minimize RAM usage
    2. with robust search engine to prohibit meaningless search (eg. non alphanumeric characters are skipped, and search with space is not allowed)
    3. with instructive real time message/error


## Original Data Source
H-1B data (FY15 to FY17) is obtained directly from [United States Department of Labor](https://www.foreignlaborcert.doleta.gov/performancedata.cfm). Then 3 years of data is combined to a single file and some unrelated columns are removed, more details are documented at [data source.txt](https://github.com/sxl5507/H1B-Web-Application.git).


## Download Trimmed Data
Trimmed [data](https://github.com/sxl5507/H1B-Web-Application.git) that is uploaded to AWS:
1. top 100 employer.csv
2. top 100 job title.csv
3. H-1B_Data_FY15to17.zip


## Python File
The main python file [H1B_bokeh_server.py]( https://github.com/sxl5507/H1B-Web-Application-Deployment.git) is built during previous project [H1B-Web-Application]( https://github.com/sxl5507/H1B-Web-Application.git), but we will focus on deployment in this repository.


## Setup AWS EC2 Instance
First, you need to create a new AWS account to get 12 months free-tier service. 

Under Services tab, find Compute/EC2, then launch instance.

Select ‘Ubuntu Server 16.04 LTS (HVM), EBS General Purpose (SSD) Volume Type’

Leave every configuration as default, but under ‘Configure Security Group’ change ‘Type’ to ‘All TCP’ and ‘Source’ to ‘Anywhere’.

Click ‘launch’ and select the drop down and create a new key pair, download it. You need it to connect to VM later.


## Create an Elastic IP
For web application to be permanently accessible from the same IP, we will need to allocate a static address. 

Under EC2 Dashboard/Network & Security/Elastic IPs, click ‘Allocate new address’

Under Action/Associate address, choose your EC2 instance and private IP


## Connect to Ubuntu VM
Download and install PuTTY software on your local computer.

Use PuTTYgen to convert your PEM key file to RSA format. Later, you only need RSA key


## Setup Bokeh Server on Ubuntu VM
Instruction: [Setup Bokeh Server on Ubuntu VM.txt](https://github.com/sxl5507/H1B-Web-Application-Deployment.git)


