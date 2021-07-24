# viportfolio

build image from a Dockerfile
- docker build -t dockername .

run container
- docker run -i -t  dockername

# Usage in a container:
create max_sharpe ru-stocks portfolio with 2-month observations
- ./viportfolio.py ru create -p 2  

create Markowitz porfolio ru-stocks portfolio with target return 0.4, using 4-month observations and deposit 100000
- ./viportfolio.py ru create -p 4 -t optimal -r 0.4 -d 100000

analyze portfolio of Franklin FTSE Russia ETF for deposit 100000
- ./viportfolio.py  ru analyze -m franklin -d 100000

analyze portfolio of SEB Russia Fund for deposit 100000
- ./viportfolio.py  ru analyze -m seb -d 100000
 
analyze portfolio of Voya Russia Fund for deposit 100000
- ./viportfolio.py  ru analyze -m voya -d 100000

analyze portfolio of MSCI Russia Fund for deposit 100000
- ./viportfolio.py  ru analyze -m msci -d 100000

edit config file
- nano ./config.json
