FROM python
ADD main.py /
RUN pip3 install docker
RUN pip3 install schedule
ENTRYPOINT ["python3","main.py"]