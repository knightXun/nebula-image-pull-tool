import docker
import datetime
import time
import schedule

def image_pull():
    client = docker.from_env()
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    client.images.pull("docker.io/vesoft/nebula-metad:nightly")
    image = client.images.get("docker.io/vesoft/nebula-metad:nightly")
    image.tag( "docker.io/vesoft/nebula-metad" , str(month) + "-" + str(day))
    print("pull image: %s:%d-%d", "docker.io/vesoft/nebula-metad" , month , day)

    client.images.pull("docker.io/vesoft/nebula-storaged:nightly")
    image = client.images.get("docker.io/vesoft/nebula-storaged:nightly")
    image.tag( "docker.io/vesoft/nebula-storaged", str(month) + "-" + str(day))
    print("pull image: %s:%d-%d", "docker.io/vesoft/nebula-storaged" , month , day)

    client.images.pull("docker.io/vesoft/nebula-graphd:nightly")
    image = client.images.get("docker.io/vesoft/nebula-graphd:nightly")
    image.tag( "docker.io/vesoft/nebula-graphd", str(month) + "-" + str(day))
    print("pull image: %s:%d-%d", "docker.io/vesoft/nebula-graphd" , month , day)


def clean_images():
    client = docker.from_env()
    images = client.images.list()
    nebula_list = ["vesoft/nebula-graphd", "vesoft/nebula-metad", "vesoft/nebula-storaged"]
    cleans = []
    for image in images:
        tags = image.attrs['RepoTags']
        if len(tags) == 0:
            cleans.append(image.attrs['Id'])
            continue
        for nebula in nebula_list:
            for tag in tags:
                if nebula in tag:
                    buildTime = datetime.datetime.strptime(image.attrs['Created'].split('T')[0], "%Y-%m-%d")
                    if datetime.datetime.now() - buildTime > datetime.timedelta(30):
                        cleans.append(image.attrs['Id'])
    for id in cleans:
        try:
            client.images.remove(id, force=False)
        except Exception as e:
            print(e)

def pull_and_clean():
    image_pull()
    clean_images()

image_pull()

schedule.every().day.do(pull_and_clean)
while True:
    schedule.run_pending()
    time.sleep(1)



