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

analyze portfolio of {{Fund name}} for deposit 100000
- ./viportfolio.py  ru analyze -m {{Fund code}} -d 100000

available funds:

| Fund name   | Fund code |
| ----------- | ----------- |
|  Voya Russia Fund   | voya        |
|  MSCI Russia Fund   | msci        |
|  UBS Equity Russia   | ubs     |
|  Franklin FTSE Russia ETF   | franklin   |
| SEB Eastern Europe Small and Mid Cap Fund (Russia part)      | seb       |
| SEB Russia Fund (after 2021-05-31 merged into "SEB Eastern Europe Small and Mid Cap Fund")     | seb_old      |

edit config file
- nano ./config.json
