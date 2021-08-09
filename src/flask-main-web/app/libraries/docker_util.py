import docker


class DockerUtil:

    def __init__(self) -> None:
        self.client = docker.from_env()


    def containers(self):
        return self.client.containers.list(all=True)





# same result with below line
#cli = docker.client.DockerClient(base_url='tcp://127.0.0.1:2375')
#cli = docker.DockerClient(base_url='tcp://127.0.0.1:2375')
'''
cli = docker.from_env()
containers = cli.containers.list(all=True)

cont = containers[0]
print(cont.short_id)
print(cont.name)
'''
