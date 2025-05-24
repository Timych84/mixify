FROM python:3.10.13-alpine3.19


# get curl for healthchecks
RUN apk add curl

# permissions and nonroot user for tightened security
RUN adduser -D nonroot && \
    mkdir -p /home/app /var/log/flask-app && \
    touch /var/log/flask-app/flask-app.err.log /var/log/flask-app/flask-app.out.log && \
    chown -R nonroot:nonroot /home/app /var/log/flask-app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrade pip
RUN pip install --upgrade pip

RUN export FLASK_APP=app.py
RUN pip install -r requirements.txt
RUN pip --version
# define the port number the container should expose
EXPOSE 5000

CMD ["python", "app.py"]
