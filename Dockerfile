FROM python:3.9.5
RUN pip install pandas
RUN pip install cvxopt
RUN pip install cvxpy
RUN pip install pandas-datareader
RUN pip install pyportfolioopt
RUN pip install tabulate
RUN apt-get update && apt-get install -y nano

COPY . /home
WORKDIR /home
CMD [ "bash" ]
