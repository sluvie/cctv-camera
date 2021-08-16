import docker


class DockerUtil:

    def __init__(self) -> None:
        self.client = docker.from_env()

    def containers(self, filters="*"):
        return self.client.containers.list(all=True, filters=filters)

    def container_status(self, container_name):
        container = self.client.containers.get(container_name)
        container_state = container.attrs['State']
        return container_state['Status'] == 'running'


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
