FROM ubuntu

RUN apt update
RUN apt install python3 -y
RUN apt install chromium-browser chromium-chromedriver -y
RUN apt install xvfb -y
RUN apt install bash -y
RUN apt install python3-pip -y

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install selenium
RUN python3 -m pip install ipython
RUN python3 -m pip install PyVirtualDisplay
RUN python3 -m pip install xlrd
RUN python3 -m pip install pystan
RUN python3 -m pip install fbprophet
RUN python3 -m pip install flask
RUN python3 -m pip install flask_sqlalchemy
RUN python3 -m pip install flask_marshmallow
RUN python3 -m pip install marshmallow-sqlalchemy
RUN python3 -m pip install plotly

RUN apt install cron -y

ADD . /usr/wd/urgency_predictor/.

RUN chmod 755 /usr/wd/urgency_predictor/daemon.sh /usr/wd/urgency_predictor/entry.sh
RUN crontab /usr/wd/urgency_predictor/crontab.txt
RUN bash /usr/wd/urgency_predictor/entry.sh
CMD ["python3","/usr/wd/urgency_predictor/download_and_predict.py"]
CMD ["python3","/usr/wd/urgency_predictor/app.py"]